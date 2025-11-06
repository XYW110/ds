"""
配置管理器

集中管理所有系统配置，支持环境变量优先级。
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from dataclasses import dataclass

# 加载环境变量
load_dotenv()


@dataclass
class TradingConfig:
    """交易配置"""
    symbol: str = 'BTC/USDT:USDT'
    leverage: int = 10
    timeframe: str = '15m'
    test_mode: bool = True
    data_points: int = 96


@dataclass
class IndicatorConfig:
    """技术指标配置"""
    sma_periods: Optional[List[int]] = None
    ema_periods: Optional[List[int]] = None
    rsi_period: int = 14
    macd_params: Optional[Dict[str, int]] = None
    bb_period: int = 20
    bb_std: float = 2.0
    support_resistance_lookback: int = 20
    analysis_periods: Optional[Dict[str, int]] = None

    def __post_init__(self):
        if self.sma_periods is None:
            self.sma_periods = [5, 20, 50, 96]
        if self.ema_periods is None:
            self.ema_periods = [12, 26]
        if self.macd_params is None:
            self.macd_params = {'fast': 12, 'slow': 26, 'signal': 9}
        if self.analysis_periods is None:
            self.analysis_periods = {
                'short_term': 20,
                'medium_term': 50,
                'long_term': 96
            }


@dataclass
class AIConfig:
    """AI分析配置 - 统一OpenAI V1兼容接口"""
    api_key: str = ''
    base_url: str = 'https://api.deepseek.com'
    model: str = 'deepseek-chat'
    temperature: float = 0.1
    max_retries: int = 2
    timeout: Optional[int] = 10
    system_prompt: Optional[str] = None

    def __post_init__(self):
        if self.system_prompt is None:
            self.system_prompt = (
                "您是一位专业的加密货币交易分析师。"
                "专注于{timeframe}周期趋势分析。"
                "结合K线形态、技术指标、支撑阻力位和成交量进行综合判断。"
                "请以严谨的态度分析市场，给出明确的交易建议。"
            )


@dataclass
class PositionConfig:
    """仓位管理配置"""
    enable_intelligent_position: bool = True
    base_usdt_amount: float = 100.0
    high_confidence_multiplier: float = 1.5
    medium_confidence_multiplier: float = 1.0
    low_confidence_multiplier: float = 0.5
    max_position_ratio: float = 10.0
    trend_strength_multiplier: float = 1.2


@dataclass
class SentimentConfig:
    """市场情绪配置"""
    enable: bool = True
    api_key: Optional[str] = None
    api_base_url: str = "https://api.cryptoracle.io"
    indicators: Optional[List[str]] = None
    cache_ttl: int = 900  # 15分钟缓存

    def __post_init__(self):
        if self.indicators is None:
            self.indicators = ['CO-A-02-01', 'CO-A-02-02']


class Config:
    """主配置类"""

    def __init__(self):
        self.trading = self._load_trading_config()
        self.indicators = self._load_indicator_config()
        self.ai = self._load_ai_config()
        self.position = self._load_position_config()
        self.sentiment = self._load_sentiment_config()
        self.api_keys = self._load_api_keys()

    def _load_trading_config(self) -> TradingConfig:
        """加载交易配置"""
        return TradingConfig(
            symbol=os.getenv('TRADE_SYMBOL', 'BTC/USDT:USDT'),
            leverage=int(os.getenv('TRADE_LEVERAGE', '10')),
            timeframe=os.getenv('TRADE_TIMEFRAME', '15m'),
            test_mode=os.getenv('TRADE_TEST_MODE', 'true').lower() == 'true',
            data_points=int(os.getenv('TRADE_DATA_POINTS', '96'))
        )

    def _load_indicator_config(self) -> IndicatorConfig:
        """加载技术指标配置"""
        return IndicatorConfig()

    def _load_ai_config(self) -> AIConfig:
        """加载AI配置"""
        return AIConfig(
            api_key=os.getenv('AI_API_KEY', ''),
            base_url=os.getenv('AI_BASE_URL', 'https://api.deepseek.com'),
            model=os.getenv('AI_MODEL', 'deepseek-chat'),
            temperature=float(os.getenv('AI_TEMPERATURE', '0.1')),
            max_retries=int(os.getenv('AI_MAX_RETRIES', '2')),
            timeout=int(os.getenv('AI_TIMEOUT', '10'))
        )

    def _load_position_config(self) -> PositionConfig:
        """加载仓位配置"""
        return PositionConfig(
            enable_intelligent_position=os.getenv('POSITION_INTELLIGENT', 'true').lower() == 'true',
            base_usdt_amount=float(os.getenv('POSITION_BASE_USDT', '100')),
            high_confidence_multiplier=float(os.getenv('POSITION_HIGH_MULTIPLIER', '1.5')),
            medium_confidence_multiplier=float(os.getenv('POSITION_MEDIUM_MULTIPLIER', '1.0')),
            low_confidence_multiplier=float(os.getenv('POSITION_LOW_MULTIPLIER', '0.5')),
            max_position_ratio=float(os.getenv('POSITION_MAX_RATIO', '10')),
            trend_strength_multiplier=float(os.getenv('POSITION_TREND_MULTIPLIER', '1.2'))
        )

    def _load_sentiment_config(self) -> SentimentConfig:
        """加载情绪配置"""
        return SentimentConfig(
            enable=os.getenv('SENTIMENT_ENABLE', 'true').lower() == 'true',
            api_key=os.getenv('CRYPTORACLE_API_KEY'),
            cache_ttl=int(os.getenv('SENTIMENT_CACHE_TTL', '900'))
        )

    def _load_api_keys(self) -> Dict[str, Optional[str]]:
        """加载API密钥"""
        return {
            # AI统一API密钥
            'ai_api_key': os.getenv('AI_API_KEY'),
            'deepseek_api_key': os.getenv('DEEPSEEK_API_KEY'),  # 向后兼容

            # 交易所API密钥
            'okx_api_key': os.getenv('OKX_API_KEY'),
            'okx_secret': os.getenv('OKX_SECRET'),
            'okx_password': os.getenv('OKX_PASSWORD'),
            'binance_api_key': os.getenv('BINANCE_API_KEY'),
            'binance_secret': os.getenv('BINANCE_SECRET')
        }

    def validate(self) -> Dict[str, Any]:
        """验证配置完整性"""
        errors = []
        warnings = []

        # 检查必需的API密钥
        required_keys = ['deepseek_api_key']
        for key in required_keys:
            if not self.api_keys.get(key):
                errors.append(f"缺少必需的API密钥: {key}")

        # 检查交易所配置
        has_okx = all([self.api_keys['okx_api_key'], self.api_keys['okx_secret'], self.api_keys['okx_password']])
        has_binance = all([self.api_keys['binance_api_key'], self.api_keys['binance_secret']])

        if not has_okx and not has_binance:
            errors.append("至少需要配置一个交易所的完整API密钥 (OKX 或 Binance)")

        # 检查情绪数据配置
        if self.sentiment.enable and not self.sentiment.api_key:
            warnings.append("市场情绪功能已启用但缺少API密钥，将跳过情绪分析")

        # 检查交易参数合理性
        if self.trading.leverage < 1 or self.trading.leverage > 100:
            errors.append(f"杠杆倍数不合理: {self.trading.leverage}，应在1-100之间")

        if self.position.base_usdt_amount < 10:
            warnings.append(f"基础仓位金额较小: {self.position.base_usdt_amount} USDT")

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'trading': self.trading.__dict__,
            'indicators': self.indicators.__dict__,
            'ai': self.ai.__dict__,
            'position': self.position.__dict__,
            'sentiment': self.sentiment.__dict__
        }


# 全局配置实例
_config: Optional[Config] = None


def get_config() -> Config:
    """获取全局配置实例"""
    global _config
    if _config is None:
        _config = Config()
    return _config


def reset_config():
    """重置配置（主要用于测试）"""
    global _config
    _config = None


# 兼容性常量 (保持向后兼容)
def get_legacy_trade_config() -> Dict[str, Any]:
    """获取兼容旧版的交易配置"""
    config = get_config()
    return {
        **config.trading.__dict__,
        'analysis_periods': config.indicators.analysis_periods,
        'position_management': config.position.__dict__
    }