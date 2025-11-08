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
    default_exchange: str = 'auto'  # 默认交易所：auto/okx/binance


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
    
    # 新增：技术指标阈值配置
    min_data_points: int = 20  # 最小数据点数
    rsi_neutral: float = 50.0  # RSI中性值
    rsi_overbought: float = 70.0  # RSI超买阈值
    rsi_oversold: float = 30.0  # RSI超卖阈值
    bb_overbought: float = 0.8  # 布林带超买位置
    bb_oversold: float = 0.2  # 布林带超卖位置
    bb_neutral: float = 0.5  # 布林带中性位置
    volume_high_threshold: float = 1.5  # 高成交量倍数
    volume_low_threshold: float = 0.5  # 低成交量倍数
    support_resistance_default_pct: float = 0.05  # 默认支撑阻力位百分比 (5%)
    
    # 趋势判断阈值
    trend_strong_up_threshold: int = 4  # 强势上涨阈值
    trend_up_threshold: int = 2  # 上涨阈值
    trend_down_threshold: int = -2  # 下跌阈值
    trend_strong_down_threshold: int = -4  # 强势下跌阈值

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
    
    # 新增：AI分析参数
    retry_backoff_base: int = 2  # 指数退避基数
    retry_max_wait: int = 10  # 单次重试最长等待时间(秒)
    kline_display_count: int = 5  # 发送给AI的K线数量
    signal_history_count: int = 3  # 包含在分析中的历史信号数

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
    
    # 新增：仓位管理参数
    fixed_contracts: float = 0.1  # 禁用智能仓位时的固定合约数量
    rsi_extreme_high: float = 75.0  # 极端高RSI阈值
    rsi_extreme_low: float = 25.0  # 极端低RSI阈值
    rsi_extreme_multiplier: float = 0.7  # 极端RSI时的仓位调整倍数
    add_position_multiplier: float = 1.2  # 同向加仓倍数
    
    # 风险控制参数
    max_loss_pct: float = 5.0  # 单次最大损失百分比
    min_reward_ratio: float = 1.0  # 最小风险收益比
    default_stop_loss_pct: float = 0.02  # 默认止损百分比 (2%)
    default_take_profit_pct: float = 0.02  # 默认止盈百分比 (2%)


@dataclass
class DailyLimitConfig:
    """日投入限额配置"""
    enable: bool = True
    daily_limit_usdt: float = 1000.0  # 日投入限额(USDT)
    reset_hour: int = 0  # 重置时间点(小时，0-23)
    reset_timezone: str = "Asia/Shanghai"  # 重置时间时区
    max_total_exposure: float = 50.0  # 最大总敞口比例(%)
    min_reserve_balance: float = 100.0  # 最小保留余额(USDT)
    database_path: str = "data/daily_limits.db"  # SQLite数据库路径
    warning_threshold: float = 0.8  # 警告阈值(80%时发出警告)


@dataclass
class SentimentConfig:
    """��场情绪配置"""
    enable: bool = True
    api_key: Optional[str] = None
    api_base_url: str = "https://api.cryptoracle.io"
    indicators: Optional[List[str]] = None
    cache_ttl: int = 900  # 15分钟缓存

    def __post_init__(self):
        if self.indicators is None:
            self.indicators = ['CO-A-02-01', 'CO-A-02-02']


@dataclass
class FrequencyGuardConfig:
    """防频繁交易配置"""
    min_interval_minutes: int = 15  # 最小交易间隔(分钟)
    max_history: int = 50  # 信号历史容量
    consecutive_limit: int = 3  # 连续相同信号阈值
    hold_confirm_periods: int = 2  # HOLD确认周期数
    reversal_window: int = 10  # 信号反转检查窗口
    max_reversals: int = 4  # 窗口内最大反转次数


@dataclass
class OrderExecutorConfig:
    """订单执行配置"""
    max_history: int = 100  # 订单历史容量
    wait_seconds: int = 2  # 订单等待时间(秒)
    order_tag_open: str = "deepseek_bot"  # 开仓订单标签
    order_tag_close: str = "deepseek_bot_close"  # 平仓订单标签


