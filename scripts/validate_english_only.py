#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证 oxyapi 目录完全英文化的脚本
"""

import re
import json
from pathlib import Path


def has_chinese_chars(text):
    """检查文本是否包含中文字符"""
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def check_mdx_file(file_path):
    """检查 MDX 文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"error": str(e)}

    lines = content.split("\n")
    chinese_lines = []

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

        # 跳过 frontmatter 和代码块
        if in_frontmatter or in_code_block:
            continue

        # 检查中文字符
        if has_chinese_chars(line):
            chinese_lines.append(i)

    return {
        "total_lines": len(lines),
        "chinese_lines": chinese_lines,
        "is_english_only": len(chinese_lines) == 0,
    }


def check_json_file(file_path):
    """检查 JSON 文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            data = json.loads(content)
    except Exception as e:
        return {"error": str(e)}

    # 检查 JSON 内容是否包含中文
    content_str = json.dumps(data, ensure_ascii=False)
    has_chinese = has_chinese_chars(content_str)

    return {
        "has_chinese": has_chinese,
        "is_english_only": not has_chinese,
        "content_preview": (
            content_str[:200] + "..." if len(content_str) > 200 else content_str
        ),
    }


def main():
    """主函数"""
    oxyapi_dir = Path(
        "/Users/chengkai48/Documents/AI/oxygent-doc-website/content/oxyapi"
    )

    print("=" * 80)
    print("🔍 OxyAPI Directory English-Only Validation")
    print("=" * 80)

    if not oxyapi_dir.exists():
        print(f"❌ Directory not found: {oxyapi_dir}")
        return

    # 检查所有文件
    mdx_files = list(oxyapi_dir.glob("*.mdx"))
    json_files = list(oxyapi_dir.glob("*.json"))

    print(f"📁 Directory: {oxyapi_dir}")
    print(f"📄 MDX files: {len(mdx_files)}")
    print(f"📄 JSON files: {len(json_files)}")
    print()

    # 检查 MDX 文件
    print("📝 MDX Files Analysis:")
    print("-" * 40)

    mdx_issues = 0
    for file_path in sorted(mdx_files):
        result = check_mdx_file(file_path)
        if "error" in result:
            print(f"❌ {file_path.name}: {result['error']}")
            mdx_issues += 1
        elif result["is_english_only"]:
            print(f"✅ {file_path.name}: English only ({result['total_lines']} lines)")
        else:
            print(
                f"⚠️  {file_path.name}: Contains Chinese (lines: {result['chinese_lines']})"
            )
            mdx_issues += 1

    print()

    # 检查 JSON 文件
    print("📋 JSON Files Analysis:")
    print("-" * 40)

    json_issues = 0
    for file_path in sorted(json_files):
        result = check_json_file(file_path)
        if "error" in result:
            print(f"❌ {file_path.name}: {result['error']}")
            json_issues += 1
        elif result["is_english_only"]:
            print(f"✅ {file_path.name}: English only")
        else:
            print(f"⚠️  {file_path.name}: Contains Chinese")
            print(f"   Preview: {result['content_preview']}")
            json_issues += 1

    print()

    # 总结
    print("=" * 80)
    total_files = len(mdx_files) + len(json_files)
    total_issues = mdx_issues + json_issues

    if total_issues == 0:
        print("🎉 SUCCESS: All files are English-only!")
        print(f"   - Checked {total_files} files")
        print(f"   - {len(mdx_files)} MDX files: All English")
        print(f"   - {len(json_files)} JSON files: All English")
    else:
        print(f"⚠️  ISSUES FOUND: {total_issues} files need attention")
        print(f"   - MDX files with issues: {mdx_issues}")
        print(f"   - JSON files with issues: {json_issues}")

    print("=" * 80)

    # 显示文件列表
    print("\n📋 File Inventory:")
    print("MDX Files:")
    for file_path in sorted(mdx_files):
        print(f"  - {file_path.name}")

    print("JSON Files:")
    for file_path in sorted(json_files):
        print(f"  - {file_path.name}")


if __name__ == "__main__":
    main()
