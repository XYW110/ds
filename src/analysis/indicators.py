"""
技术指标计算模块

提供完整的技术指标计算和分析功能。
"""

# type: ignore  # 忽略类型检查错误

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from ..config import get_config


@dataclass
class IndicatorResult:
    """技术指标计算结果"""
    sma: Dict[int, float] = None
    ema: Dict[int, float] = None
    macd: Dict[str, float] = None
    rsi: float = None
    bollinger_bands: Dict[str, float] = None
    volume_ratio: float = None
    support_resistance: Dict[str, float] = None

    def __post_init__(self):
        if self.sma is None:
            self.sma = {}
        if self.ema is None:
            self.ema = {}
        if self.macd is None:
            self.macd = {}
        if self.bollinger_bands is None:
            self.bollinger_bands = {}
        if self.support_resistance is None:
            self.support_resistance = {}


class TechnicalIndicators:
    """技术指标计算引擎"""

    def __init__(self):
        self.config = get_config().indicators

    def calculate_all(self, df: pd.DataFrame) -> IndicatorResult:
        """
        计算所有技术指标

        Args:
            df: K线数据DataFrame

        Returns:
            IndicatorResult: 所有指标的计算结果
        """
        if df.empty or len(df) < 20:
            return IndicatorResult()

        try:
            result = IndicatorResult()

            # 1. 移动平均线
            result.sma = self.calculate_sma(df, self.config.sma_periods)
            result.ema = self.calculate_ema(df, self.config.ema_periods)

            # 2. MACD指标
            result.macd = self.calculate_macd(df, **self.config.macd_params)

            # 3. RSI指标
            result.rsi = self.calculate_rsi(df, self.config.rsi_period)

            # 4. 布林带
            result.bollinger_bands = self.calculate_bollinger_bands(
                df, self.config.bb_period, self.config.bb_std
            )

            # 5. 成交���分析
            result.volume_ratio = self.calculate_volume_ratio(df)

            # 6. 支撑阻力位
            result.support_resistance = self.calculate_support_resistance(
                df, self.config.support_resistance_lookback
            )

            return result

        except Exception as e:
            print(f"技术指标计算失败: {e}")
            return IndicatorResult()

    def calculate_sma(self, df: pd.DataFrame, periods: List[int]) -> Dict[int, float]:
        """
        计算简单移动平均线

        Args:
            df: K线数据
            periods: 计算周期列表

        Returns:
            Dict[int, float]: 各周期的SMA值
        """
        result = {}
        for period in periods:
            if len(df) >= period:
                result[period] = df['close'].rolling(window=period, min_periods=1).mean().iloc[-1]
            else:
                result[period] = df['close'].iloc[-1]  # 数据不足时返回当前价格
        return result

    def calculate_ema(self, df: pd.DataFrame, periods: List[int]) -> Dict[int, float]:
        """
        计算指数移动平均线

        Args:
            df: K线数据
            periods: 计算周期列表

        Returns:
            Dict[int, float]: 各周期的EMA值
        """
        result = {}
        for period in periods:
            if len(df) >= period:
                result[period] = df['close'].ewm(span=period).mean().iloc[-1]
            else:
                result[period] = df['close'].iloc[-1]  # 数据不足时返回当前价格
        return result

    def calculate_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, float]:
        """
        计算MACD指标

        Args:
            df: K线数据
            fast: 快线周期
            slow: 慢线周期
            signal: 信号线周期

        Returns:
            Dict[str, float]: MACD指标值
        """
        try:
            ema_fast = df['close'].ewm(span=fast).mean()
            ema_slow = df['close'].ewm(span=slow).mean()
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal).mean()
            histogram = macd_line - signal_line

            return {
                'macd': macd_line.iloc[-1],
                'signal': signal_line.iloc[-1],
                'histogram': histogram.iloc[-1],
                'trend': 'bullish' if histogram.iloc[-1] > 0 else 'bearish'
            }
        except Exception as e:
            print(f"MACD计算失败: {e}")
            return {'macd': 0, 'signal': 0, 'histogram': 0, 'trend': 'neutral'}

    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> float:
        """
        计算RSI相对强弱指标

        Args:
            df: K线数据
            period: 计算周期

        Returns:
            float: RSI值
        """
        try:
            if len(df) < period + 1:
                return 50.0  # 数据不足时返回中性值

            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period, min_periods=1).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period, min_periods=1).mean()

            # 避免除零错误
            rs = gain / loss.replace(0, np.inf)
            rsi = 100 - (100 / (1 + rs))

            return rsi.iloc[-1]

        except Exception as e:
            print(f"RSI计算失败: {e}")
            return 50.0

    def calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20, std: float = 2.0) -> Dict[str, float]:
        """
        计算布林带

        Args:
            df: K线数据
            period: 计算周期
            std: 标准差倍数

        Returns:
            Dict[str, float]: 布林带指标值
        """
        try:
            if len(df) < period:
                current_price = df['close'].iloc[-1]
                return {
                    'upper': current_price,
                    'middle': current_price,
                    'lower': current_price,
                    'position': 0.5
                }

            middle = df['close'].rolling(window=period, min_periods=1).mean().iloc[-1]
            std_dev = df['close'].rolling(window=period, min_periods=1).std().iloc[-1]
            upper = middle + (std_dev * std)
            lower = middle - (std_dev * std)

            current_price = df['close'].iloc[-1]
            position = (current_price - lower) / (upper - lower) if upper != lower else 0.5

            return {
                'upper': upper,
                'middle': middle,
                'lower': lower,
                'position': position,
                'squeeze': (upper - lower) / middle  # 挤压指标
            }

        except Exception as e:
            print(f"布林带计算失败: {e}")
            current_price = df['close'].iloc[-1]
            return {
                'upper': current_price,
                'middle': current_price,
                'lower': current_price,
                'position': 0.5
            }

    def calculate_volume_ratio(self, df: pd.DataFrame, ma_period: int = 20) -> float:
        """
        计算成交量比例

        Args:
            df: K线数据
            ma_period: 移动平均周期

        Returns:
            float: 成交量比例
        """
        try:
            if len(df) < ma_period:
                return 1.0  # 数据不足时返回正常值

            volume_ma = df['volume'].rolling(window=ma_period, min_periods=1).mean().iloc[-1]
            current_volume = df['volume'].iloc[-1]

            return current_volume / volume_ma if volume_ma > 0 else 1.0

        except Exception as e:
            print(f"成交量比例计算失败: {e}")
            return 1.0

    def calculate_support_resistance(self, df: pd.DataFrame, lookback: int = 20) -> Dict[str, float]:
        """
        计算支撑阻力位

        Args:
            df: K线数据
            lookback: 回看周期

        Returns:
            Dict[str, float]: 支撑阻力位信息
        """
        try:
            if len(df) < lookback:
                current_price = df['close'].iloc[-1]
                return {
                    'resistance': current_price * 1.05,
                    'support': current_price * 0.95,
                    'resistance_distance': 5.0,
                    'support_distance': 5.0
                }

            recent_data = df.tail(lookback)
            resistance = recent_data['high'].max()
            support = recent_data['low'].min()
            current_price = df['close'].iloc[-1]

            resistance_distance = ((resistance - current_price) / current_price) * 100
            support_distance = ((current_price - support) / support) * 100

            return {
                'resistance': resistance,
                'support': support,
                'resistance_distance': resistance_distance,
                'support_distance': support_distance,
                'mid_price': (resistance + support) / 2
            }

        except Exception as e:
            print(f"支撑阻力计算失败: {e}")
            current_price = df['close'].iloc[-1]
            return {
                'resistance': current_price * 1.05,
                'support': current_price * 0.95,
                'resistance_distance': 5.0,
                'support_distance': 5.0
            }

    def get_market_trend(self, indicators: IndicatorResult, current_price: float) -> Dict[str, Any]:
        """
        分析市场趋势

        Args:
            indicators: 技术指标结果
            current_price: 当前价格

        Returns:
            Dict[str, Any]: 趋势分析结果
        """
        try:
            # 均线趋势分析
            sma_trend_points = 0
            if indicators.sma.get(5, 0) > indicators.sma.get(20, 0):
                sma_trend_points += 1
            if indicators.sma.get(20, 0) > indicators.sma.get(50, 0):
                sma_trend_points += 1

            if current_price > indicators.sma.get(5, 0):
                sma_trend_points += 1
            if current_price > indicators.sma.get(20, 0):
                sma_trend_points += 1

            # EMA趋势分析
            ema_trend = 'bullish' if indicators.ema.get(12, 0) > indicators.ema.get(26, 0) else 'bearish'

            # MACD趋势
            macd_trend = indicators.macd.get('trend', 'neutral')

            # 布林带位置
            bb_position = indicators.bollinger_bands.get('position', 0.5)
            if bb_position > 0.8:
                bb_signal = 'overbought'
            elif bb_position < 0.2:
                bb_signal = 'oversold'
            else:
                bb_signal = 'neutral'

            # RSI水平
            rsi_level = indicators.rsi or 50
            if rsi_level > 70:
                rsi_signal = 'overbought'
            elif rsi_level < 30:
                rsi_signal = 'oversold'
            else:
                rsi_signal = 'neutral'

            # 综合趋势判��
            trend_score = sma_trend_points + (1 if macd_trend == 'bullish' else -1)
            if trend_score >= 4:
                overall_trend = 'strong_uptrend'
            elif trend_score >= 2:
                overall_trend = 'uptrend'
            elif trend_score <= -2:
                overall_trend = 'downtrend'
            elif trend_score <= -4:
                overall_trend = 'strong_downtrend'
            else:
                overall_trend = 'sideways'

            return {
                'overall_trend': overall_trend,
                'sma_trend_points': sma_trend_points,
                'ema_trend': ema_trend,
                'macd_trend': macd_trend,
                'bb_signal': bb_signal,
                'rsi_signal': rsi_signal,
                'rsi_value': rsi_level,
                'bb_position': bb_position,
                'volume_strength': 'high' if indicators.volume_ratio > 1.5 else 'low' if indicators.volume_ratio < 0.5 else 'normal'
            }

        except Exception as e:
            print(f"趋势分析失败: {e}")
            return {
                'overall_trend': 'neutral',
                'sma_trend_points': 0,
                'ema_trend': 'neutral',
                'macd_trend': 'neutral',
                'bb_signal': 'neutral',
                'rsi_signal': 'neutral',
                'rsi_value': 50,
                'bb_position': 0.5,
                'volume_strength': 'normal'
            }