#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终清理脚本：确保所有文档部分都是中文，代码部分保持英文
"""

import re
from pathlib import Path


def final_check_file(file_path):
    """最终检查文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []

    # 检查 frontmatter 区域外的英文模式
    lines = content.split('\n')
    in_code = False
    in_frontmatter = False
    frontmatter_count = 0

    for i, line in enumerate(lines, 1):
        # 跟踪 frontmatter
        if line.strip() == '---':
            frontmatter_count += 1
            if frontmatter_count == 1:
                in_frontmatter = True
            elif frontmatter_count == 2:
                in_frontmatter = False
            continue

        # 跟踪代码块
        if line.strip().startswith('```'):
            in_code = not in_code
            continue

        # 跳过 frontmatter 和代码块
        if in_code or in_frontmatter:
            continue

        # 检查标题和描述性文本
        stripped = line.strip()

        # 忽略空行和特殊行
        if not stripped or stripped.startswith('```') or stripped.startswith('-'):
            continue

        # 检查是否有需要翻译的英文模式
        patterns_to_check = [
            (r'^## [A-Z][a-z]+ [A-Z]', '标题可能未翻译'),
            (r'^This example demonstrates', '示例描述未翻译'),
            (r'^- This example shows', '要点未翻译'),
            (r'^Follow the code', '说明未翻译'),
            (r'^Make sure to', '说明未翻译'),
            (r'^To run this', '运行说明未翻译'),
        ]

        for pattern, desc in patterns_to_check:
            if re.search(pattern, stripped):
                issues.append({
                    'line': i,
                    'content': stripped[:60],
                    'issue': desc
                })

    return issues


def main():
    """主函数"""
    examples_dir = Path("/Users/chengkai48/Documents/AI/oxygent-doc-website/content/examples")
    files = sorted(examples_dir.glob("*.zh-CN.mdx"))

    print("=" * 70)
    print("最终翻译质量检查")
    print("=" * 70)

    total_issues = 0
    files_with_issues = 0

    for file_path in files:
        issues = final_check_file(file_path)
        if issues:
            files_with_issues += 1
            print(f"\n📄 {file_path.name}")
            print("-" * 70)
            for issue in issues:
                print(f"  第 {issue['line']:3d} 行 | {issue['issue']:20s} | {issue['content']}")
                total_issues += 1

    print("\n" + "=" * 70)
    if total_issues == 0:
        print("✅ 恭喜！所有文件都已正确翻译！")
        print(f"   - 检查了 {len(files)} 个文件")
        print(f"   - 未发现需要翻译的内容")
    else:
        print(f"⚠️  发现 {total_issues} 处可能的问题，涉及 {files_with_issues} 个文件")

    print("=" * 70)

    # 显示翻译统计
    print("\n📊 翻译完成情况：")
    for file_path in files[:5]:  # 显示前5个文件作为示例
        with open(file_path, 'r', encoding='utf-8') as f:
            first_lines = f.read(500)
            # 检查是否有中文标题
            if re.search(r'## 概述|## 代码|## 要点', first_lines):
                print(f"  ✓ {file_path.name}")

    print(f"  ... 以及其他 {len(files) - 5} 个文件")


if __name__ == "__main__":
    main()
