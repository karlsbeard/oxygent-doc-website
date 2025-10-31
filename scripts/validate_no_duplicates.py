#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证文档中没有重复的标题和描述
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple


def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """解析 frontmatter 和内容"""
    lines = content.split("\n")

    if not lines[0].strip() == "---":
        return {}, content

    frontmatter = {}
    content_start = 0

    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            content_start = i + 1
            break

        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip().strip("\"'")

    remaining_content = "\n".join(lines[content_start:])
    return frontmatter, remaining_content


def check_duplicates(file_path: Path) -> Dict[str, any]:
    """检查单个文件的重复内容"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()
    except Exception as e:
        return {"error": f"Error reading file: {e}"}

    frontmatter, content = parse_frontmatter(original_content)

    if not frontmatter:
        return {"status": "no_frontmatter", "duplicates": []}

    title = frontmatter.get("title", "")
    description = frontmatter.get("description", "")

    if not title:
        return {"status": "no_title", "duplicates": []}

    lines = content.split("\n")
    duplicates = []

    for i, line in enumerate(lines, 1):
        line_stripped = line.strip()

        # 检查重复的 # 标题
        if line_stripped.startswith("# ") and line_stripped[2:].strip() == title:
            duplicates.append(
                {"type": "title", "line": i, "content": line_stripped, "matches": title}
            )

        # 检查重复的描述
        if description:
            if line_stripped == description or line_stripped.rstrip(
                "."
            ) == description.rstrip("."):
                duplicates.append(
                    {
                        "type": "description",
                        "line": i,
                        "content": line_stripped,
                        "matches": description,
                    }
                )

    return {
        "status": "checked",
        "title": title,
        "description": (
            description[:50] + "..." if len(description) > 50 else description
        ),
        "duplicates": duplicates,
    }


def main():
    """主函数"""
    base_dir = Path("/Users/chengkai48/Documents/AI/oxygent-doc-website/content")

    # 要检查的目录
    directories = [base_dir / "oxyapi", base_dir / "examples", base_dir / "docs"]

    print("=" * 80)
    print("🔍 Validate No Duplicate Titles and Descriptions")
    print("=" * 80)

    total_files = 0
    total_duplicates = 0
    files_with_duplicates = 0

    for directory in directories:
        if not directory.exists():
            print(f"⚠️  Directory not found: {directory}")
            continue

        print(f"\n📁 Checking: {directory.name}/")
        print("-" * 60)

        mdx_files = list(directory.glob("*.mdx"))

        for file_path in sorted(mdx_files):
            total_files += 1
            result = check_duplicates(file_path)

            if "error" in result:
                print(f"❌ {file_path.name}: {result['error']}")
            elif result["status"] == "no_frontmatter":
                print(f"⚪ {file_path.name}: No frontmatter")
            elif result["status"] == "no_title":
                print(f"⚪ {file_path.name}: No title in frontmatter")
            elif not result["duplicates"]:
                print(f"✅ {file_path.name}: No duplicates")
            else:
                files_with_duplicates += 1
                duplicate_count = len(result["duplicates"])
                total_duplicates += duplicate_count
                print(f"⚠️  {file_path.name}: {duplicate_count} duplicates found")
                for dup in result["duplicates"]:
                    print(
                        f"   Line {dup['line']:3d} ({dup['type']}): {dup['content'][:60]}..."
                    )

    print("\n" + "=" * 80)
    print("📊 Validation Summary:")
    print(f"   - Total files checked: {total_files}")
    print(f"   - Files with duplicates: {files_with_duplicates}")
    print(f"   - Total duplicates found: {total_duplicates}")

    if total_duplicates == 0:
        print(f"\n🎉 SUCCESS: No duplicate titles or descriptions found!")
        print(f"   All {total_files} files are clean!")
    else:
        print(
            f"\n⚠️  ISSUES: Found {total_duplicates} duplicates in {files_with_duplicates} files"
        )
        print(f"   Run fix_duplicate_titles.py to fix these issues")

    print("=" * 80)


if __name__ == "__main__":
    main()
