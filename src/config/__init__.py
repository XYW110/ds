"""
配置管理模块

提供统一配置管理，支持环境变量、配置文件和默认值。
"""

from .config_manager import Config, get_config

__all__ = ['Config', 'get_config']