"""
智能仓位管理模块

根据信号信心度和市场趋势动态调整仓位大小。
集成日投入限额控制功能。
"""

from typing import Dict, Any, Optional, Tuple
from ..config import get_config
from ..exchanges.base import Position
from ..utils.daily_limit_manager import DailyLimitManager, TradeRecord


class PositionManager:
    """智能仓位管理器"""

    def __init__(self, exchange_adapter):
        self.config = get_config().position
        self.exchange = exchange_adapter
        self.daily_limit_config = get_config().daily_limit

        # 初始化日投入限额管理器
        if self.daily_limit_config.enable:
            self.daily_limit_manager = DailyLimitManager(self.daily_limit_config)
            print(f"[INFO] 日投入限额已启用: {self.daily_limit_config.daily_limit_usdt} USDT")
            print(f"[INFO] 重置时间: {self.daily_limit_config.reset_hour}:00 ({self.daily_limit_config.reset_timezone})")
        else:
            self.daily_limit_manager = None
            print("[INFO] 日投入限额功能已禁用")

    def calculate_position_size(self, signal_data: Dict[str, Any], market_data: Dict[str, Any],
                              current_position: Optional[Position] = None) -> float:
        """
        计算智能仓位大小

        Args:
            signal_data: 交易信号数据
            market_data: 市场数据
            current_position: 当前持仓

        Returns:
            float: 建议的交易数量（合约张数）
        """
        try:
            # 如果禁用智能仓位，使用固定仓位
            if not self.config.enable_intelligent_position:
                fixed_contracts = 0.1
                print(f"[INFO] 智能仓位已禁用，使用固定仓位: {fixed_contracts} 张")
                return fixed_contracts

            # 1. 获取账户余额
            balance = self.exchange.fetch_balance()
            usdt_balance = balance.get('USDT', {}).get('free', 0)

            if usdt_balance <= 0:
                print("[ERROR] USDT余额不足")
                return 0

            # 2. 基础仓位计算
            base_usdt = self.config.base_usdt_amount
            print(f"[INFO] 可用USDT余额: {usdt_balance:.2f}, 下单基数: {base_usdt}")

            # 3. 根据信心程度调整
            confidence_multiplier = self._get_confidence_multiplier(signal_data.get('confidence', 'MEDIUM'))

            # 4. 根据趋势强度调整
            trend_multiplier = self._get_trend_multiplier(market_data)

            # 5. 根据RSI状态调整（超买超卖区域减仓）
            rsi_multiplier = self._get_rsi_multiplier(market_data)

            # 6. 根据当前持仓状态调整
            position_multiplier = self._get_position_multiplier(signal_data, current_position)

            # 7. 计算建议投入USDT金额
            suggested_usdt = (base_usdt *
                             confidence_multiplier *
                             trend_multiplier *
                             rsi_multiplier *
                             position_multiplier)

            # 8. 风险管理：不超过总资金的指定比例
            max_usdt = usdt_balance * (self.config.max_position_ratio / 100)
            final_usdt = min(suggested_usdt, max_usdt)

            # 9. 日投入限额检查
            if self.daily_limit_manager:
                signal = signal_data.get('signal', 'HOLD')
                can_trade, limit_reason = self.daily_limit_manager.check_trade_limit(final_usdt, signal)

                if not can_trade:
                    print(f"[BLOCKED] {limit_reason}")
                    print("[ERROR] 交易被日投入限额阻止")
                    return 0
                elif "警告" in limit_reason:
                    print(f"[WARNING] {limit_reason}")

            # 10. 检查最小保��余额
            if usdt_balance - final_usdt < self.daily_limit_config.min_reserve_balance:
                available_for_trading = usdt_balance - self.daily_limit_config.min_reserve_balance
                if available_for_trading <= 0:
                    print(f"[ERROR] 需要保留最小余额 {self.daily_limit_config.min_reserve_balance} USDT，无法交易")
                    return 0
                final_usdt = min(final_usdt, available_for_trading)
                print(f"[INFO] 调整后投入: {final_usdt:.2f} USDT (保留最小余额)")

            # 11. 转换为合约张数
            symbol = market_data.get('symbol', 'BTC/USDT:USDT')
            contracts = self.exchange.calculate_position_size(final_usdt, symbol)

            print(f"[INFO] 仓位计算结果:")
            print(f"   - 基础金额: {base_usdt:.2f} USDT")
            print(f"   - 信心倍数: {confidence_multiplier:.2f}")
            print(f"   - 趋势倍数: {trend_multiplier:.2f}")
            print(f"   - RSI倍数: {rsi_multiplier:.2f}")
            print(f"   - 持仓倍数: {position_multiplier:.2f}")
            print(f"   - 建议投入: {suggested_usdt:.2f} USDT")
            print(f"   - 最大允许: {max_usdt:.2f} USDT")
            if self.daily_limit_manager:
                daily_stats = self.daily_limit_manager.get_daily_stats()
                print(f"   - 日限额使用: {daily_stats.get('usage_percentage', 0)*100:.1f}% ({daily_stats.get('total_usdt_invested', 0):.2f}/{self.daily_limit_config.daily_limit_usdt:.2f} USDT)")
            print(f"   - 最终仓位: {contracts:.4f} 张")

            return contracts

        except Exception as e:
            print(f"[ERROR] 仓位计算失败: {e}")
            return 0

    def _get_confidence_multiplier(self, confidence: str) -> float:
        """获取信心度倍数"""
        multipliers = {
            'HIGH': self.config.high_confidence_multiplier,
            'MEDIUM': self.config.medium_confidence_multiplier,
            'LOW': self.config.low_confidence_multiplier
        }
        return multipliers.get(confidence, 1.0)

    def _get_trend_multiplier(self, market_data: Dict[str, Any]) -> float:
        """获取趋势强度倍数"""
        trend_analysis = market_data.get('trend_analysis', {})
        overall_trend = trend_analysis.get('overall', '震荡整理')

        if '强势' in overall_trend:
            return self.config.trend_strength_multiplier
        else:
            return 1.0

    def _get_rsi_multiplier(self, market_data: Dict[str, Any]) -> float:
        """获取RSI调整倍数"""
        technical_data = market_data.get('technical_data', {})
        rsi = technical_data.get('rsi', 50)

        # 超买超卖区域减仓
        if rsi > 75 or rsi < 25:
            return 0.7
        else:
            return 1.0

    def _get_position_multiplier(self, signal_data: Dict[str, Any],
                                current_position: Optional[Position]) -> float:
        """获取持仓状态倍数"""
        if not current_position:
            return 1.0  # 无持仓，正常仓位

        signal = signal_data.get('signal', 'HOLD')
        position_side = current_position.side

        # 如果信号与当前持仓方向一致，可以适当加仓
        if (signal == 'BUY' and position_side == 'long') or \
           (signal == 'SELL' and position_side == 'short'):
            return 1.2  # 加仓倍数

        # 如果信号与当前持仓方向相反，需要平仓后再开新仓
        return 1.0

    def should_execute_trade(self, signal_data: Dict[str, Any],
                           current_position: Optional[Position]) -> bool:
        """
        判断是否应该执行交易

        Args:
            signal_data: 交易信号
            current_position: 当前持仓

        Returns:
            bool: 是否执行交易
        """
        signal = signal_data.get('signal', 'HOLD')
        confidence = signal_data.get('confidence', 'LOW')

        # HOLD信号不执行交易
        if signal == 'HOLD':
            return False

        # LOW信心度的信号需要谨慎考虑
        if confidence == 'LOW':
            if current_position:
                # 如果有持仓，LOW信心度信号不执行
                print(f"[WARNING] 信心度过低({confidence})，保持现有持仓")
                return False
            else:
                # 如果无持仓，可以考虑小额建仓
                print(f"[WARNING] 信心度过低({confidence})，将使用最小仓位")

        return True

    def calculate_risk_metrics(self, signal_data: Dict[str, Any],
                             market_data: Dict[str, Any],
                             position_size: float) -> Dict[str, Any]:
        """
        计算风险指标

        Args:
            signal_data: 交易信号
            market_data: 市场数据
            position_size: 仓位大小

        Returns:
            Dict[str, Any]: 风险指标
        """
        try:
            current_price = market_data.get('price', 0)
            stop_loss = signal_data.get('stop_loss', current_price * 0.98)
            take_profit = signal_data.get('take_profit', current_price * 1.02)

            # 计算风险收益比
            risk_per_unit = abs(current_price - stop_loss)
            reward_per_unit = abs(take_profit - current_price)
            risk_reward_ratio = reward_per_unit / risk_per_unit if risk_per_unit > 0 else 1.0

            # 计算潜在盈亏
            balance = self.exchange.fetch_balance()
            usdt_balance = balance.get('USDT', {}).get('free', 0)

            position_value = position_size * current_price
            position_ratio = (position_value / usdt_balance) * 100 if usdt_balance > 0 else 0

            potential_loss = position_size * risk_per_unit
            potential_profit = position_size * reward_per_unit

            loss_percentage = (potential_loss / usdt_balance) * 100 if usdt_balance > 0 else 0
            profit_percentage = (potential_profit / usdt_balance) * 100 if usdt_balance > 0 else 0

            return {
                'risk_reward_ratio': risk_reward_ratio,
                'position_ratio': position_ratio,
                'potential_loss': potential_loss,
                'potential_profit': potential_profit,
                'loss_percentage': loss_percentage,
                'profit_percentage': profit_percentage,
                'acceptable_risk': loss_percentage <= 5.0,  # 单次损失不超过5%
                'acceptable_position': position_ratio <= self.config.max_position_ratio
            }

        except Exception as e:
            print(f"[ERROR] 风险指标计算失败: {e}")
            return {}

    def record_trade(self, symbol: str, side: str, amount: float, price: float,
                    status: str = "completed", strategy: str = "", confidence: str = "MEDIUM",
                    fee: float = 0.0, notes: str = "") -> bool:
        """
        记录交易到日投入限额管理器

        Args:
            symbol: 交易对
            side: 交易方向 (BUY/SELL)
            amount: 交易数量
            price: 交易价格
            status: 交易状态
            strategy: 策略标识
            confidence: 信心度
            fee: 手续费
            notes: 备注

        Returns:
            bool: 记录是否成功
        """
        if not self.daily_limit_manager:
            return True  # 如果未启用限额管理，直接返回成功

        try:
            usdt_value = amount * price
            trade_record = TradeRecord(
                symbol=symbol,
                side=side,
                amount=amount,
                price=price,
                usdt_value=usdt_value,
                fee=fee,
                status=status,
                strategy=strategy,
                confidence=confidence,
                notes=notes
            )

            success = self.daily_limit_manager.record_trade(trade_record)
            if success:
                print(f"[INFO] 交易已记录: {side} {amount:.4f} {symbol} @ {price:.2f} = {usdt_value:.2f} USDT")

                # 显示更新后的日限额状态
                daily_stats = self.daily_limit_manager.get_daily_stats()
                print(f"[INFO] 今日投入: {daily_stats.get('total_usdt_invested', 0):.2f}/{self.daily_limit_config.daily_limit_usdt:.2f} USDT ({daily_stats.get('usage_percentage', 0)*100:.1f}%)")

            return success

        except Exception as e:
            print(f"[ERROR] 记录交易失败: {e}")
            return False

    def get_daily_limit_status(self) -> Dict[str, Any]:
        """
        获取当前日投入限额状态

        Returns:
            Dict[str, Any]: 限额状态信息
        """
        if not self.daily_limit_manager:
            return {"enabled": False, "message": "日投入限额功能已禁用"}

        try:
            daily_stats = self.daily_limit_manager.get_daily_stats()
            return {
                "enabled": True,
                "daily_limit": self.daily_limit_config.daily_limit_usdt,
                "current_invested": daily_stats.get('total_usdt_invested', 0),
                "remaining": daily_stats.get('remaining_limit', 0),
                "usage_percentage": daily_stats.get('usage_percentage', 0),
                "is_warning": daily_stats.get('is_warning_threshold', False),
                "reset_time": self.daily_limit_manager.get_next_reset_time(),
                "trade_count": daily_stats.get('trade_count', 0),
                "successful_trades": daily_stats.get('successful_trades', 0)
            }

        except Exception as e:
            print(f"[ERROR] 获取日限额状态失败: {e}")
            return {"enabled": True, "error": str(e)}

    def print_daily_limit_summary(self):
        """打印日投入限额汇总信息"""
        if not self.daily_limit_manager:
            print("[INFO] 日投入限额���能已禁用")
            return

        try:
            status = self.get_daily_limit_status()
            if "error" in status:
                print(f"[ERROR] 获取限额状态失败: {status['error']}")
                return

            print("\n" + "="*50)
            print("[INFO] 日投入限额状态汇总")
            print("="*50)
            print(f"[INFO] 日限额: {status['daily_limit']:.2f} USDT")
            print(f"[INFO] 已投入: {status['current_invested']:.2f} USDT")
            print(f"[INFO] 剩余: {status['remaining']:.2f} USDT")
            print(f"[INFO] 使用率: {status['usage_percentage']*100:.1f}%")

            if status['is_warning']:
                print("[WARNING] 警告：已接近日投入限额！")

            print(f"[INFO] 重置时间: {status['reset_time'].strftime('%Y-%m-%d %H:%M:%S')} UTC")
            print(f"📋 今日交易: {status['trade_count']} 笔 (成功: {status['successful_trades']} 笔)")
            print("="*50)

        except Exception as e:
            print(f"[ERROR] 打印限额汇总失败: {e}")

    def validate_position_risk(self, signal_data: Dict[str, Any],
                             market_data: Dict[str, Any],
                             position_size: float) -> Dict[str, Any]:
        """
        验证仓位风险

        Args:
            signal_data: 交易信号
            market_data: 市场数据
            position_size: 仓位大小

        Returns:
            Dict[str, Any]: 验证结果
        """
        risk_metrics = self.calculate_risk_metrics(signal_data, market_data, position_size)
        if not risk_metrics:
            return {
                'valid': False,
                'errors': ['无法计算风险指标'],
                'warnings': []
            }

        errors = []
        warnings = []

        # 检查风险收益比
        if risk_metrics.get('risk_reward_ratio', 0) < 1.0:
            warnings.append("风险收益比过低，建议重新评估")

        # 检查仓位比例
        if not risk_metrics.get('acceptable_position', False):
            errors.append(f"仓位比例过大: {risk_metrics.get('position_ratio', 0):.1f}%")

        # 检查潜在损失
        if not risk_metrics.get('acceptable_risk', False):
            errors.append(f"潜在损失过大: {risk_metrics.get('loss_percentage', 0):.1f}%")

        # 检查止损止盈合理性
        current_price = market_data.get('price', 0)
        stop_loss = signal_data.get('stop_loss', current_price)
        take_profit = signal_data.get('take_profit', current_price)
        signal = signal_data.get('signal', 'HOLD')

        if signal == 'BUY' and stop_loss >= take_profit:
            errors.append("BUY信号的止损价不应高于止盈价")
        elif signal == 'SELL' and stop_loss <= take_profit:
            errors.append("SELL信号的止损价不应低于止盈价")

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'risk_metrics': risk_metrics
        }