@dataclass
class FallbackGeneratorConfig:
    """备用信号生成器配置"""
    max_history: int = 30  # 信号历史容量
    trend_weight: float = 1.5  # 趋势评分权重
    volume_weight: float = 0.5  # 成交量评分权重
    buy_threshold: float = 2.0  # 买入信号总分阈值
    sell_threshold: float = -2.0  # 卖出信号总分阈值
    stop_loss_pct: float = 0.02  # 默认止损百分比 (2%)
    take_profit_pct: float = 0.04  # 默认止盈百分比 (4%)
    high_confidence_threshold: float = 3.0  # 高信心度阈值
    medium_confidence_threshold: float = 1.0  # 中信心度阈值


@dataclass
class EngineConfig:
    """交易引擎配置"""
    signal_history_max: int = 30  # 引擎信号历史容量
    signal_context_count: int = 3  # 提供给AI的历史信号数


@dataclass
class SchedulerConfig:
    """定时调度配置"""
    default_interval_seconds: int = 900  # 默认执行间隔(秒) - 15分钟
    timeframe_intervals: Optional[Dict[str, int]] = None  # 时间周期到秒数的映射
    
    def __post_init__(self):
        if self.timeframe_intervals is None:
            self.timeframe_intervals = {
                '1m': 60,
                '5m': 300,
                '15m': 900,
                '30m': 1800,
                '1h': 3600,
                '4h': 14400
            }


