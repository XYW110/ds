"""
防频繁交易保护模块

防止过于频繁的交易操作，保护资金安全。
"""

import time
from typing import Dict, Any, Optional, List
from ..config import get_config


class FrequencyGuard:
    """防频繁交易保护器"""

    def __init__(self, config=None):
        # 使用传入的配置或从全局获取配置
        if config is None:
            config = get_config().frequency_guard

        self.config = config
        self.min_interval_seconds = self.config.min_interval_minutes * 60
        self.signal_history: List[Dict[str, Any]] = []
        self.max_history = self.config.max_history

    def should_allow_trade(self, signal_data: Dict[str, Any],
                         current_position: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        判断是否应该允许交易

        Args:
            signal_data: 当前交易信号
            current_position: 当前持仓

        Returns:
            Dict[str, Any]: 判断结果
        """
        current_signal = signal_data.get('signal', 'HOLD')
        current_timestamp = time.time()

        # 记录当前信号
        self._record_signal(current_signal, current_timestamp)

        # 1. 检查时���间隔
        time_check = self._check_time_interval(current_timestamp)
        if not time_check['allow']:
            return {
                'allow': False,
                'reason': time_check['reason'],
                'type': 'time_protection'
            }

        # 2. 检查连续信号
        signal_check = self._check_consecutive_signals(current_signal, current_position)
        if not signal_check['allow']:
            return {
                'allow': False,
                'reason': signal_check['reason'],
                'type': 'signal_protection'
            }

        # 3. 检查持仓一致性
        position_check = self._check_position_consistency(current_signal, current_position)
        if not position_check['allow']:
            return {
                'allow': False,
                'reason': position_check['reason'],
                'type': 'position_protection'
            }

        # 4. 检查信号反转频率
        reversal_check = self._check_signal_reversal_frequency(current_signal)
        if not reversal_check['allow']:
            return {
                'allow': False,
                'reason': reversal_check['reason'],
                'type': 'reversal_protection'
            }

        return {
            'allow': True,
            'reason': '交易检查通过',
            'type': 'allowed'
        }

    def _record_signal(self, signal: str, timestamp: float):
        """记录信号到历史"""
        signal_record = {
            'signal': signal,
            'timestamp': timestamp,
            'time_str': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        }

        self.signal_history.append(signal_record)

        # 保持历史记录数量
        if len(self.signal_history) > self.max_history:
            self.signal_history.pop(0)

    def _check_time_interval(self, current_timestamp: float) -> Dict[str, Any]:
        """检查时间间隔"""
        if not self.signal_history:
            return {'allow': True, 'reason': '首次交易'}

        # 查找最近一次实际执行的交易信号
        for record in reversed(self.signal_history):
            if record['signal'] in ['BUY', 'SELL']:
                last_trade_time = record['timestamp']
                time_diff = current_timestamp - last_trade_time

                if time_diff < self.min_interval_seconds:
                    remaining_time = self.min_interval_seconds - time_diff
                    remaining_minutes = remaining_time / 60

                    return {
                        'allow': False,
                        'reason': f'距离上次交易时间过短，还需等待{remaining_minutes:.1f}分钟',
                        'remaining_seconds': remaining_time
                    }

                break

        return {'allow': True, 'reason': '时间间隔满足要求'}

    def _check_consecutive_signals(self, current_signal: str,
                                 current_position: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """检查连续信号"""
        if not self.signal_history:
            return {'allow': True, 'reason': '无历史信号'}

        # 查找最近的信号
        recent_signals = [record['signal'] for record in self.signal_history[-5:]]

        # 检查是否是连续的相同信号
        if len(recent_signals) >= self.config.consecutive_limit and recent_signals[-self.config.consecutive_limit:] == [current_signal] * self.config.consecutive_limit:
            return {
                'allow': False,
                'reason': f'连续{self.config.consecutive_limit}次相同的{current_signal}信号，为避免频繁操作暂不执行'
            }

        # 检查HOLD信号后的交易信号
        if recent_signals[-1] == 'HOLD' and current_signal != 'HOLD':
            # HOLD信号后的第一个交易信号需要谨慎
            hold_count = 0
            for signal in reversed(recent_signals):
                if signal == 'HOLD':
                    hold_count += 1
                else:
                    break

            if hold_count < self.config.hold_confirm_periods:
                return {
                    'allow': False,
                    'reason': f'HOLD信号后需要至少{self.config.hold_confirm_periods}个周期的确认才能执行新交易'
                }

        return {'allow': True, 'reason': '连续信号检查通过'}

    def _check_position_consistency(self, current_signal: str,
                                  current_position: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """检查持仓一致性"""
        if not current_position:
            # 无持仓状态，所有信号都可以考虑
            return {'allow': True, 'reason': '无持仓状态'}

        position_side = current_position.get('side', '')
        if not position_side:
            return {'allow': True, 'reason': '持仓方向不明确'}

        # 检查信号与持仓方向的一致性
        if current_signal == 'BUY' and position_side == 'long':
            # 多头持仓且信号为买入 - 可以考虑加仓
            return {
                'allow': True,
                'reason': '多头持仓且信号为买入，可以加仓'
            }

        elif current_signal == 'SELL' and position_side == 'short':
            # 空头持仓且信号为卖出 - 可以考虑加仓
            return {
                'allow': True,
                'reason': '空头持仓且信号为卖出，可以加仓'
            }

        elif current_signal == 'HOLD':
            # HOLD信号总是允许的
            return {
                'allow': True,
                'reason': 'HOLD信号，维持现有持仓'
            }

        else:
            # 信号与持仓方向相反，需要平仓
            return {
                'allow': True,
                'reason': f'信号{current_signal}与持仓{position_side}方向相反，需要平仓',
                'require_close_position': True
            }

    def _check_signal_reversal_frequency(self, current_signal: str) -> Dict[str, Any]:
        """检查信号反转频率"""
        if len(self.signal_history) < self.config.reversal_window:
            return {'allow': True, 'reason': '历史信号不足'}

        # 获取最近的信号
        recent_signals = [record['signal'] for record in self.signal_history[-self.config.reversal_window:]]

        # 计算信号反转次数
        reversals = 0
        for i in range(1, len(recent_signals)):
            if recent_signals[i] != 'HOLD' and recent_signals[i-1] != 'HOLD':
                if recent_signals[i] != recent_signals[i-1]:
                    reversals += 1

        # 如果反转过于频繁，进行保护
        if reversals >= self.config.max_reversals:
            return {
                'allow': False,
                'reason': f'近期信号反转过于频繁({reversals}次)，建议观望一段时间'
            }

        return {'allow': True, 'reason': '信号反转频率正常'}

    def get_trade_statistics(self) -> Dict[str, Any]:
        """获取交易统计信息"""
        if not self.signal_history:
            return {'total_signals': 0}

        total_signals = len(self.signal_history)
        buy_signals = sum(1 for record in self.signal_history if record['signal'] == 'BUY')
        sell_signals = sum(1 for record in self.signal_history if record['signal'] == 'SELL')
        hold_signals = sum(1 for record in self.signal_history if record['signal'] == 'HOLD')

        # 计算交易信号间隔
        trade_signals = [record for record in self.signal_history if record['signal'] in ['BUY', 'SELL']]
        if len(trade_signals) > 1:
            intervals = []
            for i in range(1, len(trade_signals)):
                interval = trade_signals[i]['timestamp'] - trade_signals[i-1]['timestamp']
                intervals.append(interval)

            avg_interval = sum(intervals) / len(intervals) if intervals else 0
            min_interval = min(intervals) if intervals else 0
        else:
            avg_interval = 0
            min_interval = 0

        return {
            'total_signals': total_signals,
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'hold_signals': hold_signals,
            'trade_signals': buy_signals + sell_signals,
            'average_interval_minutes': avg_interval / 60,
            'min_interval_minutes': min_interval / 60,
            'last_signal_time': self.signal_history[-1]['time_str'] if self.signal_history else None
        }

    def clear_history(self):
        """清空历史记录"""
        self.signal_history.clear()
        print("🛡️ 防频繁交易历史记录已清空")

    def get_protection_summary(self) -> str:
        """获取保护机制摘要"""
        return f"""
🛡️ 防频繁交易保护机制
- 最小交易间隔: {self.config.min_interval_minutes} 分钟
- 连续信号保护: 防止连续{self.config.consecutive_limit}次相同信号
- 持仓一致性检查: 避免频繁反向开仓
- 信号反转频率限制: {self.config.reversal_window}个信号中最多{self.config.max_reversals-1}次反转
- 历史信号记录: {len(self.signal_history)} 条
        """.strip()