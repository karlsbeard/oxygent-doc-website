#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 .zh-CN.mdx 文件中还有哪些英文内容需要翻译
"""

import re
from pathlib import Path

def check_file(file_path):
    """检查单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    lines = content.split('\n')

    # 检查 frontmatter
    in_frontmatter = False
    in_code_block = False
    for i, line in enumerate(lines, 1):
        # 跟踪代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        # 跟踪 frontmatter
        if line.strip() == '---':
            if not in_frontmatter and i <= 5:  # 文件开头的 frontmatter
                in_frontmatter = True
                continue
            elif in_frontmatter:
                in_frontmatter = False
                continue

        # 跳过代码块内的内容
        if in_code_block:
            continue

        # 检查标题行（## 开头）
        if line.strip().startswith('##'):
            # 检查是否包含英文单词（但允许 LLM、MCP、RAG 等缩写）
            if re.search(r'\b(?!LLM|MCP|RAG|MoA|OxyGent|SSE|API|FunctionHub|ReAct|Top-K)[A-Z][a-z]+', line):
                issues.append(f"第 {i} 行 (标题): {line.strip()}")

        # 检查非代码行中的英文句子
        if not in_code_block and not line.strip().startswith('#') and not line.strip().startswith('```'):
            # 查找完整的英文句子（以大写字母开头，以句号结尾）
            if re.search(r'^[A-Z][a-z].*\.$', line.strip()):
                if not any(keyword in line for keyword in ['import', 'from', 'def', 'class', 'return']):
                    issues.append(f"第 {i} 行 (句子): {line.strip()}")

            # 查找英文描述性短语
            if re.search(r'(This example|Follow the|Make sure|To run)', line):
                issues.append(f"第 {i} 行 (短语): {line.strip()}")

    return issues


def main():
    """主函数"""
    examples_dir = Path("/Users/chengkai48/Documents/AI/oxygent-doc-website/content/examples")

    all_files = sorted(examples_dir.glob("*.zh-CN.mdx"))

    total_issues = 0
    for file_path in all_files:
        issues = check_file(file_path)
        if issues:
            print(f"\n文件: {file_path.name}")
            print("-" * 60)
            for issue in issues:
                print(f"  {issue}")
            total_issues += len(issues)

    if total_issues == 0:
        print("\n✅ 所有文件检查完成，未发现需要翻译的英文内容！")
    else:
        print(f"\n⚠️  共发现 {total_issues} 处可能需要翻译的内容。")


if __name__ == "__main__":
    main()
