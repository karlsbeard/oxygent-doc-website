#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证 OxyAPI 翻译完整性
"""

from pathlib import Path
import re

def validate():
    """验证翻译完整性"""
    oxyapi_dir = Path("/Users/chengkai48/Documents/AI/oxygent-doc-website/content/oxyapi")
    
    # 获取所有英文文件
    en_files = [f for f in oxyapi_dir.glob("*.mdx")
                if not f.name.endswith(".zh-CN.mdx")]
    
    print(f"{'='*60}")
    print(f"OxyAPI 翻译完整性验证")
    print(f"{'='*60}\n")
    
    # 1. 检查文件完整性
    print("1. 检查文件完整性")
    print("-" * 60)
    missing = []
    for en_file in en_files:
        zh_file = en_file.parent / f"{en_file.stem}.zh-CN.mdx"
        if not zh_file.exists():
            missing.append(en_file.name)
            print(f"  ❌ 缺少翻译: {en_file.name}")
        else:
            print(f"  ✓ {en_file.name} → {zh_file.name}")
    
    if missing:
        print(f"\n❌ 缺少 {len(missing)} 个翻译文件")
        return False
    else:
        print(f"\n✅ 所有 {len(en_files)} 个英文文件都有对应的中文翻译")
    
    # 2. 检查 meta.zh-CN.json
    print(f"\n2. 检查 meta.zh-CN.json")
    print("-" * 60)
    meta_zh = oxyapi_dir / "meta.zh-CN.json"
    if meta_zh.exists():
        print(f"  ✓ meta.zh-CN.json 已创建")
    else:
        print(f"  ❌ meta.zh-CN.json 不存在")
        return False
    
    # 3. 检查是否有大量未翻译的英文内容
    print(f"\n3. 检查翻译质量（英文残留检测）")
    print("-" * 60)
    
    zh_files = list(oxyapi_dir.glob("*.zh-CN.mdx"))
    issues = []
    
    for zh_file in zh_files:
        with open(zh_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除代码块
        content_no_code = re.sub(r'```[\s\S]*?```', '', content)
        # 移除链接
        content_no_links = re.sub(r'\[.*?\]\(.*?\)', '', content_no_code)
        # 移除代码引用
        content_no_inline_code = re.sub(r'`[^`]+`', '', content_no_links)
        
        # 查找可能的未翻译英文句子（连续3个以上英文单词）
        english_sentences = re.findall(r'\b[A-Z][a-z]+(?:\s+[a-z]+){2,}\b', content_no_inline_code)
        
        if len(english_sentences) > 5:  # 如果发现超过5个疑似未翻译的句子
            issues.append((zh_file.name, len(english_sentences)))
            print(f"  ⚠️  {zh_file.name}: 发现 {len(english_sentences)} 处可能未翻译的英文")
        else:
            print(f"  ✓ {zh_file.name}: 翻译良好")
    
    if issues:
        print(f"\n⚠️  {len(issues)} 个文件可能需要进一步检查")
    else:
        print(f"\n✅ 所有文件翻译质量良好")
    
    # 4. 统计信息
    print(f"\n4. 统计信息")
    print("-" * 60)
    print(f"  英文文件: {len(en_files)}")
    print(f"  中文文件: {len(zh_files)}")
    print(f"  meta.zh-CN.json: {'✓' if meta_zh.exists() else '✗'}")
    
    total_size = sum(f.stat().st_size for f in zh_files)
    print(f"  中文文件总大小: {total_size / 1024:.2f} KB")
    
    print(f"\n{'='*60}")
    print(f"✅ 验证完成！所有翻译文件已创建。")
    print(f"{'='*60}")
    
    return True

if __name__ == "__main__":
    validate()


