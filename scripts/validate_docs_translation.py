#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证 content/docs/ 目录翻译完成情况
"""

import json
from pathlib import Path

def validate():
    """验证翻译完成情况"""
    docs_dir = Path("content/docs")
    
    # 1. 检查所有 .mdx 文件是否都有对应的 .zh-CN.mdx
    en_files = [f for f in docs_dir.glob("*.mdx")
                if not f.name.endswith(".zh-CN.mdx")]
    
    missing = []
    translated = []
    for en_file in en_files:
        zh_file = en_file.parent / f"{en_file.stem}.zh-CN.mdx"
        if not zh_file.exists():
            missing.append(en_file.name)
        else:
            translated.append((en_file.name, zh_file.name))
    
    print("=" * 70)
    print("📋 OxyGent Docs 翻译验证报告")
    print("=" * 70)
    print()
    
    # 报告翻译状态
    if missing:
        print(f"❌ 缺少 {len(missing)} 个中文翻译:")
        for f in missing:
            print(f"   - {f}")
        print()
    else:
        print(f"✅ 所有 {len(en_files)} 个英文文档都有对应的中文翻译")
        print()
    
    # 列出已翻译的文件
    if translated:
        print(f"📄 已翻译文件列表 ({len(translated)} 个):")
        for en, zh in sorted(translated):
            print(f"   {en:30} → {zh}")
        print()
    
    # 2. 验证 meta.zh-CN.json
    meta_zh = docs_dir / "meta.zh-CN.json"
    meta_en = docs_dir / "meta.json"
    
    if meta_zh.exists() and meta_en.exists():
        with open(meta_zh, 'r', encoding='utf-8') as f:
            zh_data = json.load(f)
        with open(meta_en, 'r', encoding='utf-8') as f:
            en_data = json.load(f)
        
        zh_pages = [p for p in zh_data.get('pages', []) if not p.startswith('---')]
        en_pages = [p for p in en_data.get('pages', []) if not p.startswith('---')]
        
        print(f"📑 meta.json 页面数: {len(en_pages)}")
        print(f"📑 meta.zh-CN.json 页面数: {len(zh_pages)}")
        
        if len(zh_pages) == len(en_pages):
            print("✅ meta.zh-CN.json 页面数量正确")
        else:
            print(f"⚠️ 页面数量不匹配 (英文: {len(en_pages)}, 中文: {len(zh_pages)})")
        print()
    
    # 3. 总结
    print("=" * 70)
    if not missing and len(zh_pages) == len(en_pages):
        print("🎉 验证通过！所有文档翻译已完成")
        print("=" * 70)
        return True
    else:
        print("⚠️ 验证未完全通过，请检查上述问题")
        print("=" * 70)
        return False

if __name__ == "__main__":
    import sys
    success = validate()
    sys.exit(0 if success else 1)

