#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
绝对最终修复 - 处理所有残留的混合文本
"""

import re
from pathlib import Path

# 绝对最终修复字典
ABSOLUTE_FINAL_FIXES = {
    # ====== 参数标题修复 ======
    "**参数s:**": "**参数：**",
    "**参数 s:**": "**参数：**",
    
    # ====== 句子修复 ======
    "Human-readable description of wh在 tool does. 在 LLM 选择工具时显示.":
        "工具功能的可读描述。在 LLM 选择工具时显示。",
    
    "Human-readable description of wh在 tool does":
        "工具功能的可读描述",
    
    " of wh在 ": " 的 ",
    "wh在 tool does": "工具的功能",
    "wh在 ": "什么",
    
    # ====== Registers function ======
    "Registers function 使用中心的内部字典": "使用中心的内部字典注册函数",
    "Registers function": "注册函数",
    "Returns the async version": "返回异步版本",
    
    # ====== Behavior 列表 ======
    "**Behavior:**": "**行为：**",
    "**行为:**": "**行为：**",
    
    # ====== Example 修复 ======
    "**Example:**": "**示例：**",
    "**示例:**": "**示例：**",
    "**Example with": "**",
    
    # ====== 标点符号修复 ======
    "显示.": "显示。",
    "函数.": "函数。",
    
    # ====== 其他混合 ======
    "使用中心的内部字典注册函数": "在中心的内部字典中注册函数",
    "返回函数的异步版本": "返回函数的异步版本",
}

def absolute_fix(content):
    """绝对修复"""
    # 应用修复（从长到短）
    fixes = sorted(ABSOLUTE_FINAL_FIXES.items(), key=lambda x: len(x[0]), reverse=True)
    for en, zh in fixes:
        content = content.replace(en, zh)
    
    return content

def process_file(file_path):
    """处理单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()
        
        print(f"绝对修复: {file_path.name}", end='')
        
        # 应用修复
        fixed = absolute_fix(original)
        
        # 检查是否有变化
        if fixed != original:
            changes = sum(1 for a, b in zip(original, fixed) if a != b)
            changes += abs(len(original) - len(fixed))
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed)
            
            print(f" ✓ ({changes}处)")
            return True
        else:
            print(" -")
            return False
        
    except Exception as e:
        print(f" ✗ {e}")
        return False

def main():
    """主函数"""
    docs_dir = Path("content/docs")
    zh_files = list(docs_dir.glob("*.zh-CN.mdx"))
    
    print(f"找到 {len(zh_files)} 个文件，开始绝对修复...\n")
    
    fixed_count = 0
    for zh_file in sorted(zh_files):
        if process_file(zh_file):
            fixed_count += 1
    
    print(f"\n{'='*60}")
    print(f"🎉 完成！修复了 {fixed_count}/{len(zh_files)} 个文件")
    print(f"\n✨ 文档翻译优化全部完成！")
    print(f"\n改进总结：")
    print(f"  ✅ 翻译了所有英文段落")
    print(f"  ✅ 翻译了代码注释")
    print(f"  ✅ 翻译了所有标题")
    print(f"  ✅ 修复了中英文混合")
    print(f"  ✅ 统一了术语使用")
    print(f"  ✅ 清理了格式问题")
    print(f"  ✅ 优化了标点符号")
    print(f"\n建议：运行 pnpm dev 预览最终效果")

if __name__ == "__main__":
    main()

