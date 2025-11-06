"""
DeepSeek交易机器人主程序

统一版本的DeepSeek AI驱动交易机器人。
"""

import sys
import signal
import time
import argparse
from datetime import datetime
from typing import Optional

from src.config import get_config
from src.trading_engine import TradingEngine


class DeepSeekTradingBot:
    """DeepSeek交易机器人主类"""

    def __init__(self, exchange_name: Optional[str] = None):
        print("DeepSeek AI交易机器人启动中...")
        self.engine = None
        self.running = False
        self.exchange_name = exchange_name

    def initialize(self) -> bool:
        """初始化交易机器人"""
        try:
            # 加载配置
            config = get_config()

            # 验证配置
            validation = config.validate()
            if not validation['valid']:
                print("❌ 配置验证失败:")
                for error in validation['errors']:
                    print(f"   - {error}")
                return False

            if validation['warnings']:
                print("警告: 配置警告:")
                for warning in validation['warnings']:
                    print(f"   - {warning}")

            # 初始化交易引擎
            self.engine = TradingEngine(self.exchange_name)

            # 设置交易环境
            if not self.engine.setup_trading_environment():
                print("❌ 交易环境设置失败")
                return False

            # 设置信号处理
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)

            print("成功: 交易机器人初始化成功")
            return True

        except Exception as e:
            print(f"错误: 初始化失败: {e}")
            return False

    def run_once(self) -> bool:
        """运行一次交易周期"""
        try:
            result = self.engine.run_trading_cycle()
            return result.get('status') != 'error'
        except Exception as e:
            print(f"❌ 交易周期运行失败: {e}")
            return False

    def run_scheduled(self):
        """定时运行模式"""
        config = get_config()
        timeframe = config.trading.timeframe

        print(f"🕐 启���定时运行模式 - 时间周期: {timeframe}")
        print("按 Ctrl+C 停止程序")

        # 立即执行一次
        print("🚀 执行首次交易周期...")
        self.run_once()

        # 设置定时调度
        if timeframe == '1m':
            interval = 60  # 1分钟
        elif timeframe == '5m':
            interval = 300  # 5分钟
        elif timeframe == '15m':
            interval = 900  # 15分钟
        elif timeframe == '30m':
            interval = 1800  # 30分钟
        elif timeframe == '1h':
            interval = 3600  # 1小时
        elif timeframe == '4h':
            interval = 14400  # 4小时
        else:
            interval = 900  # 默认15分钟

        self.running = True

        while self.running:
            try:
                # 等待到下一个执行时间
                time.sleep(interval)

                if not self.running:
                    break

                print(f"\n🕐 定时执行 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.run_once()

            except KeyboardInterrupt:
                print("\n👋 用户中断，正在停止...")
                break
            except Exception as e:
                print(f"❌ 定时运行异常: {e}")
                # 继续运行，不退出程序

    def run_interactive(self):
        """交互式运行模式"""
        print("🎮 启动交互式运行模式")
        print("输入命令: 'run' (执行一次), 'status' (查看状态), 'quit' (退出)")

        self.running = True

        while self.running:
            try:
                command = input("\n> ").strip().lower()

                if command == 'run' or command == 'r':
                    self.run_once()
                elif command == 'status' or command == 's':
                    self._print_status()
                elif command == 'quit' or command == 'q' or command == 'exit':
                    print("👋 正在退出...")
                    break
                elif command == 'help' or command == 'h':
                    self._print_help()
                elif command == '':
                    continue
                else:
                    print(f"❌ 未知命令: {command}，输入 'help' 查看帮助")

            except KeyboardInterrupt:
                print("\n👋 用户中断，正在退出...")
                break
            except Exception as e:
                print(f"❌ 命令执行异常: {e}")

    def _print_status(self):
        """打印状态信息"""
        if not self.engine:
            print("❌ 交易引擎未初始化")
            return

        try:
            status = self.engine.get_status_summary()
            config = status['config']

            print("\n📊 交易机器人状态:")
            print(f"   - 交易对: {config['symbol']}")
            print(f"   - 时间周期: {config['timeframe']}")
            print(f"   - 杠杆倍数: {config['leverage']}x")
            print(f"   - 测试模式: {'是' if config['test_mode'] else '否'}")
            print(f"   - 信号历史: {status['signal_history_count']} 条")

            # 最近信号
            recent_signals = status.get('recent_signals', [])
            if recent_signals:
                print("   - 最近信号:")
                for signal in recent_signals[-3:]:
                    print(f"     {signal['timestamp']}: {signal['signal']} ({signal['confidence']})")

            # 订单统计
            order_stats = status.get('order_stats', {})
            if order_stats.get('total_orders', 0) > 0:
                print(f"   - 订单统计: {order_stats['total_orders']} 单")
                print(f"     成功率: {order_stats['success_rate']:.1f}%")

        except Exception as e:
            print(f"❌ 获取状态失败: {e}")

    def _print_help(self):
        """打印帮助信息"""
        print("\n📖 可用命令:")
        print("   run, r        - 执行一次交易周期")
        print("   status, s     - 查看机器人状态")
        print("   help, h       - 显示帮助信息")
        print("   quit, q       - 退出程序")

    def _signal_handler(self, signum, frame):
        """信号处理器"""
        print(f"\n🛑 接收到信号 {signum}，正在停止...")
        self.running = False

    def shutdown(self):
        """关闭交易机器人"""
        print("🔄 正在关闭交易机器人...")
        if self.engine:
            self.engine.shutdown()
        print("成功: 交易机器人已关闭")


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='DeepSeek AI交易机器人',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py                    # 使用默认配置
  python main.py --exchange okx     # 指定交易所
  python main.py --mode interactive # 交互式模式
  python main.py --mode once        # 执行一次后退出
        """
    )

    parser.add_argument(
        '--exchange', '-e',
        choices=['okx', 'binance'],
        help='指定交易所 (默认自动检测)'
    )

    parser.add_argument(
        '--mode', '-m',
        choices=['scheduled', 'interactive', 'once'],
        default='scheduled',
        help='运行模式 (默认: scheduled)'
    )

    parser.add_argument(
        '--config', '-c',
        help='配置文件路径'
    )

    parser.add_argument(
        '--test',
        action='store_true',
        help='强制启用测试模式'
    )

    parser.add_argument(
        '--status',
        action='store_true',
        help='只显示状态信息，不运行交易'
    )

    return parser.parse_args()


def main():
    """主函数"""
    try:
        # 解析命令行参数
        args = parse_arguments()

        print("DeepSeek AI交易机器人 v5.0 (BMad统一架构)")
        print("="*50)

        # 如果是状态查询模式
        if args.status:
            bot = DeepSeekTradingBot(args.exchange)
            if bot.initialize():
                bot._print_status()
            return

        # 创建交易机器人
        bot = DeepSeekTradingBot(args.exchange)

        # 初始化
        if not bot.initialize():
            print("❌ 交易机器人初始化失败")
            sys.exit(1)

        # 强制测试模式
        if args.test:
            print("🧪 强制启用测试模式")
            # 这里可以设置测试模式的配置

        # 根据模式运行
        if args.mode == 'once':
            print("🎯 执行单次运行模式")
            success = bot.run_once()
            sys.exit(0 if success else 1)

        elif args.mode == 'interactive':
            bot.run_interactive()

        else:  # scheduled
            bot.run_scheduled()

    except KeyboardInterrupt:
        print("\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"❌ 程序运行异常: {e}")
        sys.exit(1)
    finally:
        # 确保清理资源
        if 'bot' in locals():
            bot.shutdown()


if __name__ == "__main__":
    main()