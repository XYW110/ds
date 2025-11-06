"""
技术分析文本生成器

将技术指标数据格式化为结构化文本，用于AI分析输入。
"""

from typing import Dict, Any
import pandas as pd


class TechnicalAnalysisTextGenerator:
    """技术分析文本生成器"""

    def __init__(self):
        pass

    def generate_analysis_text(self, market_data: Dict[str, Any]) -> str:
        """
        生成完整的技术分析文本

        Args:
            market_data: 市场数据

        Returns:
            str: 格式化的技术分析文本
        """
        technical_data = market_data.get('technical_data', {})
        trend_analysis = market_data.get('trend_analysis', {})
        current_price = market_data.get('price', 0)

        # 构建各部分文本
        sections = []

        # 1. 技术指标部分
        indicators_text = self._generate_indicators_text(technical_data, current_price)
        sections.append(indicators_text)

        # 2. 趋势分析部分
        trend_text = self._generate_trend_text(trend_analysis, technical_data)
        sections.append(trend_text)

        # 3. 支撑阻力部分
        support_resistance_text = self._generate_support_resistance_text(technical_data, current_price)
        sections.append(support_resistance_text)

        # 4. 成交量分析
        volume_text = self._generate_volume_text(technical_data)
        sections.append(volume_text)

        # 5. 综合评估
        assessment_text = self._generate_assessment_text(trend_analysis, technical_data)
        sections.append(assessment_text)

        return "\n\n".join(sections)

    def _generate_indicators_text(self, technical_data: Dict[str, Any], current_price: float) -> str:
        """生成技术指标文本"""
        text = "【技术指标分析】\n"

        # RSI分析
        rsi = technical_data.get('rsi', 50)
        if rsi > 70:
            rsi_status = "超买区间 (看跌信号)"
        elif rsi < 30:
            rsi_status = "超卖区间 (看涨信号)"
        elif 30 <= rsi <= 70:
            rsi_status = "正常区间"
        else:
            rsi_status = "数据异常"

        text += f"- RSI相对强弱指标: {rsi:.1f} ({rsi_status})\n"

        # 均线分析
        sma_5 = technical_data.get('sma_5', current_price)
        sma_20 = technical_data.get('sma_20', current_price)
        sma_50 = technical_data.get('sma_50', current_price)

        ma_trend = []
        if current_price > sma_5:
            ma_trend.append("价格突破5日均线")
        if current_price > sma_20:
            ma_trend.append("价格站在20日均线上方")
        if sma_5 > sma_20 > sma_50:
            ma_trend.append("均线多头排列")

        text += f"- 均线系统: 5日线{sma_5:.2f}, 20日线{sma_20:.2f}, 50日线{sma_50:.2f}\n"
        text += f"  均线信号: {'; '.join(ma_trend) if ma_trend else '均线无明确信号'}\n"

        # MACD分析
        macd = technical_data.get('macd', 0)
        macd_signal = technical_data.get('macd_signal', 0)
        macd_histogram = technical_data.get('macd_histogram', 0)

        if macd_histogram > 0:
            macd_signal_text = "MACD金叉 (看涨信号)"
        elif macd_histogram < 0:
            macd_signal_text = "MACD死叉 (看跌信号)"
        else:
            macd_signal_text = "MACD中性"

        text += f"- MACD指标: DIF={macd:.4f}, DEA={macd_signal:.4f}, MACD柱={macd_histogram:.4f}\n"
        text += f"  MACD信号: {macd_signal_text}\n"

        # 布林带分析
        bb_upper = technical_data.get('bb_upper', current_price * 1.02)
        bb_middle = technical_data.get('bb_middle', current_price)
        bb_lower = technical_data.get('bb_lower', current_price * 0.98)
        bb_position = technical_data.get('bb_position', 0.5)

        if bb_position > 0.8:
            bb_signal = "接近上轨 (超买警示)"
        elif bb_position < 0.2:
            bb_signal = "接近下轨 (超卖警示)"
        else:
            bb_signal = "在中轨附近震荡"

        text += f"- 布林带: 上轨{bb_upper:.2f}, 中轨{bb_middle:.2f}, 下轨{bb_lower:.2f}\n"
        text += f"  当前价格位置: {bb_position*100:.1f}% ({bb_signal})\n"

        return text

    def _generate_trend_text(self, trend_analysis: Dict[str, Any], technical_data: Dict[str, Any]) -> str:
        """生成趋势分析文本"""
        text = "【趋势分析】\n"

        # 整体趋势
        overall_trend = trend_analysis.get('overall', '震荡整理')
        short_term = trend_analysis.get('short_term', '震荡')
        medium_term = trend_analysis.get('medium_term', '震荡')
        macd_trend = trend_analysis.get('macd', 'neutral')

        text += f"- 整体趋势: {overall_trend}\n"
        text += f"- 短期趋势: {short_term}\n"
        text += f"- 中期趋势: {medium_term}\n"
        text += f"- MACD趋势: {macd_trend}\n"

        # 趋势强度评估
        rsi = technical_data.get('rsi', 50)
        volume_ratio = technical_data.get('volume_ratio', 1.0)

        trend_strength_score = 0
        if '上涨' in overall_trend:
            trend_strength_score += 2
        elif '下跌' in overall_trend:
            trend_strength_score -= 2

        if volume_ratio > 1.5:
            trend_strength_score += 1
        elif volume_ratio < 0.5:
            trend_strength_score -= 1

        if trend_strength_score >= 2:
            strength_text = "强势趋势"
        elif trend_strength_score >= 1:
            strength_text = "中等强度趋势"
        elif trend_strength_score <= -2:
            strength_text = "强势下跌趋势"
        elif trend_strength_score <= -1:
            strength_text = "中等强度下跌"
        else:
            strength_text = "无明确趋势"

        text += f"- 趋势强度: {strength_text}\n"

        return text

    def _generate_support_resistance_text(self, technical_data: Dict[str, Any], current_price: float) -> str:
        """生成支撑阻力文本"""
        text = "【支撑阻力分析】\n"

        # 静态支撑阻力
        resistance = technical_data.get('resistance', current_price * 1.05)
        support = technical_data.get('support', current_price * 0.95)

        resistance_distance = ((resistance - current_price) / current_price) * 100
        support_distance = ((current_price - support) / support) * 100

        text += f"- 静态阻力位: ${resistance:.2f} (距离{resistance_distance:+.2f}%)\n"
        text += f"- 静态支撑位: ${support:.2f} (距离{support_distance:+.2f}%)\n"

        # 动态支撑阻力 (布林带)
        bb_upper = technical_data.get('bb_upper', current_price * 1.02)
        bb_lower = technical_data.get('bb_lower', current_price * 0.98)

        bb_resistance_distance = ((bb_upper - current_price) / current_price) * 100
        bb_support_distance = ((current_price - bb_lower) / current_price) * 100

        text += f"- 动态阻力位 (布林带上轨): ${bb_upper:.2f} (距离{bb_resistance_distance:+.2f}%)\n"
        text += f"- 动态支撑位 (布林带下轨): ${bb_lower:.2f} (距离{bb_support_distance:+.2f}%)\n"

        # 关键价位评估
        if abs(resistance_distance) < 1:
            text += "- 当前价格接近阻力位，注意突破或回调\n"
        elif abs(support_distance) < 1:
            text += "- 当前价格接近支撑位，注意反弹或跌破\n"
        else:
            text += "- 当前价格在支撑阻力区间中部运行\n"

        return text

    def _generate_volume_text(self, technical_data: Dict[str, Any]) -> str:
        """生成成交量分析文本"""
        text = "【成交量分析】\n"

        volume_ratio = technical_data.get('volume_ratio', 1.0)

        if volume_ratio > 2.0:
            volume_status = "成交量异常放大"
            volume_implication = "可能预示趋势加速或反转"
        elif volume_ratio > 1.5:
            volume_status = "成交量显著增加"
            volume_implication = "趋势确认信号"
        elif volume_ratio < 0.5:
            volume_status = "成交量萎缩"
            volume_implication = "趋势可能乏力或盘整"
        else:
            volume_status = "成交量正常"
            volume_implication = "维持现有趋势"

        text += f"- 成交量比率: {volume_ratio:.2f} (相对于20日均量)\n"
        text += f"- 成交量状态: {volume_status}\n"
        text += f"- 技术含义: {volume_implication}\n"

        return text

    def _generate_assessment_text(self, trend_analysis: Dict[str, Any], technical_data: Dict[str, Any]) -> str:
        """生成综合评估文本"""
        text = "【综合技术评估】\n"

        # 多空力量对比
        bullish_factors = []
        bearish_factors = []

        # RSI因素
        rsi = technical_data.get('rsi', 50)
        if rsi < 30:
            bullish_factors.append("RSI超卖")
        elif rsi > 70:
            bearish_factors.append("RSI超买")

        # 均线因素
        current_price = technical_data.get('current_price', 0)
        sma_20 = technical_data.get('sma_20', current_price)
        if current_price > sma_20:
            bullish_factors.append("价格在均线上方")
        else:
            bearish_factors.append("价格在均线下方")

        # MACD因素
        macd_histogram = technical_data.get('macd_histogram', 0)
        if macd_histogram > 0:
            bullish_factors.append("MACD金叉")
        else:
            bearish_factors.append("MACD死叉")

        # 趋势因素
        overall_trend = trend_analysis.get('overall', '')
        if '���涨' in overall_trend:
            bullish_factors.append("整体趋势向上")
        elif '下跌' in overall_trend:
            bearish_factors.append("整体趋势向下")

        # 成交量因素
        volume_ratio = technical_data.get('volume_ratio', 1.0)
        if volume_ratio > 1.5:
            if bullish_factors:
                bullish_factors.append("放量配合")
            else:
                bearish_factors.append("放量下跌")
        elif volume_ratio < 0.5:
            bearish_factors.append("量能萎缩")

        # 输出评估结果
        if bullish_factors:
            text += f"- 看涨因素: {'; '.join(bullish_factors)}\n"
        if bearish_factors:
            text += f"- 看跌因素: {'; '.join(bearish_factors)}\n"

        # 技术建议
        bull_count = len(bullish_factors)
        bear_count = len(bearish_factors)

        if bull_count > bear_count + 1:
            text += "- 技术面偏向看涨，但需关注风险控制\n"
        elif bear_count > bull_count + 1:
            text += "- 技术面偏向看跌，建议谨慎操作\n"
        else:
            text += "- 技术面多空平衡，建议观望等待明确信号\n"

        return text

    def generate_summary_text(self, signal_data: Dict[str, Any], market_data: Dict[str, Any]) -> str:
        """
        生成信号摘要文本

        Args:
            signal_data: 信号数据
            market_data: 市场数据

        Returns:
            str: 摘要文本
        """
        signal = signal_data.get('signal', 'HOLD')
        confidence = signal_data.get('confidence', 'MEDIUM')
        reason = signal_data.get('reason', '')

        text = f"【交易信号摘要】\n"
        text += f"- 交易信号: {signal}\n"
        text += f"- 信心程度: {confidence}\n"
        text += f"- 分析理由: {reason}\n"

        if signal != 'HOLD':
            stop_loss = signal_data.get('stop_loss', 0)
            take_profit = signal_data.get('take_profit', 0)
            current_price = market_data.get('price', 0)

            stop_distance = abs(stop_loss - current_price) / current_price * 100
            profit_distance = abs(take_profit - current_price) / current_price * 100

            text += f"- 建议止损: ${stop_loss:.2f} (距离{stop_distance:.2f}%)\n"
            text += f"- 建议止盈: ${take_profit:.2f} (距离{profit_distance:.2f}%)\n"
            text += f"- 风险收益比: 1:{profit_distance/stop_distance:.2f}\n"

        return text