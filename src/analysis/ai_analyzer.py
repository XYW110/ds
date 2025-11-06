"""
AI分析模块

集成DeepSeek AI进行智能市场分析和交易信号生成。
"""

import json
import time
from typing import Dict, Any, Optional, List
from openai import OpenAI

from ..config import get_config
from ..utils.json_parser import JSONParser
from ..utils.fallback_generator import FallbackSignalGenerator


class AIAnalyzer:
    """通用AI分析引擎 - 统一OpenAI V1兼容接口"""

    def __init__(self):
        self.config = get_config().ai
        self.api_keys = get_config().api_keys

        # 获取API密钥，优先使用统一配置，向后兼容DeepSeek
        api_key = self.config.api_key or self.api_keys.get('deepseek_api_key')
        if not api_key:
            raise ValueError("未配置AI_API_KEY或DEEPSEEK_API_KEY")

        # 初始化OpenAI兼容客户端
        self.client = OpenAI(
            api_key=api_key,
            base_url=self.config.base_url
        )

        # 组件
        self.json_parser = JSONParser()
        self.fallback_generator = FallbackSignalGenerator()

        # 提示词模板
        self.system_prompt = self.config.system_prompt
        self.user_prompt_template = self._build_user_prompt_template()

    def _build_user_prompt_template(self) -> str:
        """构建用户提示词模板"""
        return """
你是一个专业的加密货币交易分析师。请基于以下BTC/USDT {timeframe}周期数据进行分析：

{kline_data}

{technical_analysis}

{signal_history}

{sentiment_text}

【当前行情】
- 当前价格: ${current_price:,.2f}
- 时间: {timestamp}
- 本K线最高: ${high:,.2f}
- 本K线最低: ${low:,.2f}
- 本K线成交量: {volume:.2f} BTC
- 价格变化: {price_change:+.2f}%
- 当前持仓: {position_text}{pnl_text}

【分析要求】
1. 基于{timeframe}K线趋势和技术指标给出交易信号: BUY(买入) / SELL(卖出) / HOLD(观望)
2. 简要分析理由（考虑趋势连续性、支撑阻力、成交量等因素）
3. 基于技术分析建议合理的止损价位
4. 基于技术分析建议合理的止盈价位
5. 评估信号信心程度

请用以下JSON格式回复：
{{
    "signal": "BUY|SELL|HOLD",
    "reason": "分析理由",
    "stop_loss": 具体价格,
    "take_profit": 具体价格,
    "confidence": "HIGH|MEDIUM|LOW"
}}
"""

    def analyze_market(self, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        分析市场并生成交易信号

        Args:
            market_data: 市场数据

        Returns:
            Dict[str, Any]: 交易信号数据
        """
        try:
            # 构建提示词
            prompt = self._build_prompt(market_data)

            # 调用DeepSeek API
            response = self._call_deepseek_api(prompt)

            if response:
                return response
            else:
                # 使用备用信号生成器
                print("⚠️ AI分析失败，使用备用信号生成器")
                return self.fallback_generator.generate_signal(market_data)

        except Exception as e:
            print(f"AI分析失败: {e}")
            return self.fallback_generator.generate_signal(market_data)

    def _build_prompt(self, market_data: Dict[str, Any]) -> str:
        """构建完整的提示词"""
        # 提取数据
        kline_data = market_data.get('kline_data', [])
        technical_analysis = market_data.get('technical_analysis_text', '')
        sentiment_text = market_data.get('sentiment_text', '【市场情绪】数据暂不可用')

        # 构建K线数据文本
        kline_text = f"【最近5根{market_data.get('timeframe', '15m')}K线数据】\n"
        for i, kline in enumerate(kline_data[-5:]):
            trend = "阳线" if kline['close'] > kline['open'] else "阴线"
            change = ((kline['close'] - kline['open']) / kline['open']) * 100
            kline_text += f"K线{i + 1}: {trend} 开盘:{kline['open']:.2f} 收盘:{kline['close']:.2f} 涨跌:{change:+.2f}%\n"

        # 构建信号历史文本
        signal_history = market_data.get('signal_history', [])
        signal_text = ""
        if signal_history:
            last_signal = signal_history[-1]
            signal_text = f"\n【上次交易信号】\n信号: {last_signal.get('signal', 'N/A')}\n信心: {last_signal.get('confidence', 'N/A')}"

        # 构建持仓文本
        current_position = market_data.get('current_position')
        position_text = "无持仓"
        pnl_text = ""
        if current_position:
            position_text = f"{current_position['side']}仓, 数量: {current_position['size']}"
            pnl_text = f", 持仓盈亏: {current_position['unrealized_pnl']:.2f} USDT"

        # 替换模板变量
        return self.user_prompt_template.format(
            timeframe=market_data.get('timeframe', '15m'),
            kline_data=kline_text,
            technical_analysis=technical_analysis,
            signal_history=signal_text,
            sentiment_text=sentiment_text,
            current_price=market_data.get('price', 0),
            timestamp=market_data.get('timestamp', ''),
            high=market_data.get('high', 0),
            low=market_data.get('low', 0),
            volume=market_data.get('volume', 0),
            price_change=market_data.get('price_change', 0),
            position_text=position_text,
            pnl_text=pnl_text
        )

    def _call_deepseek_api(self, prompt: str, max_retries: int = None) -> Optional[Dict[str, Any]]:
        """
        调用DeepSeek API

        Args:
            prompt: 提示词
            max_retries: 最大重试次数

        Returns:
            Dict[str, Any]: 解析后的信号数据
        """
        if max_retries is None:
            max_retries = self.config.max_retries

        retry_count = 0

        while retry_count <= max_retries:
            try:
                print(f"🤖 正在调用DeepSeek AI分析... (尝试 {retry_count + 1}/{max_retries + 1})")

                response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt.format(timeframe="15分钟")},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.config.temperature,
                    timeout=self.config.timeout
                )

                if not response.choices or not response.choices[0].message:
                    print("❌ DeepSeek返回数据为空")
                    continue

                result = response.choices[0].message.content
                if result is None:
                    print("❌ DeepSeek返回内容为空")
                    continue

                print(f"✅ DeepSeek分析完成")

                # 解析JSON响应
                signal_data = self.json_parser.parse_signal_json(result)

                if signal_data:
                    # 添加时间戳
                    signal_data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    signal_data['source'] = 'deepseek_ai'
                    return signal_data
                else:
                    print(f"⚠️ JSON解析失败，响应内容: {result[:200]}...")

            except Exception as e:
                print(f"❌ DeepSeek API调用失败 (尝试 {retry_count + 1}): {e}")

                if retry_count == max_retries:
                    print(f"❌ 已达到最大重试次数 {max_retries}")
                    break

                # 指数退避重试
                wait_time = min(2 ** retry_count, 10)
                print(f"⏳ 等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)

            retry_count += 1

        return None

    def analyze_with_retry(self, market_data: Dict[str, Any], max_retries: int = 2) -> Optional[Dict[str, Any]]:
        """
        带重试机制的分析

        Args:
            market_data: 市场数据
            max_retries: 最大重试次数

        Returns:
            Dict[str, Any]: 交易信号数据
        """
        return self._call_deepseek_api(self._build_prompt(market_data), max_retries)

    def validate_signal(self, signal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证信号数据的有效性

        Args:
            signal_data: 信号数据

        Returns:
            Dict[str, Any]: 验证结果
        """
        if not signal_data:
            return {
                'valid': False,
                'errors': ['信号数据为空']
            }

        errors = []
        warnings = []

        # 检查必需字段
        required_fields = ['signal', 'reason', 'confidence']
        for field in required_fields:
            if field not in signal_data:
                errors.append(f"缺少必需字段: {field}")

        # 检查信号值
        valid_signals = ['BUY', 'SELL', 'HOLD']
        if 'signal' in signal_data and signal_data['signal'] not in valid_signals:
            errors.append(f"无效的信号值: {signal_data['signal']}")

        # 检查信心度
        valid_confidence = ['HIGH', 'MEDIUM', 'LOW']
        if 'confidence' in signal_data and signal_data['confidence'] not in valid_confidence:
            warnings.append(f"异常的信心度: {signal_data['confidence']}")

        # 检查价格合理性
        if 'stop_loss' in signal_data and 'take_profit' in signal_data:
            stop_loss = signal_data['stop_loss']
            take_profit = signal_data['take_profit']

            if stop_loss <= 0 or take_profit <= 0:
                warnings.append("止损止盈价格异常")

            if 'signal' in signal_data:
                if signal_data['signal'] == 'BUY' and stop_loss >= take_profit:
                    warnings.append("BUY信号的止损价不应高于止盈价")
                elif signal_data['signal'] == 'SELL' and stop_loss <= take_profit:
                    warnings.append("SELL信号的止损价不应低于止盈价")

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def get_analysis_summary(self, signal_data: Dict[str, Any]) -> str:
        """
        获取分析摘要

        Args:
            signal_data: 信号数据

        Returns:
            str: 分析摘要
        """
        if not signal_data:
            return "无有效的分析结果"

        signal = signal_data.get('signal', 'N/A')
        confidence = signal_data.get('confidence', 'N/A')
        reason = signal_data.get('reason', 'N/A')
        stop_loss = signal_data.get('stop_loss', 'N/A')
        take_profit = signal_data.get('take_profit', 'N/A')

        summary = f"""
🤖 DeepSeek AI 分析结果
📊 交易信号: {signal}
🎯 信心程度: {confidence}
💡 分析理由: {reason}
🛑 建议止损: ${stop_loss:,.2f}
🎯 建议止盈: ${take_profit:,.2f}
        """.strip()

        return summary