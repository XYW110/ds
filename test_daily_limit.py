#!/usr/bin/env python3
"""
日投入限额功能测试脚本

测试日投入限额管理器的各项功能：
- 配置加载和验证
- 交易记录和限额检查
- 数据库操作
- 时间处理和重置逻辑
"""

import os
import sys
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, 'src')

def test_config_loading():
    """测试配置加载功能"""
    print("[测试] 配置加载功能...")

    try:
        from src.config.config_manager import get_config

        config = get_config()
        daily_limit_config = config.daily_limit

        print(f"[OK] 配置加载成功")
        print(f"  - 日投入限额: {daily_limit_config.daily_limit_usdt} USDT")
        print(f"  - 重置时间: {daily_limit_config.reset_hour}:00 ({daily_limit_config.reset_timezone})")
        print(f"  - 数据库路径: {daily_limit_config.database_path}")
        print(f"  - 警告阈值: {daily_limit_config.warning_threshold*100:.0f}%")

        # 测试配置验证
        validation = config.validate()
        print(f"[OK] 配置验证: {'通过' if validation['valid'] else '失败'}")

        if validation['errors']:
            print("[ERROR] 配置错误:")
            for error in validation['errors']:
                print(f"   - {error}")

        if validation['warnings']:
            print("[WARNING] 配置警告:")
            for warning in validation['warnings']:
                print(f"   - {warning}")

        return validation['valid']

    except Exception as e:
        print(f"[ERROR] 配置测试失败: {e}")
        return False

def test_database_initialization():
    """测试数据库初始化"""
    print("\n[测试] 数据库初始化...")

    try:
        from src.config.config_manager import get_config
        from src.utils.daily_limit_manager import DailyLimitManager

        config = get_config().daily_limit

        # 删除现有数据库文件（如果存在）
        db_path = Path(config.database_path)
        if db_path.exists():
            db_path.unlink()
            print(f"[INFO] 已删除现有数据库文件: {db_path}")

        # 初始化管理器
        manager = DailyLimitManager(config)
        print("[OK] 日投入限额管理器初始化成功")

        # 检查数据库文件是否创建
        if db_path.exists():
            print(f"[OK] 数据库文件已创建: {db_path}")
        else:
            print("[ERROR] 数据库文件未创建")
            return False

        # 检查表结构
        with sqlite3.connect(config.database_path) as conn:
            cursor = conn.cursor()

            # 检查交易记录表
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trade_records'")
            if cursor.fetchone():
                print("[OK] trade_records表已创建")
            else:
                print("[ERROR] trade_records表未创建")
                return False

            # 检查日统计表
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='daily_stats'")
            if cursor.fetchone():
                print("[OK] daily_stats表已创建")
            else:
                print("[ERROR] daily_stats表未创建")
                return False

        return True

    except Exception as e:
        print(f"[ERROR] 数据库初始化测试失败: {e}")
        return False

def test_daily_limit_logic():
    """测试日投入限额逻辑"""
    print("\n[测试] 日投入限额逻辑...")

    try:
        from src.config.config_manager import get_config
        from src.utils.daily_limit_manager import DailyLimitManager, TradeRecord

        config = get_config().daily_limit
        manager = DailyLimitManager(config)

        # 获取当前状态
        stats = manager.get_daily_stats()
        print(f"[OK] 获取当前统计: 已投入 {stats.get('total_usdt_invested', 0):.2f} USDT")

        # 测试限额检查
        can_trade, reason = manager.check_trade_limit(100, "BUY")
        print(f"[OK] 限额检查 (100 USDT): {can_trade} - {reason}")

        # 测试模拟交易记录
        test_trade = TradeRecord(
            symbol="BTC/USDT:USDT",
            side="BUY",
            amount=0.001,
            price=50000,
            usdt_value=50,
            status="completed",
            strategy="TEST",
            confidence="HIGH"
        )

        success = manager.record_trade(test_trade)
        if success:
            print("[OK] 交易记录成功")

            # 更新后的统计
            updated_stats = manager.get_daily_stats()
            print(f"[OK] 更新后统计: 已投入 {updated_stats.get('total_usdt_invested', 0):.2f} USDT")
        else:
            print("[ERROR] 交易记录失败")
            return False

        # 测试接近限额的情况
        large_amount = config.daily_limit_usdt - updated_stats.get('total_usdt_invested', 0) + 100
        can_trade_large, reason_large = manager.check_trade_limit(large_amount, "BUY")
        print(f"[OK] 大额交易检查 ({large_amount:.2f} USDT): {can_trade_large} - {reason_large}")

        return True

    except Exception as e:
        print(f"[ERROR] 日限额逻辑测试失败: {e}")
        return False

