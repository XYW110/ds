"""
智能仓位管理模块

根据信号信心度和市场趋势动态调整仓位大小。
"""

from typing import Dict, Any, Optional
from ..config import get_config
from ..exchanges.base import Position


class PositionManager:
    """智能仓位管理器"""

    def __init__(self, exchange_adapter):
        self.config = get_config().position
        self.exchange = exchange_adapter

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
                print(f"🔧 智能仓位已禁用，使用固定仓位: {fixed_contracts} 张")
                return fixed_contracts

            # 1. 获取账户余额
            balance = self.exchange.fetch_balance()
            usdt_balance = balance.get('USDT', {}).get('free', 0)

            if usdt_balance <= 0:
                print("❌ USDT余额不足")
                return 0

            # 2. 基础仓位计算
            base_usdt = self.config.base_usdt_amount
            print(f"💰 可用USDT余额: {usdt_balance:.2f}, 下单基数: {base_usdt}")

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

            # 9. 转换为合约张数
            symbol = market_data.get('symbol', 'BTC/USDT:USDT')
            contracts = self.exchange.calculate_position_size(final_usdt, symbol)

            print(f"📊 仓位计算结果:")
            print(f"   - 基础金额: {base_usdt:.2f} USDT")
            print(f"   - 信心倍数: {confidence_multiplier:.2f}")
            print(f"   - 趋势倍数: {trend_multiplier:.2f}")
            print(f"   - RSI倍数: {rsi_multiplier:.2f}")
            print(f"   - 持仓倍数: {position_multiplier:.2f}")
            print(f"   - 建议投入: {suggested_usdt:.2f} USDT")
            print(f"   - 最大允许: {max_usdt:.2f} USDT")
            print(f"   - 最终仓位: {contracts:.4f} 张")

            return contracts

        except Exception as e:
            print(f"❌ 仓位计算失败: {e}")
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
                print(f"⚠️ 信心度过低({confidence})，保持现有持仓")
                return False
            else:
                # 如果无持仓，可以考虑小额建仓
                print(f"⚠️ 信心度过低({confidence})，将使用最小仓位")

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
            print(f"❌ 风险指标计算失败: {e}")
            return {}

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