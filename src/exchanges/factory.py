# -*- coding: utf-8 -*-
"""
交易所工厂模块

提供统一的交易所适配器创建接口。
"""

from typing import Dict, Any, Optional, Type
from ..config import get_config

from .base import ExchangeAdapter
from .okx_adapter import OKXAdapter
from .binance_adapter import BinanceAdapter


class ExchangeFactory:
    """交易所工厂类"""

    # 注册的交易所适配器
    _adapters: Dict[str, Type[ExchangeAdapter]] = {
        'okx': OKXAdapter,
        'binance': BinanceAdapter,
    }

    @classmethod
    def create_adapter(cls, exchange_name: str, **kwargs) -> ExchangeAdapter:
        """
        创建交易所适配器实例

        Args:
            exchange_name: 交易所名称 ('okx', 'binance')
            **kwargs: 额外参数

        Returns:
            ExchangeAdapter: 交易所适配器实例

        Raises:
            ValueError: 不支持的交易所
            KeyError: 缺少必需的API密钥
        """
        if exchange_name.lower() not in cls._adapters:
            raise ValueError(f"不支持的交易所: {exchange_name}, 支持的交易所: {list(cls._adapters.keys())}")

        adapter_class = cls._adapters[exchange_name.lower()]
        config = get_config()
        api_keys = config.api_keys

        # 根据交易所获取对应的API密钥
        if exchange_name.lower() == 'okx':
            required_keys = ['okx_api_key', 'okx_secret', 'okx_password']
            api_key = api_keys['okx_api_key']
            secret = api_keys['okx_secret']
            password = api_keys['okx_password']
        elif exchange_name.lower() == 'binance':
            required_keys = ['binance_api_key', 'binance_secret']
            api_key = api_keys['binance_api_key']
            secret = api_keys['binance_secret']
            password = None
        else:
            raise ValueError(f"未知的交易所: {exchange_name}")

        # 验证必需的API密钥
        missing_keys = [key for key in required_keys if not api_keys.get(key.replace('okx_', '').replace('binance_', '') if key.endswith('_api_key') else key.split('_')[-1])]
        if missing_keys:
            raise KeyError(f"缺少必需的API密钥: {missing_keys}")

        # 创建适配器实例
        adapter = adapter_class(
            api_key=api_key,
            secret=secret,
            password=password,
            test_mode=config.trading.test_mode,
            **kwargs
        )

        return adapter

    @classmethod
    def create_from_config(cls, exchange_name: Optional[str] = None) -> ExchangeAdapter:
        """
        从配置创建交易所适配器

        Args:
            exchange_name: 交易所名称，如果为None则从配置读取

        Returns:
            ExchangeAdapter: 交易所适配器实例
        """
        config = get_config()

        # 如果没有指定交易所，使用配置中的默认交易所
        if exchange_name is None:
            default_exchange = config.trading.default_exchange.lower()

            if default_exchange == 'auto':
                # 自动检测可用的交易所
                exchange_name = cls._detect_available_exchange()
            else:
                # 使用指定的交易所
                exchange_name = default_exchange

        return cls.create_adapter(exchange_name)

    @classmethod
    def _detect_available_exchange(cls) -> str:
        """
        自动检测可用的交易所

        Returns:
            str: 可用的交易所名称

        Raises:
            ValueError: 没有找到可用的交易所API密钥配置
        """
        config = get_config()
        api_keys = config.api_keys

        # 优先级: OKX > Binance
        if all([api_keys['okx_api_key'], api_keys['okx_secret'], api_keys['okx_password']]):
            return 'okx'
        elif all([api_keys['binance_api_key'], api_keys['binance_secret']]):
            return 'binance'
        else:
            # 详细的错误信息
            okx_missing = []
            binance_missing = []

            if not api_keys['okx_api_key']:
                okx_missing.append('OKX_API_KEY')
            if not api_keys['okx_secret']:
                okx_missing.append('OKX_SECRET')
            if not api_keys['okx_password']:
                okx_missing.append('OKX_PASSWORD')

            if not api_keys['binance_api_key']:
                binance_missing.append('BINANCE_API_KEY')
            if not api_keys['binance_secret']:
                binance_missing.append('BINANCE_SECRET')

            error_msg = "No available exchange API keys found\n"
            if okx_missing and binance_missing:
                error_msg += f"OKX missing: {', '.join(okx_missing)}\n"
                error_msg += f"Binance missing: {', '.join(binance_missing)}"
            elif okx_missing:
                error_msg += f"OKX missing: {', '.join(okx_missing)} (Binance also required)"
            else:
                error_msg += f"Binance missing: {', '.join(binance_missing)} (OKX also required)"

            raise ValueError(error_msg)

    @classmethod
    def register_adapter(cls, name: str, adapter_class: Type[ExchangeAdapter]):
        """
        注册新的交易所适配器

        Args:
            name: 交易所名称
            adapter_class: 适配器类
        """
        cls._adapters[name.lower()] = adapter_class

    @classmethod
    def get_supported_exchanges(cls) -> list:
        """
        获取支持的交易所列表

        Returns:
            list: 支持的交易所名称列表
        """
        return list(cls._adapters.keys())

    @classmethod
    def validate_exchange_config(cls, exchange_name: str) -> Dict[str, Any]:
        """
        验证交易所配置

        Args:
            exchange_name: 交易所名称

        Returns:
            Dict[str, Any]: 验证结果
        """
        if exchange_name.lower() not in cls._adapters:
            return {
                'valid': False,
                'errors': [f"不支持的交易所: {exchange_name}"]
            }

        config = get_config()
        api_keys = config.api_keys

        errors = []
        warnings = []

        if exchange_name.lower() == 'okx':
            if not api_keys['okx_api_key']:
                errors.append("缺少OKX API Key")
            if not api_keys['okx_secret']:
                errors.append("缺少OKX Secret")
            if not api_keys['okx_password']:
                errors.append("缺少OKX Password")

        elif exchange_name.lower() == 'binance':
            if not api_keys['binance_api_key']:
                errors.append("缺少Binance API Key")
            if not api_keys['binance_secret']:
                errors.append("缺少Binance Secret")

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }


# 便捷函数
def create_exchange_adapter(exchange_name: Optional[str] = None, **kwargs) -> ExchangeAdapter:
    """
    便捷的交易所适配器创建函数

    Args:
        exchange_name: 交易所名称
        **kwargs: 额外参数

    Returns:
        ExchangeAdapter: 交易所适配器实例
    """
    if exchange_name:
        return ExchangeFactory.create_adapter(exchange_name, **kwargs)
    else:
        return ExchangeFactory.create_from_config(exchange_name, **kwargs)


def auto_detect_exchange() -> str:
    """
    自动检测可用的交易所

    Returns:
        str: 可用的交易所名称
    """
    return ExchangeFactory._detect_available_exchange()