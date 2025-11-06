"""
JSON解析工具

提供安全的JSON解析和验证功能。
"""

# type: ignore  # 忽略类型检查错误

import json
import re
from typing import Dict, Any, Optional


class JSONParser:
    """安全JSON解析器"""

    def __init__(self):
        self.json_schema = {
            'required_fields': ['signal', 'reason', 'confidence'],
            'valid_signals': ['BUY', 'SELL', 'HOLD'],
            'valid_confidence': ['HIGH', 'MEDIUM', 'LOW']
        }

    def parse_signal_json(self, json_str: str) -> Optional[Dict[str, Any]]:
        """
        解析交易信号JSON

        Args:
            json_str: JSON字符串

        Returns:
            Dict[str, Any]: 解析后的数据
        """
        try:
            # 1. 提取JSON内容
            extracted_json = self._extract_json(json_str)
            if not extracted_json:
                return None

            # 2. 解析JSON
            data = json.loads(extracted_json)

            # 3. 验证和清洗数据
            cleaned_data = self._validate_and_clean(data)

            return cleaned_data

        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            return None
        except Exception as e:
            print(f"❌ 处理JSON时发生错误: {e}")
            return None

    def _extract_json(self, text: str) -> Optional[str]:
        """
        从文本中提取JSON内容

        Args:
            text: 包含JSON的文本

        Returns:
            str: 提取的JSON字符串
        """
        if not text:
            return None

        # 1. ��试直接查找第一个完整的JSON对象
        start_idx = text.find('{')
        if start_idx == -1:
            # 尝试查找JSON数组
            start_idx = text.find('[')

        if start_idx == -1:
            print("⚠️ 未找到JSON起始标记")
            return None

        # 2. 查找匹配的结束标记
        end_idx = self._find_matching_brace(text, start_idx)
        if end_idx == -1:
            print("⚠️ 未找到匹配的JSON结束标记")
            return None

        # 3. 提取JSON内容
        json_content = text[start_idx:end_idx + 1].strip()

        # 4. 预处理：移除注释和多余的空白
        json_content = self._preprocess_json(json_content)

        return json_content

    def _find_matching_brace(self, text: str, start_idx: int) -> int:
        """
        查找匹配的括号

        Args:
            text: 文本
            start_idx: 起始索引

        Returns:
            int: 结束索引，-1表示未找到
        """
        char = text[start_idx]
        if char == '{':
            closing_char = '}'
        elif char == '[':
            closing_char = ']'
        else:
            return -1

        brace_count = 1
        for i in range(start_idx + 1, len(text)):
            if text[i] == char:
                brace_count += 1
            elif text[i] == closing_char:
                brace_count -= 1
                if brace_count == 0:
                    return i

        return -1

    def _preprocess_json(self, json_str: str) -> str:
        """
        预处理JSON字符串

        Args:
            json_str: 原始JSON字符串

        Returns:
            str: 处理后的JSON字符串
        """
        # 移除单行注释
        json_str = re.sub(r'//.*', '', json_str)

        # 移除多行注释
        json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)

        # 移除尾随逗号
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)

        return json_str.strip()

    def _validate_and_clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证和清洗数据

        Args:
            data: 原始数据

        Returns:
            Dict[str, Any]: 清洗后的数据
        """
        cleaned = {}

        # 验证必需字段
        for field in self.json_schema['required_fields']:
            if field in data:
                cleaned[field] = data[field]
            else:
                print(f"⚠️ 缺少必需字段: {field}")
                return None

        # 验证信号值
        signal = cleaned.get('signal', '').upper()
        if signal not in self.json_schema['valid_signals']:
            print(f"⚠️ 无效的信号值: {signal}")
            return None
        cleaned['signal'] = signal

        # 验证信心度
        confidence = cleaned.get('confidence', '').upper()
        if confidence not in self.json_schema['valid_confidence']:
            print(f"⚠️ 无效的信心度: {confidence}，使用默认值 MEDIUM")
            cleaned['confidence'] = 'MEDIUM'
        else:
            cleaned['confidence'] = confidence

        # 清洗和验证价格字段
        price_fields = ['stop_loss', 'take_profit']
        for field in price_fields:
            if field in data:
                try:
                    price = float(data[field])
                    if price > 0:
                        cleaned[field] = price
                    else:
                        print(f"⚠️ 无效的{field}价格: {price}")
                        cleaned[field] = 0.0
                except (ValueError, TypeError):
                    print(f"⚠️ 无法解析{field}价格: {data[field]}")
                    cleaned[field] = 0.0

        # 清洗其他字段
        optional_fields = ['reason', 'timestamp']
        for field in optional_fields:
            if field in data:
                cleaned[field] = str(data[field]).strip()

        return cleaned

    def safe_parse(self, json_str: str, default_value: Any = None) -> Any:
        """
        安全解析JSON，失败时返回默认值

        Args:
            json_str: JSON字符串
            default_value: 默认值

        Returns:
            Any: 解析结果或默认值
        """
        try:
            return json.loads(json_str)
        except (json.JSONDecodeError, TypeError, ValueError):
            return default_value

    def is_valid_json(self, text: str) -> bool:
        """
        检查文本是否包含有效的JSON

        Args:
            text: 文本内容

        Returns:
            bool: 是否包含有效JSON
        """
        try:
            json_str = self._extract_json(text)
            if json_str:
                json.loads(json_str)
                return True
            return False
        except:
            return False

    def format_signal_data(self, signal_data: Dict[str, Any]) -> str:
        """
        格式化信号数据为JSON字符串

        Args:
            signal_data: 信号数据

        Returns:
            str: 格式化的JSON字符串
        """
        try:
            return json.dumps(signal_data, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ 格式化信号数据失败: {e}")
            return str(signal_data)