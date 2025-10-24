#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译剩余的英文内容
"""

import re
from pathlib import Path

# 需要手动处理的文件和翻译
MANUAL_FIXES = {
    "14_multi-agent.zh-CN.mdx": {
        "title: 多智能体 System": "title: 多智能体系统",
        "本示例演示如何在 OxyGent 中multi-agent system。": "本示例演示如何在 OxyGent 中实现多智能体系统。",
    },
    "09_concurrent-testing.zh-CN.mdx": {
        "title: Concurrent Test Mode": "title: 并发测试模式",
    },
    "10_concurrency-limits.zh-CN.mdx": {
        "title: Limit Concurrency": "title: 并发限制",
    },
    "13_auto-recall-tools.zh-CN.mdx": {
        "title: Auto Recall Top-K Tools": "title: 自动召回 Top-K 工具",
    },
    "15_global-llm-config.zh-CN.mdx": {
        "title: Global LLM Model Configuration": "title: 全局 LLM 模型配置",
    },
    "17_custom-parsing.zh-CN.mdx": {
        "title: 自定义解析 Function": "title: 自定义解析函数",
    },
    "19_user-level-query.zh-CN.mdx": {
        "title: User-Level Query": "title: 用户级查询",
    },
    "21_distributed.zh-CN.mdx": {
        "title: 分布式 System": "title: 分布式系统",
    },
}


def fix_file(file_path, replacements):
    """修复单个文件"""
    print(f"正在处理: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    for old_text, new_text in replacements.items():
        content = content.replace(old_text, new_text)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ 已更新")
        return True
    else:
        print(f"  - 无需更新")
        return False


def main():
    """主函数"""
    examples_dir = Path("/Users/chengkai48/Documents/AI/oxygent-doc-website/content/examples")

    updated_count = 0
    for filename, replacements in MANUAL_FIXES.items():
        file_path = examples_dir / filename
        if file_path.exists():
            if fix_file(file_path, replacements):
                updated_count += 1
        else:
            print(f"文件不存在: {file_path}")

    print(f"\n完成！共更新 {updated_count} 个文件。")


if __name__ == "__main__":
    main()
