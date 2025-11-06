"""
市场情绪分析模块

集成CryptOracle API获取市场情绪数据。
"""

import requests
import time
from typing import Dict, Any, Optional
from ..config import get_config


class SentimentAnalyzer:
    """市场情绪分析器"""

    def __init__(self):
        self.config = get_config().sentiment
        self.api_key = self.config.api_key
        self.base_url = self.config.api_base_url
        self.cache = {}
        self.cache_ttl = self.config.cache_ttl

    def fetch_sentiment_data(self) -> Optional[Dict[str, Any]]:
        """
        获取市场情绪数据

        Returns:
            Dict[str, Any]: 情绪数据
        """
        if not self.config.enable:
            print("📊 市场情绪功能已禁用")
            return None

        if not self.api_key:
            print("⚠️ 缺少CryptOracle API密钥，跳过情绪分析")
            return None

        # 检查缓存
        current_time = time.time()
        if 'sentiment_data' in self.cache:
            cached_data, cached_time = self.cache['sentiment_data']
            if current_time - cached_time < self.cache_ttl:
                print("📊 使用缓存的市场情绪数据")
                return cached_data

        try:
            print("📊 正在获取市场情绪数据...")
            sentiment_data = self._fetch_indicators()

            if sentiment_data:
                # 缓存数据
                self.cache['sentiment_data'] = (sentiment_data, current_time)
                print("✅ 市场情绪数据获取成功")
                return sentiment_data
            else:
                print("⚠️ 市场情绪数据获取失败")
                return None

        except Exception as e:
            print(f"❌ 获取市场情绪数据失败: {e}")
            return None

    def _fetch_indicators(self) -> Optional[Dict[str, Any]]:
        """
        获取情绪指标

        Returns:
            Dict[str, Any]: 情绪指标数据
        """
        indicators = self.config.indicators
        result = {}

        for indicator in indicators:
            try:
                data = self._fetch_single_indicator(indicator)
                if data:
                    result[indicator] = data
                    time.sleep(0.5)  # 避免请求过于频繁
            except Exception as e:
                print(f"⚠️ 获取指标 {indicator} 失败: {e}")
                continue

        if not result:
            return None

        # 计算综合情绪指标
        return self._calculate_composite_sentiment(result)

    def _fetch_single_indicator(self, indicator_id: str) -> Optional[Dict[str, Any]]:
        """
        获取单个情绪指标

        Args:
            indicator_id: 指标ID

        Returns:
            Dict[str, Any]: 指标数据
        """
        url = f"{self.base_url}/v1/indicators/{indicator_id}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            return self._process_indicator_data(indicator_id, data)

        except requests.exceptions.RequestException as e:
            print(f"❌ API请求失败 {indicator_id}: {e}")
            return None
        except Exception as e:
            print(f"❌ 处理指标数据失败 {indicator_id}: {e}")
            return None

    def _process_indicator_data(self, indicator_id: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理原始指标数据

        Args:
            indicator_id: 指标ID
            raw_data: 原始数据

        Returns:
            Dict[str, Any]: 处理后的数据
        """
        processed = {
            'indicator_id': indicator_id,
            'timestamp': raw_data.get('timestamp', int(time.time())),
            'value': None,
            'sentiment': 'neutral',
            'metadata': {}
        }

        # 根据指标ID处理不同类型的数据
        if indicator_id == 'CO-A-02-01':  # 恐慌贪婪指数
            value = raw_data.get('value', 50)
            processed['value'] = float(value)

            if value > 75:
                processed['sentiment'] = 'extreme_greed'
                processed['description'] = '极度贪婪'
            elif value > 60:
                processed['sentiment'] = 'greed'
                processed['description'] = '贪婪'
            elif value > 40:
                processed['sentiment'] = 'neutral'
                processed['description'] = '中性'
            elif value > 25:
                processed['sentiment'] = 'fear'
                processed['description'] = '恐惧'
            else:
                processed['sentiment'] = 'extreme_fear'
                processed['description'] = '极度恐惧'

        elif indicator_id == 'CO-A-02-02':  # 市场情绪评分
            value = raw_data.get('score', 0)
            processed['value'] = float(value)

            if value > 0.3:
                processed['sentiment'] = 'very_positive'
                processed['description'] = '非常积极'
            elif value > 0.1:
                processed['sentiment'] = 'positive'
                processed['description'] = '积极'
            elif value > -0.1:
                processed['sentiment'] = 'neutral'
                processed['description'] = '中性'
            elif value > -0.3:
                processed['sentiment'] = 'negative'
                processed['description'] = '消极'
            else:
                processed['sentiment'] = 'very_negative'
                processed['description'] = '非常消极'

        else:
            # 通用处理
            value = raw_data.get('value', 0)
            processed['value'] = float(value)
            processed['metadata'] = raw_data

        return processed

    def _calculate_composite_sentiment(self, indicators: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算综合情绪指标

        Args:
            indicators: 各指标数据

        Returns:
            Dict[str, Any]: 综合情绪数据
        """
        # 初始化统计
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        total_score = 0

        sentiment_values = []
        for indicator_id, data in indicators.items():
            sentiment = data.get('sentiment', 'neutral')
            value = data.get('value', 0)

            if 'positive' in sentiment:
                positive_count += 1
                total_score += abs(value)
            elif 'negative' in sentiment:
                negative_count += 1
                total_score -= abs(value)
            else:
                neutral_count += 1

            sentiment_values.append(value)

        # 计算综合情绪
        total_indicators = len(indicators)
        net_sentiment = total_score / total_indicators if total_indicators > 0 else 0

        # 计算比例
        positive_ratio = positive_count / total_indicators if total_indicators > 0 else 0
        negative_ratio = negative_count / total_indicators if total_indicators > 0 else 0
        neutral_ratio = neutral_count / total_indicators if total_indicators > 0 else 0

        # 确定综合情绪状态
        if net_sentiment > 0.2:
            composite_sentiment = 'bullish'
            composite_description = '乐观'
        elif net_sentiment > 0.05:
            composite_sentiment = 'slightly_bullish'
            composite_description = '略乐观'
        elif net_sentiment > -0.05:
            composite_sentiment = 'neutral'
            composite_description = '中性'
        elif net_sentiment > -0.2:
            composite_sentiment = 'slightly_bearish'
            composite_description = '略悲观'
        else:
            composite_sentiment = 'bearish'
            composite_description = '悲观'

        return {
            'composite_sentiment': composite_sentiment,
            'composite_description': composite_description,
            'net_sentiment': net_sentiment,
            'positive_ratio': positive_ratio,
            'negative_ratio': negative_ratio,
            'neutral_ratio': neutral_ratio,
            'indicators': indicators,
            'summary': {
                'total_indicators': total_indicators,
                'positive_count': positive_count,
                'negative_count': negative_count,
                'neutral_count': neutral_count,
                'average_sentiment_value': sum(sentiment_values) / len(sentiment_values) if sentiment_values else 0
            }
        }

    def format_sentiment_text(self, sentiment_data: Dict[str, Any]) -> str:
        """
        格式化情绪数据为文本

        Args:
            sentiment_data: 情绪数据

        Returns:
            str: 格式化的文本
        """
        if not sentiment_data:
            return "【市场情绪】数据暂不可用"

        composite = sentiment_data.get('composite_description', '中性')
        net_sentiment = sentiment_data.get('net_sentiment', 0)
        positive_ratio = sentiment_data.get('positive_ratio', 0)
        negative_ratio = sentiment_data.get('negative_ratio', 0)

        sign = '+' if net_sentiment >= 0 else ''
        text = f"【市场情绪】{composite} 乐观{positive_ratio:.1%} 悲观{negative_ratio:.1%} 净值{sign}{net_sentiment:.3f}"

        return text

    def get_sentiment_signal_weight(self, sentiment_data: Dict[str, Any]) -> float:
        """
        获取情绪信号权重

        Args:
            sentiment_data: 情绪数据

        Returns:
            float: 权重值 (-1 到 1)
        """
        if not sentiment_data:
            return 0.0

        net_sentiment = sentiment_data.get('net_sentiment', 0)

        # 将情绪值映射到权重
        # 乐观情绪增加权重，悲观情绪减少权重
        if net_sentiment > 0.3:
            return 0.3  # 最大正权重
        elif net_sentiment > 0.1:
            return 0.2
        elif net_sentiment > 0:
            return 0.1
        elif net_sentiment > -0.1:
            return 0.0  # 中性
        elif net_sentiment > -0.3:
            return -0.1
        else:
            return -0.2  # 负权重

    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()
        print("📊 市场情绪数据缓存已清空")

    def is_data_fresh(self) -> bool:
        """
        检查数据是否新鲜

        Returns:
            bool: 数据是否在缓存期内
        """
        if 'sentiment_data' not in self.cache:
            return False

        _, cached_time = self.cache['sentiment_data']
        current_time = time.time()
        return current_time - cached_time < self.cache_ttl