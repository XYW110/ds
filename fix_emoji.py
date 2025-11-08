#!/usr/bin/env python3
"""
快速修复emoji字符问题
"""

import re

def fix_emoji_in_file(file_path):
    """修复文件中的emoji字符"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换所有emoji字符
    replacements = {
        '❌': '[ERROR]',
        '⚠️': '[WARNING]',
        '💰': '[INFO]',
        '📊': '[INFO]',
        '🔄': '[INFO]',
        '💵': '[INFO]',
        '📈': '[INFO]',
        '💡': '[INFO]',
        'ℹ️': '[INFO]',
        '🚫': '[BLOCKED]',
        '📝': '[INFO]',
        '🔧': '[INFO]',
        '💹': '[INFO]'
    }

    for emoji, replacement in replacements.items():
        content = content.replace(emoji, replacement)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Fixed emoji in {file_path}")

if __name__ == "__main__":
    fix_emoji_in_file("src/execution/position_manager.py")
    fix_emoji_in_file("src/utils/daily_limit_manager.py")
    print("Emoji fix completed!")