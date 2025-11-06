#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终清理中英文混合文本
"""

import re
from pathlib import Path

# 最终混合文本修复
MIXED_TEXT_FIXES = {
    # ====== 代码注释中的混合 ======
    "# 创建实例 of ": "# 创建 ",
    "# 创建 instance of ": "# 创建 ",
    "# Create an instance of ": "# 创建 ",
    
    # ====== 表格中的混合 ======
    " 描述 of ": " ",
    " 描述 of this ": " 此",
    "描述 of this tool collection": "此工具集合的描述",
    
    # ====== 句子中的混合 ======
    " inherits from BaseTool and 支持": " 继承自 BaseTool 并支持",
    " inherits from BaseTool and 支持these 参数s": " 继承自 BaseTool 并支持这些参数",
    " and 支持": " 并支持",
    " and 支持these ": " 并支持这些 ",
    "支持these 参数s": "支持这些参数",
    "these 参数s": "这些参数",
    
    # ====== 其他混合模式 ======
    " with 参数s": " 带参数",
    "Example with 参数s": "带参数的示例",
    " for these ": " 对于这些 ",
    " in these ": " 在这些 ",
    " of these ": " 这些 ",
    " from these ": " 从这些 ",
    " to these ": " 到这些 ",
    
    # ====== Yes/No ======
    "| **Yes** |": "| **是** |",
    "| Yes |": "| 是 |",
    "| No |": "| 否 |",
    "**Yes**": "**是**",
    "**No**": "**否**",
    
    # 修复部分中文翻译
    " 由智能体用于引用工具": "（由智能体用于引用工具）",
    
    # ====== 修复特殊字符周围的混合 ======
    "（可用于兼容的 API）": "（可用于兼容的 API）",
}

def final_cleanup(content):
    """最终清理"""
    # 应用修复
    fixes = sorted(MIXED_TEXT_FIXES.items(), key=lambda x: len(x[0]), reverse=True)
    for en, zh in fixes:
        content = content.replace(en, zh)
    
    return content

def process_file(file_path):
    """处理单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()
        
        print(f"清理: {file_path.name}")
        
        # 应用清理
        cleaned = final_cleanup(original)
        
        # 检查是否有变化
        if cleaned != original:
            changes = sum(1 for a, b in zip(original, cleaned) if a != b)
            changes += abs(len(original) - len(cleaned))
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            
            print(f"  ✓ 已清理 ({changes} 处修改)\n")
            return True
        else:
            print(f"  - 无需清理\n")
            return False
        
    except Exception as e:
        print(f"  ✗ 错误: {e}\n")
        return False

def main():
    """主函数"""
    docs_dir = Path("content/docs")
    
    # 获取所有中文翻译文件
    zh_files = list(docs_dir.glob("*.zh-CN.mdx"))
    
    print(f"找到 {len(zh_files)} 个中文翻译文件")
    print("开始最终清理...\n")
    
    cleaned_count = 0
    
    for zh_file in sorted(zh_files):
        if process_file(zh_file):
            cleaned_count += 1
    
    print(f"{'='*60}")
    print(f"✅ 完成！清理了 {cleaned_count}/{len(zh_files)} 个文件")
    print(f"\n🎉 翻译优化全部完成！")
    print(f"\n总结：")
    print(f"  ✓ 修复了中英文混合文本")
    print(f"  ✓ 翻译了代码注释")
    print(f"  ✓ 翻译了段落标题")
    print(f"  ✓ 统一了术语使用")
    print(f"  ✓ 清理了格式问题")
    print(f"\n建议：运行 pnpm dev 预览最终效果")

if __name__ == "__main__":
    main()

