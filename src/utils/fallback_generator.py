"""
备用信号生成器

在AI分析失败时提供基于规则的备用信号。
"""

# type: ignore  # 忽略类型检查错误

from typing import Dict, Any, Optional, List
import time
from ..config import get_config


class FallbackSignalGenerator:
    """备用信号生成器"""

    def __init__(self):
        self.config = get_config().fallback_generator
        self.signal_history = []
        self.max_history = self.config.max_history

    def generate_signal(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成备用交易信号

        Args:
            market_data: 市场数据

        Returns:
            Dict[str, Any]: 交易信号数据
        """
        try:
            # 1. 获取技术数据
            technical_data = market_data.get('technical_data', {})
            trend_analysis = market_data.get('trend_analysis', {})
            current_price = market_data.get('price', 0)

            # 2. 计算技术指标评分
            scores = self._calculate_indicator_scores(technical_data, trend_analysis, current_price)

            # 3. 计算总分
            total_score = sum(scores.values())

            # 4. 确定信号
            signal = self._determine_signal(total_score, trend_analysis, market_data)

            # 5. 生成理由
            reason = self._generate_reason(scores, signal, market_data)

            # 6. 设置止损止盈
            stop_loss, take_profit = self._calculate_stop_take_profit(
                signal, current_price, technical_data, market_data
            )

            # 7. 评估信心度
            confidence = self._assess_confidence(total_score, signal, trend_analysis)

            # 8. 构建结果
            signal_data = {
                'signal': signal,
                'reason': reason,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'confidence': confidence,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'fallback_generator',
                'scores': scores,
                'total_score': total_score
            }

            # 9. 保存到历史
            self._save_to_history(signal_data)

            return signal_data

        except Exception as e:
            print(f"Backup signal generation failed: {e}")
            return self._generate_default_signal(market_data)

    def _calculate_indicator_scores(self, technical_data: Dict[str, Any],
                                  trend_analysis: Dict[str, Any],
                                  current_price: float) -> Dict[str, float]:
        """计算各技术指标评分"""
        scores = {}

        # 1. RSI评分
        rsi = technical_data.get('rsi', 50)
        if rsi > 70:
            scores['rsi'] = -1  # 超买，卖出信号
        elif rsi < 30:
            scores['rsi'] = +1  # 超卖，买入信号
        else:
            scores['rsi'] = 0   # 中性

        # 2. 均线评分
        sma_20 = technical_data.get('sma_20', current_price)
        if current_price > sma_20:
            scores['ma'] = +1  # 价格在均线上方，买入信号
        else:
            scores['ma'] = -1  # 价格在均线下方，卖出信号

        # 3. MACD评分
        macd_histogram = technical_data.get('macd_histogram', 0)
        if macd_histogram > 0:
            scores['macd'] = +1  # MACD正值，买入信号
        else:
            scores['macd'] = -1  # MACD负值，卖出信号

        # 4. 布林带评分
        bb_position = technical_data.get('bb_position', 0.5)
        if bb_position > 0.8:
            scores['bb'] = -1  # 接近上轨，卖出信号
        elif bb_position < 0.2:
            scores['bb'] = +1  # 接近下轨，买入信号
        else:
            scores['bb'] = 0   # 中性区间

        # 5. 趋势评分
        overall_trend = trend_analysis.get('overall', '').lower()
        if '上涨' in overall_trend or 'uptrend' in overall_trend:
            scores['trend'] = +self.config.trend_weight  # 趋势向上，加分
        elif '下跌' in overall_trend or 'downtrend' in overall_trend:
            scores['trend'] = -self.config.trend_weight  # 趋势向下，减分
        else:
            scores['trend'] = 0     # 震荡趋势，中性

        # 6. 成交量评分
        volume_ratio = technical_data.get('volume_ratio', 1.0)
        if volume_ratio > 1.5:
            scores['volume'] = +self.config.volume_weight  # 高成交量，加分
        elif volume_ratio < 0.5:
            scores['volume'] = -self.config.volume_weight  # 低成交量，减分
        else:
            scores['volume'] = 0     # 正常成交量

        # 7. 价格变化评分
        price_change = market_data.get('price_change', 0)
        if abs(price_change) > 1.0:  # 大于1%的变化
            scores['price_change'] = self.config.volume_weight if price_change > 0 else -self.config.volume_weight
        else:
            scores['price_change'] = 0

        return scores

    def _determine_signal(self, total_score: float, trend_analysis: Dict[str, Any],
                         market_data: Dict[str, Any]) -> str:
        """确定交易信号"""
        # 基于分数判断
        if total_score > self.config.buy_threshold:
            base_signal = 'BUY'
        elif total_score < self.config.sell_threshold:
            base_signal = 'SELL'
        else:
            base_signal = 'HOLD'

        # 考虑趋势确认
        overall_trend = trend_analysis.get('overall', '').lower()
        if '上涨' in overall_trend and base_signal == 'SELL':
            # 趋势向上但指标看跌，保守选择HOLD
            return 'HOLD'
        elif '下跌' in overall_trend and base_signal == 'BUY':
            # 趋势向下但指标看涨，保守选择HOLD
            return 'HOLD'

        return base_signal

    def _generate_reason(self, scores: Dict[str, float], signal: str,
                        market_data: Dict[str, Any]) -> str:
        """生成交易理由"""
        reasons = []

        # 找出主要影响因素
        sorted_scores = sorted(scores.items(), key=lambda x: abs(x[1]), reverse=True)

        for indicator, score in sorted_scores[:3]:  # 取前3个主要因素
            if abs(score) < 0.5:
                continue

            if indicator == 'rsi':
                if score > 0:
                    reasons.append("RSI显示超卖")
                else:
                    reasons.append("RSI显示超买")
            elif indicator == 'ma':
                if score > 0:
                    reasons.append("价格在均线上方")
                else:
                    reasons.append("价格在均线下方")
            elif indicator == 'macd':
                if score > 0:
                    reasons.append("MACD指标看涨")
                else:
                    reasons.append("MACD指标看跌")
            elif indicator == 'bb':
                if score > 0:
                    reasons.append("接近布林带下轨")
                else:
                    reasons.append("接近布林带上轨")
            elif indicator == 'trend':
                if score > 0:
                    reasons.append("整体趋势向上")
                else:
                    reasons.append("整体趋势向下")

        if not reasons:
            reasons.append("基于综合技术分析")

        if signal == 'HOLD':
            reasons.append("建议观望等待明确信号")

        return "；".join(reasons)

    def _calculate_stop_take_profit(self, signal: str, current_price: float,
                                   technical_data: Dict[str, Any],
                                   market_data: Dict[str, Any]) -> tuple:
        """计算止损止盈价格"""
        # 默认百分比
        stop_loss_pct = self.config.stop_loss_pct
        take_profit_pct = self.config.take_profit_pct

        # 获取支撑阻力位
        support = technical_data.get('support', current_price * 0.98)
        resistance = technical_data.get('resistance', current_price * 1.02)

        if signal == 'BUY':
            # 买入信号
            stop_loss = max(support, current_price * (1 - stop_loss_pct))
            take_profit = min(resistance, current_price * (1 + take_profit_pct))
        elif signal == 'SELL':
            # 卖出信号
            stop_loss = min(resistance, current_price * (1 + stop_loss_pct))
            take_profit = max(support, current_price * (1 - take_profit_pct))
        else:
            # HOLD信号，使用当前价格
            stop_loss = current_price
            take_profit = current_price

        return round(stop_loss, 2), round(take_profit, 2)

    def _assess_confidence(self, total_score: float, signal: str,
                          trend_analysis: Dict[str, Any]) -> str:
        """评估信号信心度"""
        score_abs = abs(total_score)

        # 基于分数评估
        if score_abs > 3:
            base_confidence = 'HIGH'
        elif score_abs > 1:
            base_confidence = 'MEDIUM'
        else:
            base_confidence = 'LOW'

        # 考虑趋势一致性
        overall_trend = trend_analysis.get('overall', '').lower()
        trend_consistent = (
            (signal == 'BUY' and '上涨' in overall_trend) or
            (signal == 'SELL' and '下跌' in overall_trend) or
            (signal == 'HOLD')
        )

        if trend_consistent and base_confidence == 'MEDIUM':
            base_confidence = 'HIGH'
        elif not trend_consistent and base_confidence == 'HIGH':
            base_confidence = 'MEDIUM'

        return base_confidence

    def _save_to_history(self, signal_data: Dict[str, Any]):
        """保存信号到历史"""
        self.signal_history.append(signal_data)
        if len(self.signal_history) > self.max_history:
            self.signal_history.pop(0)

    def _generate_default_signal(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成默认信号（极端情况使用）"""
        current_price = market_data.get('price', 0)

        return {
            'signal': 'HOLD',
            'reason': '系统异常，建议观望等待',
            'stop_loss': current_price * 0.98,
            'take_profit': current_price * 1.02,
            'confidence': 'LOW',
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'fallback_generator',
            'scores': {},
            'total_score': 0
        }

    def get_recent_signals(self, count: int = 5) -> List[Dict[str, Any]]:
        """获取最近的信号"""
        return self.signal_history[-count:]

    def clear_history(self):
        """清空历史记录"""
        self.signal_history.clear()