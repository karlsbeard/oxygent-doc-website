#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OxyGent Docs 翻译脚本
将 content/docs/*.mdx 翻译为对应的 .zh-CN.mdx 文件
"""

import os
import re
from pathlib import Path

# 术语翻译映射表
TRANSLATIONS = {
    # 标题和前言
    "Overview": "概述",
    "Quick Start": "快速开始",
    "Configuration Options": "配置选项",
    "API Reference": "API 参考",
    "Usage Example": "使用示例",
    "Examples": "示例",
    "Related Links": "相关链接",
    "Best Practices": "最佳实践",
    "Advanced Features": "高级特性",
    "Getting Started": "入门指南",
    "Core Features": "核心特性",
    "Key Features": "关键特性",
    "When to Use": "何时使用",
    "Use Cases": "使用场景",
    "Why use": "为什么使用",
    "What ": "什么是",
    "How to": "如何",
    "Functionality": "功能",
    "Definition": "定义",
    "Applicable Scenarios": "适用场景",
    "Complete Example": "完整示例",
    "Introduction": "简介",
    
    # 常用词汇
    "Agent": "智能体",
    "Tool": "工具",
    "Flow": "流程",
    "Workflow": "工作流",
    "Configuration": "配置",
    "Parameter": "参数",
    "Method": "方法",
    "Returns": "返回值",
    "Example": "示例",
    "Description": "描述",
    "Default": "默认值",
    "Required": "必需",
    "Optional": "可选",
    "Type": "类型",
    
    # 文档相关
    "For detailed API documentation, see": "详细的 API 文档请参考",
    "For practical examples, see": "实际示例请参考",
    "See all examples": "查看所有示例",
    "Examples Gallery": "示例库",
    
    # 智能体相关
    "Multi-Agent System": "多智能体系统",
    "ReAct": "ReAct",
    "ChatAgent": "ChatAgent",
    "WorkflowAgent": "WorkflowAgent",
    "ParallelAgent": "ParallelAgent",
    "RagAgent": "RagAgent",
    
    # 技术术语
    "Large Language Model": "大语言模型",
    "LLM": "LLM",
    "Reasoning": "推理",
    "Memory": "内存",
    "Context": "上下文",
    "Lifecycle": "生命周期",
    "Visualization": "可视化",
}

def translate_frontmatter(content):
    """翻译 frontmatter"""
    lines = content.split('\n')
    result = []
    in_frontmatter = False
    
    for line in lines:
        if line.strip() == '---':
            result.append(line)
            in_frontmatter = not in_frontmatter
            continue
        
        if in_frontmatter:
            if line.startswith('title:'):
                title = line.replace('title:', '').strip()
                # 翻译标题
                translated_title = translate_text(title)
                result.append(f'title: {translated_title}')
            elif line.startswith('description:'):
                desc = line.replace('description:', '').strip()
                # 翻译描述
                translated_desc = translate_text(desc)
                result.append(f'description: {translated_desc}')
            else:
                result.append(line)
        else:
            result.append(line)
    
    return '\n'.join(result)

def translate_text(text):
    """翻译文本"""
    # 保护代码块和特殊标记
    for key, value in TRANSLATIONS.items():
        # 只翻译非代码上下文中的内容
        if key in text and not ('```' in text or '`' in text):
            text = text.replace(key, value)
    return text

def translate_headers(content):
    """翻译Markdown标题"""
    lines = content.split('\n')
    result = []
    
    header_translations = {
        "Overview": "概述",
        "Quick Start": "快速开始",
        "Configuration Options": "配置选项",
        "API Reference": "API 参考",
        "Usage Example": "使用示例",
        "Examples": "示例",
        "Related Links": "相关链接",
        "Best Practices": "最佳实践",
        "Advanced Features": "高级特性",
        "Complete Example": "完整示例",
        "Introduction": "简介",
        "Functionality": "功能",
        "Definition": "定义",
        "Applicable Scenarios": "适用场景",
        "Basic Usage": "基本用法",
        "Core Parameters": "核心参数",
        "Use Cases": "使用场景",
        "Key Features": "关键特性",
        "When to Use": "何时使用",
    }
    
    for line in lines:
        if line.startswith('#'):
            match = re.match(r'^(#+)\s+(.+)$', line)
            if match:
                level, title = match.groups()
                translated_title = title
                # 翻译标题
                for en, zh in header_translations.items():
                    if title.strip() == en:
                        translated_title = zh
                        break
                result.append(f'{level} {translated_title}')
            else:
                result.append(line)
        else:
            result.append(line)
    
    return '\n'.join(result)

def translate_file(source_file, target_file):
    """翻译单个文件"""
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 翻译 frontmatter
        content = translate_frontmatter(content)
        
        # 2. 翻译标题
        content = translate_headers(content)
        
        # 注意：由于内容复杂，主体翻译保持原样或简单替换
        # 如果需要更复杂的翻译，可以在这里添加
        
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return False

def main():
    """主函数"""
    source_dir = Path("content/docs")
    
    # 获取所有需要翻译的 .mdx 文件
    mdx_files = [f for f in source_dir.glob("*.mdx")
                 if not f.name.endswith(".zh-CN.mdx")]
    
    # 过滤出还没有翻译的文件
    files_to_translate = []
    for mdx_file in mdx_files:
        zh_file = mdx_file.parent / f"{mdx_file.stem}.zh-CN.mdx"
        if not zh_file.exists():
            files_to_translate.append(mdx_file)
    
    print(f"找到 {len(files_to_translate)} 个待翻译文件\n")
    
    success_count = 0
    
    for mdx_file in files_to_translate:
        output_file = mdx_file.parent / f"{mdx_file.stem}.zh-CN.mdx"
        
        print(f"翻译: {mdx_file.name} → {output_file.name}")
        
        if translate_file(mdx_file, output_file):
            print(f"  ✓ 完成\n")
            success_count += 1
        else:
            print(f"  ✗ 失败\n")
    
    print(f"{'='*60}")
    print(f"✅ 翻译完成！成功处理 {success_count}/{len(files_to_translate)} 个文件")

if __name__ == "__main__":
    main()

