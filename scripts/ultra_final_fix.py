#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超级最终修复 - 处理微小的残留问题
"""

import re
from pathlib import Path

# 超级细节修复
ULTRA_FINAL_FIXES = {
    # ====== 微小混合 ======
    " 在 hub.": " 在中心中。",
    " 在 hub:": " 在中心中：",
    " from hub": " 从中心",
    " to hub": " 到中心",
    " in hub": " 在中心",
    
    # ====== 标点符号修复 ======
    " 在中心中.": " 在中心中。",
    " 在中心中:": " 在中心中：",
    
    # ====== 多余空格 ======
    " ：": "：",
    "（ ": "（",
    " ）": "）",
    
    # ====== 其他细节 ======
    "将函数注册为工具 在中心中。": "将函数注册为工具在中心中。",
}

def ultra_fix(content):
    """超级修复"""
    for en, zh in ULTRA_FINAL_FIXES.items():
        content = content.replace(en, zh)
    
    # 清理多余空格
    content = re.sub(r'  +', ' ', content)
    
    return content

def process_file(file_path):
    """处理单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()
        
        print(f"超级修复: {file_path.name}", end='')
        
        # 应用修复
        fixed = ultra_fix(original)
        
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
    
    print(f"找到 {len(zh_files)} 个文件，开始超级修复...\n")
    
    fixed_count = 0
    for zh_file in sorted(zh_files):
        if process_file(zh_file):
            fixed_count += 1
    
    print(f"\n{'='*60}")
    print(f"✅ 完成！修复了 {fixed_count}/{len(zh_files)} 个文件")

if __name__ == "__main__":
    main()

