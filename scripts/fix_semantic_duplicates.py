#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复文档中语义相似的重复内容
- 检测 frontmatter description 与内容开头的语义重复
- 移除冗余的描述性段落
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


def is_semantic_duplicate(description: str, content_line: str) -> bool:
    """检查两个句子是否语义重复"""
    if not description or not content_line:
        return False

    # 标准化文本：转小写，移除标点符号
    def normalize(text):
        # 移除标点符号和多余空格
        text = re.sub(r"[^\w\s]", " ", text.lower())
        # 移除多余空格
        text = re.sub(r"\s+", " ", text.strip())
        return text

    desc_norm = normalize(description)
    content_norm = normalize(content_line)

    # 如果完全相同
    if desc_norm == content_norm:
        return True

    # 检查关键词重叠度
    desc_words = set(desc_norm.split())
    content_words = set(content_norm.split())

    # 移除常见的停用词
    stop_words = {
        "a",
        "an",
        "the",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "can",
        "this",
        "that",
        "these",
        "those",
    }

    desc_words -= stop_words
    content_words -= stop_words

    if not desc_words or not content_words:
        return False

    # 计算重叠度
    overlap = len(desc_words & content_words)
    total_unique = len(desc_words | content_words)
    overlap_ratio = overlap / total_unique if total_unique > 0 else 0

    # 如果重叠度超过70%，认为是语义重复
    if overlap_ratio > 0.7:
        return True

    # 特殊模式检测：API 文档描述
    api_patterns = [
        (r"complete.*api.*reference", r"complete.*api.*documentation"),
        (r"api.*reference.*for", r"api.*documentation.*for"),
        (r"complete.*reference", r"complete.*documentation"),
    ]

    for pattern1, pattern2 in api_patterns:
        if (re.search(pattern1, desc_norm) and re.search(pattern2, content_norm)) or (
            re.search(pattern2, desc_norm) and re.search(pattern1, content_norm)
        ):
            return True

    return False


def fix_semantic_duplicates(file_path: Path) -> Dict[str, any]:
    """修复单个文件的语义重复内容"""
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

    if not description:
        return {"status": "no_description", "changes": 0}

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

        # 检查是否是语义重复的描述
        if line and is_semantic_duplicate(description, line):
            # 检查前面是否有空行，如果有也要跳过
            if new_lines and new_lines[-1].strip() == "":
                new_lines.pop()
            changes += 1
            skip_next_empty = True
            i += 1
            continue

        # 跳过重复内容后的第一个空行
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
    print("🔧 Fix Semantic Duplicate Descriptions")
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
            result = fix_semantic_duplicates(file_path)

            if "error" in result:
                print(f"❌ {file_path.name}: {result['error']}")
            elif result["status"] == "no_frontmatter":
                print(f"⚪ {file_path.name}: No frontmatter")
            elif result["status"] == "no_description":
                print(f"⚪ {file_path.name}: No description in frontmatter")
            elif result["changes"] == 0:
                print(f"✅ {file_path.name}: No semantic duplicates found")
            else:
                files_modified += 1
                total_changes += result["changes"]
                print(
                    f"🔧 {file_path.name}: Fixed {result['changes']} semantic duplicates"
                )
                print(f"   Title: {result['title']}")
                print(f"   Desc:  {result['description']}")

    print("\n" + "=" * 80)
    print("📊 Summary:")
    print(f"   - Total files processed: {total_files}")
    print(f"   - Files modified: {files_modified}")
    print(f"   - Total semantic duplicates removed: {total_changes}")

    if files_modified > 0:
        print(f"\n✅ Successfully fixed semantic duplicates in {files_modified} files!")
    else:
        print(f"\n✅ No semantic duplicates found!")

    print("=" * 80)


if __name__ == "__main__":
    main()
