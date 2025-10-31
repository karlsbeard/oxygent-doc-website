#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复文档中重复的标题和描述问题
- 保留 frontmatter 中的 title 和 description
- 移除重复的 # 标题和描述段落
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


def fix_duplicate_content(file_path: Path) -> Dict[str, any]:
    """修复单个文件的重复内容"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()
    except Exception as e:
        return {"error": f"Error reading file: {e}"}

    frontmatter, content = parse_frontmatter(original_content)

    if not frontmatter:
        return {"status": "no_frontmatter", "changes": 0}

    title = frontmatter.get("title", "")
    description = frontmatter.get("description", "")

    if not title:
        return {"status": "no_title", "changes": 0}

    lines = content.split("\n")
    new_lines = []
    changes = 0
    skip_next_empty = False

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 检查是否是重复的 # 标题
        if line.startswith("# ") and line[2:].strip() == title:
            changes += 1
            skip_next_empty = True
            i += 1
            continue

        # 检查是否是重复的描述段落
        if description and line == description:
            # 检查前面是否有空行，如果有也要跳过
            if new_lines and new_lines[-1].strip() == "":
                new_lines.pop()
            changes += 1
            skip_next_empty = True
            i += 1
            continue

        # 检查是否是重复的描述段落（去掉标点符号的匹配）
        if description and line.rstrip(".") == description.rstrip("."):
            # 检查前面是否有空行，如果有也要跳过
            if new_lines and new_lines[-1].strip() == "":
                new_lines.pop()
            changes += 1
            skip_next_empty = True
            i += 1
            continue

        # 跳过重复标题/描述后的第一个空行
        if skip_next_empty and line == "":
            skip_next_empty = False
            i += 1
            continue

        skip_next_empty = False
        new_lines.append(lines[i])
        i += 1

    if changes > 0:
        # 重建完整内容
        frontmatter_lines = ["---"]
        for key, value in frontmatter.items():
            frontmatter_lines.append(f"{key}: {value}")
        frontmatter_lines.append("---")
        frontmatter_lines.append("")  # 空行分隔

        new_content = "\n".join(frontmatter_lines + new_lines)

        # 写回文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

    return {
        "status": "processed",
        "changes": changes,
        "title": title,
        "description": (
            description[:50] + "..." if len(description) > 50 else description
        ),
    }


def main():
    """主函数"""
    base_dir = Path("/Users/chengkai48/Documents/AI/oxygent-doc-website/content")

    # 要处理的目录
    directories = [base_dir / "oxyapi", base_dir / "examples", base_dir / "docs"]

    print("=" * 80)
    print("🔧 Fix Duplicate Titles and Descriptions")
    print("=" * 80)

    total_files = 0
    total_changes = 0
    files_modified = 0

    for directory in directories:
        if not directory.exists():
            print(f"⚠️  Directory not found: {directory}")
            continue

        print(f"\n📁 Processing: {directory.name}/")
        print("-" * 60)

        mdx_files = list(directory.glob("*.mdx"))

        for file_path in sorted(mdx_files):
            total_files += 1
            result = fix_duplicate_content(file_path)

            if "error" in result:
                print(f"❌ {file_path.name}: {result['error']}")
            elif result["status"] == "no_frontmatter":
                print(f"⚪ {file_path.name}: No frontmatter")
            elif result["status"] == "no_title":
                print(f"⚪ {file_path.name}: No title in frontmatter")
            elif result["changes"] == 0:
                print(f"✅ {file_path.name}: No duplicates found")
            else:
                files_modified += 1
                total_changes += result["changes"]
                print(f"🔧 {file_path.name}: Fixed {result['changes']} duplicates")
                print(f"   Title: {result['title']}")
                print(f"   Desc:  {result['description']}")

    print("\n" + "=" * 80)
    print("📊 Summary:")
    print(f"   - Total files processed: {total_files}")
    print(f"   - Files modified: {files_modified}")
    print(f"   - Total duplicates removed: {total_changes}")

    if files_modified > 0:
        print(f"\n✅ Successfully fixed duplicate content in {files_modified} files!")
    else:
        print(f"\n✅ No duplicate content found!")

    print("=" * 80)


if __name__ == "__main__":
    main()