class Config:
    """主配置类"""

    def __init__(self):
        self.trading = self._load_trading_config()
        self.indicators = self._load_indicator_config()
        self.ai = self._load_ai_config()
        self.position = self._load_position_config()
        self.daily_limit = self._load_daily_limit_config()
        self.sentiment = self._load_sentiment_config()
        self.frequency_guard = self._load_frequency_guard_config()
        self.order_executor = self._load_order_executor_config()
        self.fallback_generator = self._load_fallback_generator_config()
        self.engine = self._load_engine_config()
        self.scheduler = self._load_scheduler_config()
        self.api_keys = self._load_api_keys()

    def _load_trading_config(self) -> TradingConfig:
        """加载交易配置"""
        return TradingConfig(
            symbol=os.getenv('TRADE_SYMBOL', 'BTC/USDT:USDT'),
            leverage=int(os.getenv('TRADE_LEVERAGE', '10')),
            timeframe=os.getenv('TRADE_TIMEFRAME', '15m'),
            test_mode=os.getenv('TRADE_TEST_MODE', 'true').lower() == 'true',
            data_points=int(os.getenv('TRADE_DATA_POINTS', '96')),
            default_exchange=os.getenv('DEFAULT_EXCHANGE', 'auto')
        )

    def _load_indicator_config(self) -> IndicatorConfig:
        """加载技术指标配置"""
        return IndicatorConfig(
            min_data_points=int(os.getenv('INDICATOR_MIN_DATA_POINTS', '20')),
            rsi_neutral=float(os.getenv('INDICATOR_RSI_NEUTRAL', '50.0')),
            rsi_overbought=float(os.getenv('INDICATOR_RSI_OVERBOUGHT', '70.0')),
            rsi_oversold=float(os.getenv('INDICATOR_RSI_OVERSOLD', '30.0')),
            bb_overbought=float(os.getenv('INDICATOR_BB_OVERBOUGHT', '0.8')),
            bb_oversold=float(os.getenv('INDICATOR_BB_OVERSOLD', '0.2')),
            bb_neutral=float(os.getenv('INDICATOR_BB_NEUTRAL', '0.5')),
            volume_high_threshold=float(os.getenv('VOLUME_HIGH_THRESHOLD', '1.5')),
            volume_low_threshold=float(os.getenv('VOLUME_LOW_THRESHOLD', '0.5')),
            support_resistance_default_pct=float(os.getenv('SUPPORT_RESISTANCE_DEFAULT_PCT', '0.05')),
            trend_strong_up_threshold=int(os.getenv('TREND_STRONG_UP_THRESHOLD', '4')),
            trend_up_threshold=int(os.getenv('TREND_UP_THRESHOLD', '2')),
            trend_down_threshold=int(os.getenv('TREND_DOWN_THRESHOLD', '-2')),
            trend_strong_down_threshold=int(os.getenv('TREND_STRONG_DOWN_THRESHOLD', '-4'))
        )

    def _load_ai_config(self) -> AIConfig:
        """加载AI配置"""
        return AIConfig(
            api_key=os.getenv('AI_API_KEY', ''),
            base_url=os.getenv('AI_BASE_URL', 'https://api.deepseek.com'),
            model=os.getenv('AI_MODEL', 'deepseek-chat'),
            temperature=float(os.getenv('AI_TEMPERATURE', '0.1')),
            max_retries=int(os.getenv('AI_MAX_RETRIES', '2')),
            timeout=int(os.getenv('AI_TIMEOUT', '10')),
            retry_backoff_base=int(os.getenv('AI_RETRY_BACKOFF_BASE', '2')),
            retry_max_wait=int(os.getenv('AI_RETRY_MAX_WAIT', '10')),
            kline_display_count=int(os.getenv('AI_KLINE_DISPLAY_COUNT', '5')),
            signal_history_count=int(os.getenv('AI_SIGNAL_HISTORY_COUNT', '3'))
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
            trend_strength_multiplier=float(os.getenv('POSITION_TREND_MULTIPLIER', '1.2')),
            fixed_contracts=float(os.getenv('POSITION_FIXED_CONTRACTS', '0.1')),
            rsi_extreme_high=float(os.getenv('POSITION_RSI_EXTREME_HIGH', '75.0')),
            rsi_extreme_low=float(os.getenv('POSITION_RSI_EXTREME_LOW', '25.0')),
            rsi_extreme_multiplier=float(os.getenv('POSITION_RSI_EXTREME_MULTIPLIER', '0.7')),
            add_position_multiplier=float(os.getenv('POSITION_ADD_MULTIPLIER', '1.2')),
            max_loss_pct=float(os.getenv('RISK_MAX_LOSS_PCT', '5.0')),
            min_reward_ratio=float(os.getenv('RISK_MIN_REWARD_RATIO', '1.0')),
            default_stop_loss_pct=float(os.getenv('DEFAULT_STOP_LOSS_PCT', '0.02')),
            default_take_profit_pct=float(os.getenv('DEFAULT_TAKE_PROFIT_PCT', '0.02'))
        )

    def _load_daily_limit_config(self) -> DailyLimitConfig:
        """加载日投入限额配置"""
        return DailyLimitConfig(
            enable=os.getenv('DAILY_LIMIT_ENABLE', 'true').lower() == 'true',
            daily_limit_usdt=float(os.getenv('DAILY_LIMIT_USDT', '1000')),
            reset_hour=int(os.getenv('DAILY_LIMIT_RESET_HOUR', '0')),
            reset_timezone=os.getenv('DAILY_LIMIT_TIMEZONE', 'Asia/Shanghai'),
            max_total_exposure=float(os.getenv('DAILY_LIMIT_MAX_EXPOSURE', '50')),
            min_reserve_balance=float(os.getenv('DAILY_LIMIT_MIN_RESERVE', '100')),
            database_path=os.getenv('DAILY_LIMIT_DB_PATH', 'data/daily_limits.db'),
            warning_threshold=float(os.getenv('DAILY_LIMIT_WARNING_THRESHOLD', '0.8'))
        )

    def _load_sentiment_config(self) -> SentimentConfig:
        """加载情绪配置"""
        return SentimentConfig(
            enable=os.getenv('SENTIMENT_ENABLE', 'true').lower() == 'true',
            api_key=os.getenv('CRYPTORACLE_API_KEY'),
            cache_ttl=int(os.getenv('SENTIMENT_CACHE_TTL', '900'))
        )

    def _load_frequency_guard_config(self) -> FrequencyGuardConfig:
        """加载防频繁交易配置"""
        return FrequencyGuardConfig(
            min_interval_minutes=int(os.getenv('FREQUENCY_MIN_INTERVAL_MINUTES', '15')),
            max_history=int(os.getenv('FREQUENCY_MAX_HISTORY', '50')),
            consecutive_limit=int(os.getenv('FREQUENCY_CONSECUTIVE_LIMIT', '3')),
            hold_confirm_periods=int(os.getenv('FREQUENCY_HOLD_CONFIRM_PERIODS', '2')),
            reversal_window=int(os.getenv('FREQUENCY_REVERSAL_WINDOW', '10')),
            max_reversals=int(os.getenv('FREQUENCY_MAX_REVERSALS', '4'))
        )

    def _load_order_executor_config(self) -> OrderExecutorConfig:
        """加载订单执行配置"""
        return OrderExecutorConfig(
            max_history=int(os.getenv('ORDER_MAX_HISTORY', '100')),
            wait_seconds=int(os.getenv('ORDER_WAIT_SECONDS', '2')),
            order_tag_open=os.getenv('ORDER_TAG_OPEN', 'deepseek_bot'),
            order_tag_close=os.getenv('ORDER_TAG_CLOSE', 'deepseek_bot_close')
        )

    def _load_fallback_generator_config(self) -> FallbackGeneratorConfig:
        """加载备用信号生成器配置"""
        return FallbackGeneratorConfig(
            max_history=int(os.getenv('FALLBACK_MAX_HISTORY', '30')),
            trend_weight=float(os.getenv('FALLBACK_TREND_WEIGHT', '1.5')),
            volume_weight=float(os.getenv('FALLBACK_VOLUME_WEIGHT', '0.5')),
            buy_threshold=float(os.getenv('FALLBACK_BUY_THRESHOLD', '2.0')),
            sell_threshold=float(os.getenv('FALLBACK_SELL_THRESHOLD', '-2.0')),
            stop_loss_pct=float(os.getenv('FALLBACK_STOP_LOSS_PCT', '0.02')),
            take_profit_pct=float(os.getenv('FALLBACK_TAKE_PROFIT_PCT', '0.04')),
            high_confidence_threshold=float(os.getenv('FALLBACK_HIGH_CONFIDENCE_THRESHOLD', '3.0')),
            medium_confidence_threshold=float(os.getenv('FALLBACK_MEDIUM_CONFIDENCE_THRESHOLD', '1.0'))
        )

    def _load_engine_config(self) -> EngineConfig:
        """加载交易引擎配置"""
        return EngineConfig(
            signal_history_max=int(os.getenv('ENGINE_SIGNAL_HISTORY_MAX', '30')),
            signal_context_count=int(os.getenv('ENGINE_SIGNAL_CONTEXT_COUNT', '3'))
        )

    def _load_scheduler_config(self) -> SchedulerConfig:
        """加载定时调度配置"""
        return SchedulerConfig(
            default_interval_seconds=int(os.getenv('SCHEDULER_DEFAULT_INTERVAL_SECONDS', '900'))
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

        # 检查日投入限额配置
        if self.daily_limit.enable:
            if self.daily_limit.daily_limit_usdt < 50:
                warnings.append(f"日投入限额较小: {self.daily_limit.daily_limit_usdt} USDT，建议不少于50 USDT")

            if self.daily_limit.daily_limit_usdt > 100000:
                warnings.append(f"日投入限额很大: {self.daily_limit.daily_limit_usdt} USDT，请确认风险承受能力")

            if self.daily_limit.reset_hour < 0 or self.daily_limit.reset_hour > 23:
                errors.append(f"重置时间不合理: {self.daily_limit.reset_hour}，应在0-23之间")

            if self.daily_limit.max_total_exposure < 10 or self.daily_limit.max_total_exposure > 100:
                errors.append(f"最大总敞口比例不合理: {self.daily_limit.max_total_exposure}%，应在10-100%之间")

            if self.daily_limit.min_reserve_balance < 0:
                errors.append(f"最小保留余额不能为负数: {self.daily_limit.min_reserve_balance} USDT")

            if self.daily_limit.warning_threshold <= 0 or self.daily_limit.warning_threshold > 1:
                errors.append(f"警告阈值不合理: {self.daily_limit.warning_threshold}，应在0-1之间")

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