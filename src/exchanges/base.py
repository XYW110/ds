"""
交易所适配器基类

定义统一的交易所接口，支持多种交易所的统一操作。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class OHLCV:
    """K线数据结构"""
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class Position:
    """持仓信息结构"""
    symbol: str
    side: str  # 'long', 'short', or None
    size: float
    entry_price: float
    unrealized_pnl: float
    leverage: float
    margin_mode: str  # 'cross', 'isolated'


@dataclass
class Order:
    """订单信息结构"""
    id: str
    symbol: str
    side: str  # 'buy', 'sell'
    amount: float
    price: Optional[float]
    status: str  # 'open', 'closed', 'canceled'
    type: str  # 'market', 'limit', 'stop'


@dataclass
class MarketInfo:
    """市场信息结构"""
    symbol: str
    base: str
    quote: str
    active: bool
    contract_size: float
    min_amount: float
    max_amount: float
    price_precision: int
    amount_precision: int


class ExchangeAdapter(ABC):
    """交易所适配器抽象基类"""

    def __init__(self, api_key: str, secret: str, password: Optional[str] = None, **kwargs):
        self.api_key = api_key
        self.secret = secret
        self.password = password
        self.extra_params = kwargs
        self._exchange = None
        self._initialized = False

    @abstractmethod
    def initialize(self) -> bool:
        """初始化交易所连接"""
        pass

    @abstractmethod
    def load_markets(self) -> Dict[str, MarketInfo]:
        """加载市场信息"""
        pass

    @abstractmethod
    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> List[OHLCV]:
        """获取K线数据"""
        pass

    @abstractmethod
    def fetch_positions(self, symbol: Optional[str] = None) -> List[Position]:
        """获取持仓信息"""
        pass

    @abstractmethod
    def create_order(self, symbol: str, side: str, amount: float,
                     order_type: str = 'market', price: Optional[float] = None,
                     params: Optional[Dict[str, Any]] = None) -> Order:
        """创建订单"""
        pass

    @abstractmethod
    def cancel_order(self, order_id: str, symbol: str) -> bool:
        """取消订单"""
        pass

    @abstractmethod
    def fetch_order(self, order_id: str, symbol: str) -> Order:
        """获取订单状态"""
        pass

    @abstractmethod
    def set_leverage(self, leverage: int, symbol: str, params: Optional[Dict[str, Any]] = None):
        """设置杠杆倍数"""
        pass

    @abstractmethod
    def set_position_mode(self, hedged: bool, symbol: str):
        """设置持仓模式 (双向/单向)"""
        pass

    @abstractmethod
    def fetch_balance(self) -> Dict[str, Dict[str, float]]:
        """获取账户余额"""
        pass

    @abstractmethod
    def fetch_ticker(self, symbol: str) -> Dict[str, float]:
        """获取市场行情"""
        pass

    def get_market_info(self, symbol: str) -> Optional[MarketInfo]:
        """获取单个市场信息"""
        markets = self.load_markets()
        return markets.get(symbol)

    def get_current_price(self, symbol: str) -> float:
        """获取当前价格"""
        ticker = self.fetch_ticker(symbol)
        return ticker.get('last', 0.0)

    def is_market_open(self, symbol: str) -> bool:
        """检查市场是否开放"""
        market_info = self.get_market_info(symbol)
        return market_info.active if market_info else False

    def calculate_position_size(self, usdt_amount: float, symbol: str) -> float:
        """根据USDT金额计算交易数量"""
        market_info = self.get_market_info(symbol)
        if not market_info:
            raise ValueError(f"市场信息不存在: {symbol}")

        current_price = self.get_current_price(symbol)
        if current_price <= 0:
            raise ValueError(f"无效的市场价格: {current_price}")

        # 计算基础数量
        base_amount = usdt_amount / current_price

        # 应用合约乘数
        if market_info.contract_size != 1:
            base_amount /= market_info.contract_size

        # 应用最小精度
        precision = market_info.amount_precision
        rounded_amount = round(base_amount, precision)

        # 检查最小和最大限制
        if rounded_amount < market_info.min_amount:
            raise ValueError(f"计算数量小于最小限制: {rounded_amount} < {market_info.min_amount}")

        if market_info.max_amount > 0 and rounded_amount > market_info.max_amount:
            rounded_amount = market_info.max_amount

        return rounded_amount

    def validate_order_params(self, symbol: str, amount: float,
                            price: Optional[float] = None) -> Dict[str, Any]:
        """验证订单参数"""
        market_info = self.get_market_info(symbol)
        if not market_info:
            raise ValueError(f"市场信息不存在: {symbol}")

        errors = []

        # 验证数量
        if amount <= 0:
            errors.append("订单数量必须大于0")
        elif amount < market_info.min_amount:
            errors.append(f"订单数量小于最小限制: {amount} < {market_info.min_amount}")

        if market_info.max_amount > 0 and amount > market_info.max_amount:
            errors.append(f"订单数量超过最大限制: {amount} > {market_info.max_amount}")

        # 验证价格
        if price is not None and price <= 0:
            errors.append("订单价格必须大于0")

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'suggestions': self._get_order_suggestions(symbol, amount, price)
        }

    def _get_order_suggestions(self, symbol: str, amount: float,
                              price: Optional[float] = None) -> List[str]:
        """获取订单建议"""
        suggestions = []
        market_info = self.get_market_info(symbol)

        if not market_info:
            return suggestions

        if amount < market_info.min_amount:
            suggestions.append(f"建议最小数量: {market_info.min_amount}")

        if market_info.max_amount > 0 and amount > market_info.max_amount:
            suggestions.append(f"建议最大数量: {market_info.max_amount}")

        return suggestions

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(initialized={self._initialized})"