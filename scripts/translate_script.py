#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量翻译 .zh-CN.mdx 文件中的英文说明为中文
保持代码为英文，代码注释保持中文
"""

import re
import os
from pathlib import Path

# 翻译映射表
TRANSLATIONS = {
    # 标题翻译
    "RAG Implementation": "RAG 实现",
    "MoA Simple Implementation": "MoA 简单实现",
    "FunctionHub Tools": "FunctionHub 工具",
    "Local MCP Tools": "本地 MCP 工具",
    "SSE MCP Tools": "SSE MCP 工具",
    "External MCP Tools": "外部 MCP 工具",
    "Concurrent Testing": "并发测试",
    "Concurrency Limits": "并发限制",
    "Production Config": "生产环境配置",
    "Multi-Environment Config": "多环境配置",
    "Multi-Agent": "多智能体",
    "Auto Recall Tools": "自动召回工具",
    "Multi-Level Agents": "多层级智能体",
    "Global LLM Config": "全局 LLM 配置",
    "Custom Parsing": "自定义解析",
    "Workflow": "工作流",
    "User Level Query": "用户级查询",
    "Reflexion": "反思",
    "Multimodal": "多模态",
    "Distributed": "分布式",

    # 常用短语翻译
    "## Overview": "## 概述",
    "## Code": "## 代码",
    "## Key Points": "## 要点",
    "## Running the Example": "## 运行示例",
    "To run this example:": "运行此示例：",

    # 句子翻译
    "This example demonstrates": "本示例演示如何在 OxyGent 中",
    " in OxyGent.": "。",
    "- This example shows how to use OxyGent for ": "- 本示例展示如何使用 OxyGent ",
    "- Follow the code comments for detailed explanations": "- 请按照代码注释获取详细说明",
    "- Make sure to set up your environment variables before running": "- 运行前请确保已设置好环境变量",
}

# 特定功能的翻译
FEATURE_TRANSLATIONS = {
    "rag implementation": "实现 RAG",
    "moa simple implementation": "实现 MoA 简单版本",
    "functionhub tools": "使用 FunctionHub 工具",
    "local mcp tools": "使用本地 MCP 工具",
    "sse mcp tools": "使用 SSE MCP 工具",
    "external mcp tools": "使用外部 MCP 工具",
    "concurrent testing": "进行并发测试",
    "concurrency limits": "设置并发限制",
    "production config": "配置生产环境",
    "multi-environment config": "配置多环境",
    "multi-agent": "实现多智能体",
    "auto recall tools": "使用自动召回工具",
    "multi-level agents": "实现多层级智能体",
    "global llm config": "配置全局 LLM",
    "custom parsing": "实现自定义解析",
    "workflow": "实现工作流",
    "user level query": "实现用户级查询",
    "reflexion": "实现反思机制",
    "multimodal": "实现多模态",
    "distributed": "实现分布式系统",
}


def translate_file(file_path):
    """翻译单个文件"""
    print(f"正在处理: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. 翻译 frontmatter 中的 title
    for en, zh in TRANSLATIONS.items():
        if en.startswith("title:") or not en.startswith("#"):
            content = content.replace(f"title: {en}", f"title: {zh}")

    # 2. 翻译标题（## 开头的部分）
    for en, zh in TRANSLATIONS.items():
        if en.startswith("##"):
            content = content.replace(en, zh)

    # 3. 翻译 Overview 部分的句子
    # 匹配 "This example demonstrates XXX in OxyGent."
    pattern = r'This example demonstrates (.*?) in OxyGent\.'

    def replace_overview(match):
        feature = match.group(1)
        feature_lower = feature.lower()
        if feature_lower in FEATURE_TRANSLATIONS:
            return f"本示例演示如何在 OxyGent 中{FEATURE_TRANSLATIONS[feature_lower]}。"
        else:
            return f"本示例演示如何在 OxyGent 中{feature}。"

    content = re.sub(pattern, replace_overview, content)

    # 4. 翻译 Key Points 部分
    # 匹配 "- This example shows how to use OxyGent for XXX"
    pattern2 = r'- This example shows how to use OxyGent for (.*?)$'

    def replace_keypoint(match):
        feature = match.group(1)
        feature_lower = feature.lower()
        if feature_lower in FEATURE_TRANSLATIONS:
            return f"- 本示例展示如何使用 OxyGent {FEATURE_TRANSLATIONS[feature_lower]}"
        else:
            return f"- 本示例展示如何使用 OxyGent {feature}"

    content = re.sub(pattern2, replace_keypoint, content, flags=re.MULTILINE)

    # 5. 翻译其他常用短语
    content = content.replace("- Follow the code comments for detailed explanations",
                            "- 请按照代码注释获取详细说明")
    content = content.replace("- Make sure to set up your environment variables before running",
                            "- 运行前请确保已设置好环境变量")
    content = content.replace("To run this example:", "运行此示例：")

    # 只有在内容发生变化时才写入
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

    # 获取所有 .zh-CN.mdx 文件（排除已完成的前3个）
    files_to_translate = [
        "04_moa-implementation.zh-CN.mdx",
        "05_functionhub-tools.zh-CN.mdx",
        "06_local-mcp-tools.zh-CN.mdx",
        "07_sse-mcp-tools.zh-CN.mdx",
        "08_external-mcp-tools.zh-CN.mdx",
        "09_concurrent-testing.zh-CN.mdx",
        "10_concurrency-limits.zh-CN.mdx",
        "11_production-config.zh-CN.mdx",
        "12_multi-environment-config.zh-CN.mdx",
        "13_auto-recall-tools.zh-CN.mdx",
        "14_multi-agent.zh-CN.mdx",
        "15_global-llm-config.zh-CN.mdx",
        "16_multi-level-agents.zh-CN.mdx",
        "17_custom-parsing.zh-CN.mdx",
        "18_workflow.zh-CN.mdx",
        "19_user-level-query.zh-CN.mdx",
        "20_reflexion.zh-CN.mdx",
        "21_distributed.zh-CN.mdx",
        "22_multimodal.zh-CN.mdx",
    ]

    updated_count = 0
    for filename in files_to_translate:
        file_path = examples_dir / filename
        if file_path.exists():
            if translate_file(file_path):
                updated_count += 1
        else:
            print(f"文件不存在: {file_path}")

    print(f"\n完成！共更新 {updated_count} 个文件。")


if __name__ == "__main__":
    main()
