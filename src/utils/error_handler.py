"""
错误处理模块

提供统一的错误处理和异常管理。
"""

import logging
import traceback
from typing import Dict, Any, Optional, Callable


class ErrorHandler:
    """错误处理器"""

    def __init__(self):
        self.logger = logging.getLogger('deepseek_bot')
        self.error_handlers: Dict[type, Callable] = {}

    def register_handler(self, exception_type: type, handler: Callable):
        """
        ���册异常处理器

        Args:
            exception_type: 异常类型
            handler: 处理函数
        """
        self.error_handlers[exception_type] = handler

    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """
        处理错误

        Args:
            error: 异常对象
            context: 错误上下文

        Returns:
            Dict[str, Any]: 错误处理结果
        """
        error_type = type(error)

        # 查找注册的处理器
        if error_type in self.error_handlers:
            try:
                return self.error_handlers[error_type](error, context)
            except Exception as handler_error:
                self.logger.error(f"异常处理器执行失败: {handler_error}")

        # 默认错误处理
        return self._default_error_handler(error, context)

    def _default_error_handler(self, error: Exception, context: str) -> Dict[str, Any]:
        """默认错误处理器"""
        error_info = {
            'type': type(error).__name__,
            'message': str(error),
            'context': context,
            'traceback': traceback.format_exc(),
            'timestamp': logging.LogRecord(
                name='', level=0, pathname='', lineno=0, msg='', args=(), exc_info=None
            ).created
        }

        self.logger.error(f"错误发生在 {context}: {error}")
        self.logger.debug(f"错误详情: {error_info['traceback']}")

        return {
            'handled': False,
            'error_info': error_info,
            'recovery_action': 'retry_later'
        }


# 全局错误处理器实例
error_handler = ErrorHandler()


def handle_error(error: Exception, context: str = "") -> Dict[str, Any]:
    """
    便捷的错误处理函数

    Args:
        error: 异常对象
        context: 错误上下文

    Returns:
        Dict[str, Any]: 错误处理结果
    """
    return error_handler.handle_error(error, context)