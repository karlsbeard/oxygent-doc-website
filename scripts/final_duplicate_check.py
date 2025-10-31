#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终检查所有类型的重复内容
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

    # 标准化文本
    def normalize(text):
        text = re.sub(r"[^\w\s]", " ", text.lower())
        text = re.sub(r"\s+", " ", text.strip())
        return text

    desc_norm = normalize(description)
    content_norm = normalize(content_line)

    # 完全相同
    if desc_norm == content_norm:
        return True

    # 关键词重叠检查
    desc_words = set(desc_norm.split())
    content_words = set(content_norm.split())

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

    overlap = len(desc_words & content_words)
    total_unique = len(desc_words | content_words)
    overlap_ratio = overlap / total_unique if total_unique > 0 else 0

    return overlap_ratio > 0.7


def check_all_duplicates(file_path: Path) -> Dict[str, any]:
    """检查所有类型的重复内容"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()
    except Exception as e:
        return {"error": f"Error reading file: {e}"}

    frontmatter, content = parse_frontmatter(original_content)

    if not frontmatter:
        return {"status": "no_frontmatter", "issues": []}

    title = frontmatter.get("title", "")
    description = frontmatter.get("description", "")

    lines = content.split("\n")
    issues = []

    for i, line in enumerate(lines, 1):
        line_stripped = line.strip()

        # 检查重复的 # 标题
        if (
            line_stripped.startswith("# ")
            and title
            and line_stripped[2:].strip() == title
        ):
            issues.append(
                {
                    "type": "exact_title",
                    "line": i,
                    "content": line_stripped,
                    "matches": title,
                }
            )

        # 检查完全重复的描述
        if description and (
            line_stripped == description
            or line_stripped.rstrip(".") == description.rstrip(".")
        ):
            issues.append(
                {
                    "type": "exact_description",
                    "line": i,
                    "content": line_stripped,
                    "matches": description,
                }
            )

        # 检查语义重复的描述
        if (
            description
            and line_stripped
            and is_semantic_duplicate(description, line_stripped)
        ):
            issues.append(
                {
                    "type": "semantic_description",
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
        "issues": issues,
    }


def main():
    """主函数"""
    base_dir = Path("/Users/chengkai48/Documents/AI/oxygent-doc-website/content")

    directories = [base_dir / "oxyapi", base_dir / "examples", base_dir / "docs"]

    print("=" * 80)
    print("🔍 Final Duplicate Content Check")
    print("=" * 80)

    total_files = 0
    total_issues = 0
    files_with_issues = 0

    for directory in directories:
        if not directory.exists():
            print(f"⚠️  Directory not found: {directory}")
            continue

        print(f"\n📁 Checking: {directory.name}/")
        print("-" * 60)

        mdx_files = list(directory.glob("*.mdx"))

        for file_path in sorted(mdx_files):
            total_files += 1
            result = check_all_duplicates(file_path)

            if "error" in result:
                print(f"❌ {file_path.name}: {result['error']}")
            elif result["status"] == "no_frontmatter":
                print(f"⚪ {file_path.name}: No frontmatter")
            elif not result["issues"]:
                print(f"✅ {file_path.name}: Clean")
            else:
                files_with_issues += 1
                issue_count = len(result["issues"])
                total_issues += issue_count
                print(f"⚠️  {file_path.name}: {issue_count} issues found")
                for issue in result["issues"]:
                    print(
                        f"   Line {issue['line']:3d} ({issue['type']}): {issue['content'][:60]}..."
                    )

    print("\n" + "=" * 80)
    print("📊 Final Check Summary:")
    print(f"   - Total files checked: {total_files}")
    print(f"   - Files with issues: {files_with_issues}")
    print(f"   - Total issues found: {total_issues}")

    if total_issues == 0:
        print(f"\n🎉 PERFECT: All files are completely clean!")
        print(f"   No duplicate titles or descriptions found in {total_files} files!")
    else:
        print(
            f"\n⚠️  REMAINING ISSUES: {total_issues} duplicates in {files_with_issues} files"
        )
        print(f"   Consider running additional cleanup scripts")

    print("=" * 80)

    # 按类型统计问题
    if total_issues > 0:
        issue_types = {}
        for directory in directories:
            if directory.exists():
                for file_path in directory.glob("*.mdx"):
                    result = check_all_duplicates(file_path)
                    if result.get("issues"):
                        for issue in result["issues"]:
                            issue_type = issue["type"]
                            issue_types[issue_type] = issue_types.get(issue_type, 0) + 1

        print("\n📊 Issue Types:")
        for issue_type, count in issue_types.items():
            print(f"   - {issue_type}: {count}")


if __name__ == "__main__":
    main()
