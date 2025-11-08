#!/usr/bin/env python3
"""
简化版模拟测试脚本 - 无emoji版本
用于测试基本的交易机器人功能
"""

import os
import sys
import json
from datetime import datetime

def test_basic_imports():
    """测试基本模块导入"""
    print("[测试] 基本模块导入...")

    try:
        # 测试配置模块
        sys.path.insert(0, 'src')
        from src.config.config_manager import get_config
        print("[OK] 配置模块导入成功")

        # 加载配置
        config = get_config()
        print("[OK] 配置加载成功")

        # 验证配置
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

def test_ai_config():
    """测试AI配置"""
    print("\n[测试] AI配置...")

    try:
        from dotenv import load_dotenv
        load_dotenv()

        ai_api_key = os.getenv('AI_API_KEY')
        ai_base_url = os.getenv('AI_BASE_URL')
        ai_model = os.getenv('AI_MODEL')

        print(f"[INFO] AI API Key: {'已配置' if ai_api_key and ai_api_key != 'your_api_key_here' else '未配置'}")
        print(f"[INFO] AI Base URL: {ai_base_url or '未配置'}")
        print(f"[INFO] AI Model: {ai_model or '未配置'}")

        if ai_api_key and ai_api_key != 'your_api_key_here':
            print("[OK] AI配置检查通过")
            return True
        else:
            print("[WARNING] AI API Key未配置或使用默认值")
            return False

    except Exception as e:
        print(f"[ERROR] AI配置测试失败: {e}")
        return False

def test_exchange_config():
    """测试交易所配置"""
    print("\n[测试] 交易所配置...")

    try:
        from dotenv import load_dotenv
        load_dotenv()

        # 检查OKX配置
        okx_key = os.getenv('OKX_API_KEY')
        okx_secret = os.getenv('OKX_SECRET')
        okx_password = os.getenv('OKX_PASSWORD')

        print(f"[INFO] OKX API Key: {'已配置' if okx_key and okx_key != 'your_okx_api_key' else '未配置'}")
        print(f"[INFO] OKX Secret: {'已配置' if okx_secret and okx_secret != 'your_okx_secret' else '未配置'}")
        print(f"[INFO] OKX Password: {'已配置' if okx_password and okx_password != 'your_okx_password' else '未配置'}")

        # 检查Binance配置
        binance_key = os.getenv('BINANCE_API_KEY')
        binance_secret = os.getenv('BINANCE_SECRET')

        print(f"[INFO] Binance API Key: {'已配置' if binance_key and binance_key != 'your_binance_api_key' else '未配置'}")
        print(f"[INFO] Binance Secret: {'已配置' if binance_secret and binance_secret != 'your_binance_secret' else '未配置'}")

        # 检查交易配置
        symbol = os.getenv('TRADE_SYMBOL', 'BTC/USDT:USDT')
        leverage = os.getenv('TRADE_LEVERAGE', '10')
        test_mode = os.getenv('TRADE_TEST_MODE', 'true')

        print(f"[INFO] 交易对: {symbol}")
        print(f"[INFO] 杠杆: {leverage}x")
        print(f"[INFO] 测试模式: {test_mode}")

        has_okx = (okx_key and okx_key != 'your_okx_api_key' and
                   okx_secret and okx_secret != 'your_okx_secret' and
                   okx_password and okx_password != 'your_okx_password')

        has_binance = (binance_key and binance_key != 'your_binance_api_key' and
                      binance_secret and binance_secret != 'your_binance_secret')

        if has_okx or has_binance:
            print("[OK] 交易所配置检查通过")
            return True
        else:
            print("[WARNING] 未配置任何交易所API")
            return False

    except Exception as e:
        print(f"[ERROR] 交易所配置测试失败: {e}")
        return False

def test_ccxt_import():
    """测试CCXT库导入"""
    print("\n[测试] CCXT库...")

    try:
        import ccxt
        print(f"[OK] CCXT导入成功 (版本: {ccxt.__version__})")

        # 测试交易所支持
        exchanges = ['binance', 'okx']
        for exchange_name in exchanges:
            if hasattr(ccxt, exchange_name):
                print(f"[OK] 支持{exchange_name.upper()}交易所")
            else:
                print(f"[ERROR] 不支持{exchange_name.upper()}交易所")

        return True

    except Exception as e:
        print(f"[ERROR] CCXT测试失败: {e}")
        return False

def generate_test_report():
    """生成测试报告"""
    print("\n[测试] 生成测试报告...")

    report = {
        'test_time': datetime.now().isoformat(),
        'python_version': sys.version,
        'tests': {}
    }

    # 运行各项测试
    report['tests']['basic_imports'] = test_basic_imports()
    report['tests']['ai_config'] = test_ai_config()
    report['tests']['exchange_config'] = test_exchange_config()
    report['tests']['ccxt_import'] = test_ccxt_import()

    # 计算总体结果
    total_tests = len(report['tests'])
    passed_tests = sum(1 for result in report['tests'].values() if result)

    print(f"\n[RESULT] 测试完成!")
    print(f"[RESULT] 测试结果: {passed_tests}/{total_tests} 项通过")

    if passed_tests == total_tests:
        print("[SUCCESS] 所有测试通过! 项目环境配置正确")
        report['overall_status'] = 'PASS'
    else:
        print("[PARTIAL] 部分测试未通过，请检查配置")
        report['overall_status'] = 'PARTIAL'

    # 保存测试报告
    try:
        with open('test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[OK] 测试报告已保存到: test_report.json")
    except Exception as e:
        print(f"[WARNING] 无法保存测试报告: {e}")

    return report

def main():
    """主函数"""
    print("[DeepSeek交易机器人模拟测试]")
    print("=" * 50)

    # 显示当前环境信息
    print(f"Python版本: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # 生成测试报告
    report = generate_test_report()

    # 根据测试结果给出建议
    print("\n[建议]:")
    if not report['tests']['ai_config']:
        print("- 请在.env文件中配置有效的AI API Key")
    if not report['tests']['exchange_config']:
        print("- 请在.env文件中配置交易所API信息")
    if report['overall_status'] == 'PASS':
        print("- 环境配置完成，可以开始交易测试!")

    print("\n[测试结束]")

if __name__ == "__main__":
    main()