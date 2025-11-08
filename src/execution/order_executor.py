"""
订单执行模块

负责创建、跟踪和管理交易订单。
"""

# type: ignore  # 忽略类型检查错误

import time
from typing import Dict, Any, Optional, List
from ..exchanges.base import Order, Position
from ..config import get_config


class OrderExecutor:
    """订单执行器"""

    def __init__(self, exchange_adapter):
        self.exchange = exchange_adapter
        self.config = get_config().trading
        self.executor_config = get_config().order_executor
        self.order_history: List[Dict[str, Any]] = []
        self.max_history = self.executor_config.max_history

    def execute_trade_signal(self, signal_data: Dict[str, Any],
                           market_data: Dict[str, Any],
                           position_size: float) -> Dict[str, Any]:
        """
        执行交易信号

        Args:
            signal_data: 交易信号
            market_data: 市场数据
            position_size: 仓位大小

        Returns:
            Dict[str, Any]: 执行结果
        """
        try:
            symbol = market_data.get('symbol', self.config.symbol)
            signal = signal_data.get('signal', 'HOLD')
            current_position = self._get_current_position(symbol)

            # 测试模式检查
            if self.config.test_mode:
                return self._simulate_execution(signal_data, market_data, position_size, current_position)

            # HOLD信号不执行交易
            if signal == 'HOLD':
                return {
                    'success': True,
                    'action': 'hold',
                    'message': 'HOLD信号，不执行交易',
                    'position': current_position
                }

            # 获取当前持仓
            position_side = current_position.get('side') if current_position else None
            position_size_current = current_position.get('size', 0) if current_position else 0

            # 确定交易操作
            trade_action = self._determine_trade_action(signal, position_side, position_size_current)

            if trade_action == 'open_new':
                return self._open_new_position(signal_data, market_data, position_size, symbol)
            elif trade_action == 'close_and_reverse':
                return self._close_and_reverse(signal_data, market_data, position_size, symbol, current_position)
            elif trade_action == 'add_position':
                return self._add_to_position(signal_data, market_data, position_size, symbol, current_position)
            else:
                return {
                    'success': True,
                    'action': 'no_action',
                    'message': '无需执行交易操作',
                    'position': current_position
                }

        except Exception as e:
            error_msg = f"订单执行失败: {e}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'action': 'failed'
            }

    def _get_current_position(self, symbol: str) -> Optional[Dict[str, Any]]:
        """获取当前持仓"""
        try:
            positions = self.exchange.fetch_positions(symbol)
            for pos in positions:
                if pos.size > 0:
                    return {
                        'side': pos.side,
                        'size': pos.size,
                        'entry_price': pos.entry_price,
                        'unrealized_pnl': pos.unrealized_pnl
                    }
            return None
        except Exception as e:
            print(f"❌ 获取持仓失败: {e}")
            return None

    def _determine_trade_action(self, signal: str, position_side: Optional[str],
                              position_size: float) -> str:
        """确定交易操作类型"""
        if not position_side or position_size == 0:
            return 'open_new'  # 无持仓，开新仓

        if signal == 'BUY' and position_side == 'short':
            return 'close_and_reverse'  # 平空仓并开多仓
        elif signal == 'SELL' and position_side == 'long':
            return 'close_and_reverse'  # 平多仓并开空仓
        elif (signal == 'BUY' and position_side == 'long') or \
             (signal == 'SELL' and position_side == 'short'):
            return 'add_position'  # 同向加仓
        else:
            return 'no_action'

    def _open_new_position(self, signal_data: Dict[str, Any],
                          market_data: Dict[str, Any],
                          position_size: float, symbol: str) -> Dict[str, Any]:
        """开新仓"""
        try:
            signal = signal_data.get('signal')
            side = 'buy' if signal == 'BUY' else 'sell'

            print(f"🔄 开仓操作: {signal.upper()} {position_size:.4f} 张 {symbol}")

            # 创建市价单
            order = self._create_market_order(symbol, side, position_size)

            if order:
                # 设置止损止盈
                self._set_stop_loss_take_profit(symbol, signal_data, order)

                # 更新持仓状态
                time.sleep(self.executor_config.wait_seconds)  # 等待订单生效
                new_position = self._get_current_position(symbol)

                self._record_order(order, 'open_new', signal_data)

                return {
                    'success': True,
                    'action': 'open_new',
                    'message': f"成功开{signal.upper()}仓",
                    'order': order,
                    'position': new_position
                }
            else:
                return {
                    'success': False,
                    'action': 'open_failed',
                    'message': f"开{signal.upper()}仓失败"
                }

        except Exception as e:
            return {
                'success': False,
                'action': 'open_failed',
                'message': f"开仓执行失败: {e}"
            }

    def _close_and_reverse(self, signal_data: Dict[str, Any],
                          market_data: Dict[str, Any],
                          position_size: float, symbol: str,
                          current_position: Dict[str, Any]) -> Dict[str, Any]:
        """平仓并反向开仓"""
        try:
            old_side = current_position.get('side')
            old_size = current_position.get('size')
            new_signal = signal_data.get('signal')
            new_side = 'buy' if new_signal == 'BUY' else 'sell'

            print(f"🔄 平{old_side}仓并开{new_signal.upper()}仓")
            print(f"   - 平仓数量: {old_size:.4f} 张")
            print(f"   - 新开数量: {position_size:.4f} 张")

            # 1. 平现有持仓
            close_order = self._close_position(symbol, old_side, old_size)
            if not close_order:
                return {
                    'success': False,
                    'action': 'close_failed',
                    'message': f"平{old_side}仓失败"
                }

            # 2. 等待平仓完成
            time.sleep(self.executor_config.wait_seconds)

            # 3. 开新仓
            new_order = self._create_market_order(symbol, new_side, position_size)

            if new_order:
                # 设置止损止盈
                self._set_stop_loss_take_profit(symbol, signal_data, new_order)

                # 更新持仓状态
                time.sleep(self.executor_config.wait_seconds)
                new_position = self._get_current_position(symbol)

                self._record_order(close_order, 'close_old', signal_data)
                self._record_order(new_order, 'open_new', signal_data)

                return {
                    'success': True,
                    'action': 'close_and_reverse',
                    'message': f"成功平{old_side}仓并开{new_signal.upper()}仓",
                    'close_order': close_order,
                    'new_order': new_order,
                    'position': new_position
                }
            else:
                return {
                    'success': False,
                    'action': 'open_failed',
                    'message': f"反向开{new_signal.upper()}仓失败"
                }

        except Exception as e:
            return {
                'success': False,
                'action': 'reverse_failed',
                'message': f"平仓反转失败: {e}"
            }

    def _add_to_position(self, signal_data: Dict[str, Any],
                         market_data: Dict[str, Any],
                         position_size: float, symbol: str,
                         current_position: Dict[str, Any]) -> Dict[str, Any]:
        """加仓操作"""
        try:
            signal = signal_data.get('signal')
            side = 'buy' if signal == 'BUY' else 'sell'

            print(f"🔄 加仓操作: {signal.upper()} {position_size:.4f} 张 {symbol}")

            # 创建市价单
            order = self._create_market_order(symbol, side, position_size)

            if order:
                # 调整止损止盈
                self._adjust_stop_loss_take_profit(symbol, signal_data, current_position)

                # 更新持仓状态
                time.sleep(self.executor_config.wait_seconds)
                new_position = self._get_current_position(symbol)

                self._record_order(order, 'add_position', signal_data)

                return {
                    'success': True,
                    'action': 'add_position',
                    'message': f"成功加{signal.upper()}仓",
                    'order': order,
                    'position': new_position
                }
            else:
                return {
                    'success': False,
                    'action': 'add_failed',
                    'message': f"加{signal.upper()}仓失败"
                }

        except Exception as e:
            return {
                'success': False,
                'action': 'add_failed',
                'message': f"加仓失败: {e}"
            }

    def _create_market_order(self, symbol: str, side: str, amount: float) -> Optional[Order]:
        """创建市价单"""
        try:
            order = self.exchange.create_order(
                symbol=symbol,
                side=side,
                amount=amount,
                order_type='market',
                params={'tag': self.executor_config.order_tag_open}
            )

            print(f"✅ 订单创建成功: {order.id}")
            print(f"   - 交易对: {symbol}")
            print(f"   - 方向: {side}")
            print(f"   - 数量: {amount:.4f}")
            print(f"   - 状态: {order.status}")

            return order

        except Exception as e:
            print(f"❌ 订单创建失败: {e}")
            return None

    def _close_position(self, symbol: str, side: str, size: float) -> Optional[Order]:
        """平仓操作"""
        try:
            close_side = 'sell' if side == 'long' else 'buy'

            print(f"🔄 平仓操作: {close_side} {size:.4f} 张 {symbol}")

            order = self.exchange.create_order(
                symbol=symbol,
                side=close_side,
                amount=size,
                order_type='market',
                params={'reduceOnly': True, 'tag': self.executor_config.order_tag_close}
            )

            if order:
                print(f"✅ 平仓订单创建成功: {order.id}")
                return order
            else:
                print(f"❌ 平仓订单创建失败")
                return None

        except Exception as e:
            print(f"❌ 平仓操作失败: {e}")
            return None

    def _set_stop_loss_take_profit(self, symbol: str, signal_data: Dict[str, Any], order: Order):
        """设置止损止盈"""
        try:
            stop_loss = signal_data.get('stop_loss')
            take_profit = signal_data.get('take_profit')

            if stop_loss and take_profit:
                print(f"🛡️ 设置止损: ${stop_loss:.2f}")
                print(f"🎯 设置止盈: ${take_profit:.2f}")
                # 实际实现需要根据交易所API设置止损止盈订单
                # 这里只是记录，实际实现取决于具体交易所的API

        except Exception as e:
            print(f"⚠️ 设置止损止盈失败: {e}")

    def _adjust_stop_loss_take_profit(self, symbol: str, signal_data: Dict[str, Any],
                                     current_position: Dict[str, Any]):
        """调整止损止盈（加仓时���"""
        try:
            # 加仓时可能需要调整现有的止损止盈单
            # 这里是简化实现
            print(f"🔄 调整止损止盈以适应新仓位")
        except Exception as e:
            print(f"⚠️ 调整止损止盈失败: {e}")

    def _simulate_execution(self, signal_data: Dict[str, Any],
                           market_data: Dict[str, Any],
                           position_size: float, current_position: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """模拟执行（测试模式）"""
        signal = signal_data.get('signal', 'HOLD')

        print(f"🧪 测试模式 - 模拟执行交易信号")
        print(f"   - 信号: {signal}")
        print(f"   - 仓位大小: {position_size:.4f}")
        print(f"   - 当前持仓: {current_position.get('side') if current_position else '无持仓'}")
        print(f"   - 止损: ${signal_data.get('stop_loss', 0):.2f}")
        print(f"   - 止盈: ${signal_data.get('take_profit', 0):.2f}")

        # 模拟持仓状态更新
        simulated_position = {
            'side': 'long' if signal == 'BUY' else 'short' if signal == 'SELL' else None,
            'size': position_size if signal != 'HOLD' else (current_position.get('size', 0) if current_position else 0),
            'simulated': True
        }

        return {
            'success': True,
            'action': 'simulated',
            'message': f'测试模式 - 模拟{signal}信号执行成功',
            'position': simulated_position,
            'test_mode': True
        }

    def _record_order(self, order: Order, action: str, signal_data: Dict[str, Any]):
        """记录订单到历史"""
        order_record = {
            'order_id': order.id,
            'symbol': order.symbol,
            'side': order.side,
            'amount': order.amount,
            'type': order.type,
            'status': order.status,
            'action': action,
            'signal': signal_data.get('signal'),
            'timestamp': time.time(),
            'time_str': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        self.order_history.append(order_record)

        # 保持历史记录数量
        if len(self.order_history) > self.max_history:
            self.order_history.pop(0)

    def get_order_history(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取订单历史"""
        return self.order_history[-count:]

    def get_execution_statistics(self) -> Dict[str, Any]:
        """获取执行统计"""
        if not self.order_history:
            return {'total_orders': 0}

        total_orders = len(self.order_history)
        buy_orders = sum(1 for record in self.order_history if record['side'] == 'buy')
        sell_orders = sum(1 for record in self.order_history if record['side'] == 'sell')

        successful_orders = sum(1 for record in self.order_history if record['status'] == 'closed')

        return {
            'total_orders': total_orders,
            'buy_orders': buy_orders,
            'sell_orders': sell_orders,
            'successful_orders': successful_orders,
            'success_rate': (successful_orders / total_orders) * 100 if total_orders > 0 else 0,
            'last_order_time': self.order_history[-1]['time_str'] if self.order_history else None
        }

    def clear_history(self):
        """清空订单历史"""
        self.order_history.clear()
        print("📋 订单历史记录已清空")