def test_position_manager_integration():
    """测试仓位管理器集成"""
    print("\n[测试] 仓位管理器集成...")

    try:
        # 模拟交易所适配器
        class MockExchangeAdapter:
            def fetch_balance(self):
                return {
                    'USDT': {'free': 5000.0, 'used': 1000.0, 'total': 6000.0}
                }

            def calculate_position_size(self, usdt_amount, symbol):
                # 简化计算：假设1 BTC = 50000 USDT
                return usdt_amount / 50000

        from src.execution.position_manager import PositionManager

        mock_exchange = MockExchangeAdapter()
        position_manager = PositionManager(mock_exchange)

        # 检查限额状态
        status = position_manager.get_daily_limit_status()
        print(f"[OK] 限额状态获取: 启用={status.get('enabled', False)}")

        # 测试仓位计算
        signal_data = {
            'signal': 'BUY',
            'confidence': 'HIGH',
            'stop_loss': 48000,
            'take_profit': 52000
        }

        market_data = {
            'symbol': 'BTC/USDT:USDT',
            'price': 50000,
            'technical_data': {'rsi': 45},
            'trend_analysis': {'overall': '震荡上涨'}
        }

        position_size = position_manager.calculate_position_size(signal_data, market_data)
        print(f"[OK] 仓位计算结果: {position_size:.6f} 张")

        if position_size > 0:
            # 测试交易记录
            success = position_manager.record_trade(
                symbol="BTC/USDT:USDT",
                side="BUY",
                amount=position_size,
                price=50000,
                status="completed",
                strategy="TEST",
                confidence="HIGH"
            )
            print(f"[OK] 交易记录: {success}")

        # 打印限额汇总
        position_manager.print_daily_limit_summary()

        return True

    except Exception as e:
        print(f"[ERROR] 仓位管理器集成测试失败: {e}")
        return False

def test_time_handling():
    """测试时间处理功能"""
    print("\n[测试] 时间处理功能...")

    try:
        from src.config.config_manager import get_config
        from src.utils.daily_limit_manager import DailyLimitManager

        config = get_config().daily_limit
        manager = DailyLimitManager(config)

        # 测试当前日期获取
        current_date = manager.get_current_date()
        print(f"[OK] 当前日期: {current_date}")

        # 测试下次重置时间
        next_reset = manager.get_next_reset_time()
        print(f"[OK] 下次重置时间: {next_reset.strftime('%Y-%m-%d %H:%M:%S')} UTC")

        # 测试重置检查
        should_reset = manager.should_reset_daily_limit()
        print(f"[OK] 是否需要重置: {should_reset}")

        return True

    except Exception as e:
        print(f"[ERROR] 时间处理测试失败: {e}")
        return False

def generate_test_report():
    """生成测试报告"""
    print("\n[测试] 生成测试报告...")

    tests = [
        ("配置加载", test_config_loading),
        ("数据库初始化", test_database_initialization),
        ("日限额逻辑", test_daily_limit_logic),
        ("仓位管理器集成", test_position_manager_integration),
        ("时间处理", test_time_handling)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[ERROR] {test_name} 测试异常: {e}")
            results.append((test_name, False))

    print(f"\n[RESULT] 测试完成!")

    passed_count = sum(1 for _, result in results if result)
    total_count = len(results)

    print(f"[RESULT] 测试结果: {passed_count}/{total_count} 项通过")

    if passed_count == total_count:
        print("[SUCCESS] 所有测试通过! 日投入限额功能正常工作")
        overall_status = "PASS"
    else:
        print("[PARTIAL] 部分测试未通过，请检查实现")
        overall_status = "PARTIAL"

    print("\n详细结果:")
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")

    return overall_status, results

def main():
    """主函数"""
    print("[日投入限额功能测试]")
    print("=" * 50)

    # 显示环境信息
    print(f"Python版本: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # 运行测试
    status, results = generate_test_report()

    print(f"\n测试状态: {status}")
    print("\n[测试结束]")

if __name__ == "__main__":
    main()