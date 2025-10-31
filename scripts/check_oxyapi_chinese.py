#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 oxyapi 目录中的中文内容，确保所有 API 文档都是英文
"""

import re
from pathlib import Path


def has_chinese_chars(text):
    """检查文本是否包含中文字符"""
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def check_file_chinese(file_path):
    """检查单个文件中的中文内容"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"Error reading file: {e}"]

    issues = []
    lines = content.split("\n")

    in_code_block = False
    in_frontmatter = False
    frontmatter_count = 0

    for i, line in enumerate(lines, 1):
        # 跟踪 frontmatter
        if line.strip() == "---":
            frontmatter_count += 1
            if frontmatter_count == 1:
                in_frontmatter = True
            elif frontmatter_count == 2:
                in_frontmatter = False
            continue

        # 跟踪代码块
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        # 跳过 frontmatter 和代码块内的内容
        if in_frontmatter or in_code_block:
            continue

        # 检查是否包含中文字符
        if has_chinese_chars(line):
            # 截取前100个字符用于显示
            display_line = line.strip()[:100]
            if len(line.strip()) > 100:
                display_line += "..."
            issues.append(f"Line {i:3d}: {display_line}")

    return issues


def main():
    """主函数"""
    oxyapi_dir = Path(
        "/Users/chengkai48/Documents/AI/oxygent-doc-website/content/oxyapi"
    )

    if not oxyapi_dir.exists():
        print(f"❌ Directory not found: {oxyapi_dir}")
        return

    # 获取所有 .mdx 文件
    mdx_files = sorted(oxyapi_dir.glob("*.mdx"))

    print("=" * 80)
    print("🔍 OxyAPI Directory Chinese Content Check")
    print("=" * 80)
    print(f"📁 Checking directory: {oxyapi_dir}")
    print(f"📄 Found {len(mdx_files)} .mdx files")
    print()

    total_issues = 0
    files_with_chinese = 0

    for file_path in mdx_files:
        issues = check_file_chinese(file_path)
        if issues:
            files_with_chinese += 1
            print(f"🇨🇳 {file_path.name}")
            print("-" * 80)
            for issue in issues:
                print(f"  {issue}")
                total_issues += 1
            print()

    print("=" * 80)
    if total_issues == 0:
        print("✅ All API documentation files are in English!")
        print(f"   - Checked {len(mdx_files)} files")
        print(f"   - No Chinese characters found")
    else:
        print(f"⚠️  Found {total_issues} lines with Chinese characters")
        print(f"   - Affected files: {files_with_chinese}/{len(mdx_files)}")
        print(f"   - Files need conversion to English")

    print("=" * 80)

    # 显示需要处理的文件列表
    if files_with_chinese > 0:
        print("\n📋 Files that need English conversion:")
        for file_path in mdx_files:
            issues = check_file_chinese(file_path)
            if issues:
                print(f"  - {file_path.name} ({len(issues)} lines)")


if __name__ == "__main__":
    main()
