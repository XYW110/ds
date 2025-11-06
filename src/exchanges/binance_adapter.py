"""
Binance交易所适配器

实现Binance现货和期货交易的适配器。
"""

# type: ignore  # 忽略类型检查错误

import ccxt
from typing import Dict, Any, List, Optional
from ccxt.base.types import ConstructorArgs
from typing import cast

from .base import ExchangeAdapter, OHLCV, Position, Order, MarketInfo


class BinanceAdapter(ExchangeAdapter):
    """Binance交易所适配器"""

    def __init__(self, api_key: str, secret: str, password: Optional[str] = None, **kwargs):
        super().__init__(api_key, secret, password, **kwargs)
        self.test_mode = kwargs.get('test_mode', False)
        self.trade_type = kwargs.get('trade_type', 'future')  # 'spot' or 'future'
        self._exchange = None

    def initialize(self) -> bool:
        """初始化Binance交易所连接"""
        try:
            # 配置Binance参数
            config: ConstructorArgs = {
                'options': {
                    'defaultType': self.trade_type,
                    'test': self.test_mode,
                },
                'apiKey': self.api_key,
                'secret': self.secret,
                **self.extra_params
            }

            # 创建交易所实例
            if self.trade_type == 'future':
                self._exchange = ccxt.binance(cast(ConstructorArgs, config))
            else:
                self._exchange = ccxt.binance(cast(ConstructorArgs, config))

            # 加载市场信息
            self._exchange.load_markets()

            self._initialized = True
            return True

        except Exception as e:
            print(f"Binance初始化失败: {e}")
            return False

    def load_markets(self) -> Dict[str, MarketInfo]:
        """加载市场信息"""
        if not self._initialized:
            self.initialize()

        markets = {}
        for symbol, market in self._exchange.markets.items():
            # 根据交易类型筛选市场
            if self.trade_type == 'future':
                if market.get('type') == 'future':
                    markets[symbol] = MarketInfo(
                        symbol=symbol,
                        base=market.get('base', ''),
                        quote=market.get('quote', ''),
                        active=market.get('active', False),
                        contract_size=float(market.get('contractSize', 1)),
                        min_amount=float(market.get('limits', {}).get('amount', {}).get('min', 0)),
                        max_amount=float(market.get('limits', {}).get('amount', {}).get('max', 0)),
                        price_precision=market.get('precision', {}).get('price', 0),
                        amount_precision=market.get('precision', {}).get('amount', 0)
                    )
            else:
                if market.get('type') == 'spot':
                    markets[symbol] = MarketInfo(
                        symbol=symbol,
                        base=market.get('base', ''),
                        quote=market.get('quote', ''),
                        active=market.get('active', False),
                        contract_size=float(market.get('contractSize', 1)),
                        min_amount=float(market.get('limits', {}).get('amount', {}).get('min', 0)),
                        max_amount=float(market.get('limits', {}).get('amount', {}).get('max', 0)),
                        price_precision=market.get('precision', {}).get('price', 0),
                        amount_precision=market.get('precision', {}).get('amount', 0)
                    )

        return markets

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> List[OHLCV]:
        """获取K线数据"""
        if not self._initialized:
            self.initialize()

        try:
            ohlcv = self._exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

            result = []
            for item in ohlcv:
                result.append(OHLCV(
                    timestamp=item[0],
                    open=float(item[1]),
                    high=float(item[2]),
                    low=float(item[3]),
                    close=float(item[4]),
                    volume=float(item[5])
                ))

            return result

        except Exception as e:
            print(f"获取K线数据失败: {e}")
            return []

    def fetch_positions(self, symbol: Optional[str] = None) -> List[Position]:
        """获取持仓信息"""
        if not self._initialized:
            self.initialize()

        try:
            if self.trade_type == 'future':
                symbols = [symbol] if symbol else None
                positions_data = self._exchange.fetch_positions(symbols)

                positions = []
                for pos in positions_data:
                    contracts = float(pos.get('contracts', 0))
                    if contracts > 0:  # 只返回有持仓的
                        positions.append(Position(
                            symbol=pos['symbol'],
                            side=pos['side'],
                            size=contracts,
                            entry_price=float(pos.get('entryPrice', 0)),
                            unrealized_pnl=float(pos.get('unrealizedPnl', 0)),
                            leverage=float(pos.get('leverage', 1)),
                            margin_mode=pos.get('mgnMode', 'cross')
                        ))

                return positions
            else:
                # 现货交易没有持仓概念，返回空列表
                return []

        except Exception as e:
            print(f"获取持仓信息失败: {e}")
            return []

    def create_order(self, symbol: str, side: str, amount: float,
                     order_type: str = 'market', price: Optional[float] = None,
                     params: Optional[Dict[str, Any]] = None) -> Order:
        """创建订单"""
        if not self._initialized:
            self.initialize()

        try:
            # 参数验证
            params = params or {}

            # 创建订单
            result = self._exchange.create_order(
                symbol, order_type, side, amount, price, params
            )

            return Order(
                id=result['id'],
                symbol=result['symbol'],
                side=result['side'],
                amount=float(result['amount']),
                price=result.get('price'),
                status=result['status'],
                type=result['type']
            )

        except Exception as e:
            print(f"创建订单失败: {e}")
            raise

    def cancel_order(self, order_id: str, symbol: str) -> bool:
        """取消订单"""
        if not self._initialized:
            self.initialize()

        try:
            self._exchange.cancel_order(order_id, symbol)
            return True
        except Exception as e:
            print(f"取消订单失败: {e}")
            return False

    def fetch_order(self, order_id: str, symbol: str) -> Order:
        """获取订单状态"""
        if not self._initialized:
            self.initialize()

        try:
            result = self._exchange.fetch_order(order_id, symbol)

            return Order(
                id=result['id'],
                symbol=result['symbol'],
                side=result['side'],
                amount=float(result['amount']),
                price=result.get('price'),
                status=result['status'],
                type=result['type']
            )

        except Exception as e:
            print(f"获取订单状态失败: {e}")
            raise

    def set_leverage(self, leverage: int, symbol: str, params: Optional[Dict[str, Any]] = None):
        """设置杠杆倍数"""
        if not self._initialized:
            self.initialize()

        if self.trade_type != 'future':
            print(f"⚠️ 现货交易不支持杠杆设置")
            return

        try:
            # 默认使用全仓模式
            default_params = {'mgnMode': 'cross'}
            if params:
                default_params.update(params)

            self._exchange.set_leverage(leverage, symbol, default_params)
            print(f"✅ Binance设置杠杆: {leverage}x, 模式: {default_params.get('mgnMode')}")

        except Exception as e:
            print(f"设置杠杆失败: {e}")
            raise

    def set_position_mode(self, hedged: bool, symbol: str):
        """设置持仓模式 (双向/单向)"""
        if not self._initialized:
            self.initialize()

        if self.trade_type != 'future':
            print(f"⚠️ 现货交易不支持持仓模式设置")
            return

        try:
            self._exchange.set_position_mode(hedged, symbol)
            mode_text = "双向持仓" if hedged else "单向持仓"
            print(f"✅ Binance设置持仓模式: {mode_text}")

        except Exception as e:
            print(f"设置持仓模式失败 (可能已设置): {e}")

    def fetch_balance(self) -> Dict[str, Dict[str, float]]:
        """获取账户余额"""
        if not self._initialized:
            self.initialize()

        try:
            return self._exchange.fetch_balance()
        except Exception as e:
            print(f"获取账户余额失败: {e}")
            return {}

    def fetch_ticker(self, symbol: str) -> Dict[str, float]:
        """获取市场行情"""
        if not self._initialized:
            self.initialize()

        try:
            return self._exchange.fetch_ticker(symbol)
        except Exception as e:
            print(f"获取市场行情失败: {e}")
            return {}

    def get_current_position(self, symbol: str) -> Optional[Position]:
        """获取当前指定交易对的持仓"""
        if self.trade_type == 'future':
            positions = self.fetch_positions(symbol)
            return positions[0] if positions else None
        else:
            # 现货交易没有持仓概念
            return None

    def setup_for_trading(self, symbol: str, leverage: int = 10) -> bool:
        """设置交易环境"""
        try:
            if self.trade_type == 'future':
                # 1. 设置杠杆
                print("⚙️ 设置杠杆...")
                self.set_leverage(leverage, symbol)

                # 2. 设置持仓模式
                print("🔄 设置单向持仓模式...")
                self.set_position_mode(False, symbol)

                # 3. 验证设置
                print("🔍 验证账户设置...")
                balance = self.fetch_balance()
                usdt_balance = balance.get('USDT', {}).get('free', 0)
                print(f"💰 当前USDT余额: {usdt_balance:.2f}")

                current_pos = self.get_current_position(symbol)
                if current_pos:
                    print(f"📦 当前持仓: {current_pos.side}仓 {current_pos.size}张")
                else:
                    print("📦 当前无持仓")

                print("🎯 期货交易环境配置完成：单向持仓模式")
            else:
                # 现货交易设置
                print("🔍 验证现货账户设置...")
                balance = self.fetch_balance()
                usdt_balance = balance.get('USDT', {}).get('free', 0)
                print(f"💰 当前USDT余额: {usdt_balance:.2f}")
                print("🎯 现货交易环境配置完成")

            return True

        except Exception as e:
            print(f"❌ 交易环境设置失败: {e}")
            return False

    def calculate_position_size(self, usdt_amount: float, symbol: str) -> float:
        """根据USDT金额计算交易数量"""
        market_info = self.get_market_info(symbol)
        if not market_info:
            raise ValueError(f"市场信息不存在: {symbol}")

        current_price = self.get_current_price(symbol)
        if current_price <= 0:
            raise ValueError(f"无效的市场价格: {current_price}")

        # 对于现货，直接计算基础数量
        if self.trade_type == 'spot':
            base_amount = usdt_amount / current_price
        else:
            # 对于期货，需要考虑合约规格
            base_amount = usdt_amount / current_price
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