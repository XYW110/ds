"""
主交易引擎

协调所有模块，实现完整的自动化交易流程。
"""

# type: ignore  # 忽略类型检查错误

import time
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Optional, List

from .config import get_config
from .exchanges.factory import create_exchange_adapter
from .analysis.indicators import TechnicalIndicators
from .analysis.ai_analyzer import AIAnalyzer
from .analysis.sentiment import SentimentAnalyzer
from .analysis.text_generator import TechnicalAnalysisTextGenerator
from .execution.position_manager import PositionManager
from .execution.order_executor import OrderExecutor
from .execution.frequency_guard import FrequencyGuard


class TradingEngine:
    """主交易引擎"""

    def __init__(self, exchange_name: Optional[str] = None):
        print("🚀 初始化DeepSeek交易机器人...")

        # 配置加载
        self.config = get_config()
        self.trade_config = self.config.trading

        # 初始化各个模块
        self._initialize_modules(exchange_name)

        # 状态变量
        self.signal_history: List[Dict[str, Any]] = []
        self.max_signal_history = self.config.engine.signal_history_max
        self.running = False
        self.strategy_id = "core-15m"

        print("✅ 交易引擎初始化完成")

    def _initialize_modules(self, exchange_name: Optional[str]):
        """初始化各个模块"""
        try:
            # 1. 交易所适配器
            print("🔄 初始化交易所适配器...")
            self.exchange = create_exchange_adapter(exchange_name)
            if not self.exchange.initialize():
                raise RuntimeError("交易所适配器初始化失败")

            # 2. 技术指标模块
            print("🔄 初始化技术指标模块...")
            self.indicators = TechnicalIndicators()

            # 3. AI分析模块
            print("🔄 初始化AI分析模块...")
            self.ai_analyzer = AIAnalyzer()

            # 4. 市场情绪模块
            print("🔄 初始化市场情绪模块...")
            self.sentiment_analyzer = SentimentAnalyzer()

            # 5. 文本生成器
            print("🔄 初始化文本生成器...")
            self.text_generator = TechnicalAnalysisTextGenerator()

            # 6. 交易执行模块
            print("🔄 初始化交易执行模块...")
            self.position_manager = PositionManager(self.exchange)
            self.order_executor = OrderExecutor(self.exchange)
            self.frequency_guard = FrequencyGuard()

            print("✅ 所有模块初始化成功")

        except Exception as e:
            print(f"❌ 模块初始化失败: {e}")
            raise

    def setup_trading_environment(self) -> bool:
        """设置交易环境"""
        try:
            print("⚙️ 设置交易环境...")

            # 使用交易所适配器的设置方法
            success = self.exchange.setup_for_trading(
                symbol=self.trade_config.symbol,
                leverage=self.trade_config.leverage
            )

            if success:
                print("✅ 交易环境设置完成")
                return True
            else:
                print("❌ 交易环境设置失败")
                return False

        except Exception as e:
            print(f"❌ 交易环境设置异常: {e}")
            return False

    def run_trading_cycle(self) -> Dict[str, Any]:
        """
        执行完整的交易周期

        Returns:
            Dict[str, Any]: 交易周期结果
        """
        cycle_start_time = time.time()

        try:
            print("\n" + "="*60)
            print(f"🔄 开始交易周期 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60)

            # 1. 获取市场数据
            market_data = self._fetch_market_data()
            if not market_data:
                return self._create_cycle_result('failed', '获取市场数据失败')

            # 2. 计算技术指标
            technical_data = self._calculate_technical_indicators(market_data)
            market_data['technical_data'] = technical_data

            # 3. 获取市场情绪数据
            sentiment_data = self._fetch_sentiment_data()
            market_data['sentiment_data'] = sentiment_data

            # 4. 生成技术分析文本
            technical_text = self.text_generator.generate_analysis_text(market_data)
            market_data['technical_analysis_text'] = technical_text

            # 5. 生成情绪文本
            sentiment_text = self.sentiment_analyzer.format_sentiment_text(sentiment_data) if sentiment_data else "【市场情绪】数据暂不可用"
            market_data['sentiment_text'] = sentiment_text

            # 6. 获取当前持仓
            current_position = self._get_current_position()
            market_data['current_position'] = current_position

            # 7. AI分析生成信号
            signal_data = self._generate_trading_signal(market_data)
            if not signal_data:
                return self._create_cycle_result('failed', '生成交易信号失败')

            # 8. 防频繁交易检查
            frequency_check = self.frequency_guard.should_allow_trade(signal_data, current_position)
            if not frequency_check['allow']:
                print(f"🛡️ 防频繁交易保护: {frequency_check['reason']}")
                return self._create_cycle_result('blocked', frequency_check['reason'], signal_data)

            # 9. 计算仓位大小
            position_size = self.position_manager.calculate_position_size(
                signal_data, market_data, current_position
            )

            # 10. 验证仓位风险
            risk_validation = self.position_manager.validate_position_risk(
                signal_data, market_data, position_size
            )
            if not risk_validation['valid']:
                print(f"⚠️ 仓位风险验证失败: {risk_validation['errors']}")
                return self._create_cycle_result('risk_blocked', '仓位风险过高', signal_data)

            # 11. 执行交易
            execution_result = self._execute_trade(signal_data, market_data, position_size)

            # 12. 记录信号到历史
            self._record_signal(signal_data, market_data)

            # 13. 生成周期报告
            cycle_time = time.time() - cycle_start_time
            result = self._create_cycle_result(
                'success' if execution_result.get('success', False) else 'failed',
                execution_result.get('message', '交易执行完成'),
                signal_data,
                execution_result,
                cycle_time
            )

            self._print_cycle_summary(result)
            return result

        except Exception as e:
            print(f"❌ 交易周期异常: {e}")
            return self._create_cycle_result('error', str(e))

    def _fetch_market_data(self) -> Optional[Dict[str, Any]]:
        """获取市场数据"""
        try:
            print("📊 获取市场数据...")

            # 获取K线数据
            ohlcv_data = self.exchange.fetch_ohlcv(
                self.trade_config.symbol,
                self.trade_config.timeframe,
                limit=self.trade_config.data_points
            )

            if not ohlcv_data:
                print("❌ 未获取到K线数据")
                return None

            # 转换为DataFrame
            df = pd.DataFrame([{
                'timestamp': item.timestamp,
                'open': item.open,
                'high': item.high,
                'low': item.low,
                'close': item.close,
                'volume': item.volume
            } for item in ohlcv_data])

            # 获取当前价格
            current_price = df['close'].iloc[-1]
            previous_price = df['close'].iloc[-2] if len(df) > 1 else current_price
            price_change = ((current_price - previous_price) / previous_price) * 100

            # 准备K线数据（用于AI分析）
            kline_data = []
            for _, row in df.tail(self.config.engine.signal_context_count + 2).iterrows():
                kline_data.append({
                    'timestamp': row['timestamp'],
                    'open': row['open'],
                    'high': row['high'],
                    'low': row['low'],
                    'close': row['close'],
                    'volume': row['volume']
                })

            market_data = {
                'symbol': self.trade_config.symbol,
                'timeframe': self.trade_config.timeframe,
                'price': current_price,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'high': df['high'].iloc[-1],
                'low': df['low'].iloc[-1],
                'volume': df['volume'].iloc[-1],
                'price_change': price_change,
                'kline_data': kline_data,
                'ohlcv_df': df
            }

            print(f"✅ 市场数据获取成功: {current_price:,.2f} ({price_change:+.2f}%)")
            return market_data

        except Exception as e:
            print(f"❌ 获取市场数据失败: {e}")
            return None

    def _calculate_technical_indicators(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """计算技术指标"""
        try:
            print("📈 计算技术指标...")

            df = market_data['ohlcv_df']
            indicators_result = self.indicators.calculate_all(df)

            # 提取指标值
            technical_data = {
                'sma_5': indicators_result.sma.get(5),
                'sma_20': indicators_result.sma.get(20),
                'sma_50': indicators_result.sma.get(50),
                'ema_12': indicators_result.ema.get(12),
                'ema_26': indicators_result.ema.get(26),
                'rsi': indicators_result.rsi,
                'macd': indicators_result.macd.get('macd'),
                'macd_signal': indicators_result.macd.get('signal'),
                'macd_histogram': indicators_result.macd.get('histogram'),
                'bb_upper': indicators_result.bollinger_bands.get('upper'),
                'bb_middle': indicators_result.bollinger_bands.get('middle'),
                'bb_lower': indicators_result.bollinger_bands.get('lower'),
                'bb_position': indicators_result.bollinger_bands.get('position'),
                'volume_ratio': indicators_result.volume_ratio,
                'support': indicators_result.support_resistance.get('support'),
                'resistance': indicators_result.support_resistance.get('resistance'),
                'current_price': market_data['price']
            }

            # 趋势分析
            trend_analysis = self.indicators.get_market_trend(indicators_result, market_data['price'])
            technical_data['trend_analysis'] = trend_analysis

            print(f"✅ 技术指标计算完成，趋势: {trend_analysis.get('overall_trend', 'neutral')}")
            return technical_data

        except Exception as e:
            print(f"❌ 技术指标计算失败: {e}")
            return {}

    def _fetch_sentiment_data(self) -> Optional[Dict[str, Any]]:
        """获取市场情绪数据"""
        try:
            if self.config.sentiment.enable:
                return self.sentiment_analyzer.fetch_sentiment_data()
            else:
                return None
        except Exception as e:
            print(f"⚠️ 市场情绪数据获取失败: {e}")
            return None

    def _get_current_position(self) -> Optional[Dict[str, Any]]:
        """获取当前持仓"""
        try:
            positions = self.exchange.fetch_positions(self.trade_config.symbol)
            for pos in positions:
                if pos.size > 0:
                    return {
                        'side': pos.side,
                        'size': pos.size,
                        'entry_price': pos.entry_price,
                        'unrealized_pnl': pos.unrealized_pnl,
                        'leverage': pos.leverage
                    }
            return None
        except Exception as e:
            print(f"⚠️ 获取持仓失败: {e}")
            return None

    def _generate_trading_signal(self, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """生成交易信号"""
        try:
            print("🤖 AI分析生成交易信号...")

            # 添加信号历史到市场数据
            if self.signal_history:
                market_data['signal_history'] = self.signal_history[-self.config.engine.signal_context_count:]  # 最近N个信号

            # 使用AI分析器生成信号
            signal_data = self.ai_analyzer.analyze_market(market_data)

            if signal_data:
                print(f"✅ AI分析完成: {signal_data.get('signal')} (信心: {signal_data.get('confidence')})")

                # 验证信号
                validation = self.ai_analyzer.validate_signal(signal_data)
                if not validation['valid']:
                    print(f"⚠️ 信号验证失败: {validation['errors']}")
                    return None

                return signal_data
            else:
                print("❌ AI分析失败")
                return None

        except Exception as e:
            print(f"❌ 信号生成失败: {e}")
            return None

    def _execute_trade(self, signal_data: Dict[str, Any],
                       market_data: Dict[str, Any], position_size: float) -> Dict[str, Any]:
        """执行交易"""
        try:
            print(f"💼 执行交易信号: {signal_data.get('signal')}")

            # 使用订单执行器执行交易
            result = self.order_executor.execute_trade_signal(
                signal_data, market_data, position_size
            )

            return result

        except Exception as e:
            print(f"❌ 交易执行失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"交易执行异常: {e}"
            }

    def _record_signal(self, signal_data: Dict[str, Any], market_data: Dict[str, Any]):
        """记录信号到历史"""
        signal_record = {
            'signal': signal_data.get('signal'),
            'confidence': signal_data.get('confidence'),
            'reason': signal_data.get('reason'),
            'stop_loss': signal_data.get('stop_loss'),
            'take_profit': signal_data.get('take_profit'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'price': market_data.get('price'),
            'source': signal_data.get('source', 'unknown')
        }

        self.signal_history.append(signal_record)

        # 保持历史记录数量
        if len(self.signal_history) > self.max_signal_history:
            self.signal_history.pop(0)

    def _create_cycle_result(self, status: str, message: str,
                           signal_data: Optional[Dict[str, Any]] = None,
                           execution_result: Optional[Dict[str, Any]] = None,
                           cycle_time: float = 0) -> Dict[str, Any]:
        """创建周期结果"""
        return {
            'status': status,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'cycle_time_seconds': round(cycle_time, 2),
            'signal_data': signal_data,
            'execution_result': execution_result
        }

    def _print_cycle_summary(self, result: Dict[str, Any]):
        """打印周期摘要"""
        print("\n" + "="*60)
        print(f"📊 交易周期完成 - {result['timestamp']}")
        print(f"⏱️ 执行时间: {result['cycle_time_seconds']:.2f} 秒")
        print(f"🎯 状态: {result['status']}")
        print(f"💬 消息: {result['message']}")

        if result.get('signal_data'):
            signal = result['signal_data']
            print(f"📈 信号: {signal.get('signal')} ({signal.get('confidence')})")
            print(f"💡 理由: {signal.get('reason')}")

        if result.get('execution_result'):
            exec_result = result['execution_result']
            if exec_result.get('success'):
                print(f"✅ 执行成功: {exec_result.get('message')}")
            else:
                print(f"❌ 执行失败: {exec_result.get('message')}")

        print("="*60)

    def start(self) -> bool:
        """启动策略"""
        if self.running:
            print(f"⚠️ 策略 {self.strategy_id} 已在运行中")
            return False
        self.running = True
        print(f"🚀 策略 {self.strategy_id} 已启动")
        return True

    def stop(self) -> bool:
        """停止策略"""
        if not self.running:
            print(f"⚠️ 策略 {self.strategy_id} 未在运行")
            return False
        self.running = False
        print(f"🛑 策略 {self.strategy_id} 已停止")
        return True

    def get_status(self) -> Dict[str, Any]:
        """获取完整状态"""
        return {
            'id': self.strategy_id,
            'status': 'running' if self.running else 'stopped',
            'running': self.running,
            'config': {
                'symbol': self.trade_config.symbol,
                'timeframe': self.trade_config.timeframe,
                'leverage': self.trade_config.leverage,
                'test_mode': self.trade_config.test_mode
            },
            'signal_history_count': len(self.signal_history),
            'recent_signals': self.signal_history[-self.config.engine.signal_context_count:] if self.signal_history else [],
            'order_stats': self.order_executor.get_execution_statistics(),
            'frequency_stats': self.frequency_guard.get_trade_statistics()
        }

    def update_config(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """更新配置参数"""
        updated = {}
        for key, value in params.items():
            if hasattr(self.trade_config, key):
                setattr(self.trade_config, key, value)
                updated[key] = value
            elif hasattr(self.config, key):
                setattr(self.config, key, value)
                updated[key] = value
        print(f"⚙️ 配置已更新: {updated}")
        return updated

    def get_status_summary(self) -> Dict[str, Any]:
        """获取状态摘要"""
        return {
            'config': {
                'symbol': self.trade_config.symbol,
                'timeframe': self.trade_config.timeframe,
                'leverage': self.trade_config.leverage,
                'test_mode': self.trade_config.test_mode
            },
            'signal_history_count': len(self.signal_history),
            'recent_signals': self.signal_history[-self.config.engine.signal_context_count:] if self.signal_history else [],
            'order_stats': self.order_executor.get_execution_statistics(),
            'frequency_stats': self.frequency_guard.get_trade_statistics()
        }

    def shutdown(self):
        """关闭交易引擎"""
        print("��� 关闭交易引擎...")
        print("✅ 交易引擎已关闭")