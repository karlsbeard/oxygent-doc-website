#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整翻译 content/docs/*.mdx 到中文
这个脚本将提供基础翻译框架，需要后续人工优化
"""

import re
from pathlib import Path

# 完整术语映射
TERM_MAPPING = {
    # 基础术语
    "Overview": "概述",
    "Quick Start": "快速开始",
    "Configuration Options": "配置选项",
    "API Reference": "API 参考",
    "Usage Example": "使用示例",
    "Examples": "示例",
    "Related Links": "相关链接",
    "Best Practices": "最佳实践",
    "Advanced Features": "高级功能",
    "Key Features": "关键特性",
    "When to Use": "何时使用",
    "Use Cases": "使用场景",
    "Definition": "定义",
    "Applicable Scenarios": "适用场景",
    "Complete Example": "完整示例",
    "Introduction": "简介",
    "Functionality": "功能",
    "Basic Usage": "基本用法",
    "Understanding": "理解",
    "Getting Started": "入门指南",
    
    # 组件相关
    "Agent": "智能体",
    "Tool": "工具",
    "Flow": "流程",
    "Workflow": "工作流",
    "Multi-Agent System": "多智能体系统",
    "Large Language Model": "大语言模型",
    
    # 配置相关
    "Parameter": "参数",
    "Method": "方法",
    "Returns": "返回值",
    "Description": "描述",
    "Default": "默认值",
    "Required": "必需",
    "Optional": "可选",
    "Type": "类型",
    
    # 文档结构
    "For practical examples": "实际示例请参考",
    "See all examples": "查看所有示例",
    "For detailed": "详细信息请参考",
    
    # 常用短语
    "provides": "提供",
    "enables": "使您能够",
    "allows": "允许",
    "supports": "支持",
    "includes": "包括",
}

# 句子模板映射
SENTENCE_PATTERNS = {
    r"is a (.+) agent": r"是一个\1智能体",
    r"provides (.+) functionality": r"提供\1功能",
    r"enables you to": r"使您能够",
    r"allows you to": r"允许您",
    r"designed to": r"旨在",
    r"suitable for": r"适用于",
}

def translate_content(content, filename):
    """基础内容翻译 - 提供框架"""
    # 这里提供基础的翻译逻辑
    # 实际翻译需要逐个文件人工完成
    
    # 1. 保护代码块
    code_blocks = []
    def save_code(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"
    
    content = re.sub(r'```[\s\S]*?```', save_code, content)
    
    # 2. 翻译frontmatter
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
                for en, zh in TERM_MAPPING.items():
                    title = title.replace(en, zh)
                result.append(f'title: {title}')
            elif line.startswith('description:'):
                desc = line.replace('description:', '').strip()
                # 保持description的基本翻译
                for en, zh in TERM_MAPPING.items():
                    desc = desc.replace(en, zh)
                result.append(f'description: {desc}')
            else:
                result.append(line)
        else:
            result.append(line)
    
    content = '\n'.join(result)
    
    # 3. 恢复代码块
    for i, block in enumerate(code_blocks):
        content = content.replace(f'__CODE_BLOCK_{i}__', block)
    
    return content

def main():
    print("⚠️ 注意：此脚本仅提供基础翻译框架")
    print("完整的文档翻译需要逐个文件进行人工翻译")
    print("请参考已完成的文件（index.zh-CN.mdx, quick-start.zh-CN.mdx, mas.zh-CN.mdx）")
    print("\n建议：使用AI工具逐个翻译每个文档的完整内容\n")

if __name__ == "__main__":
    main()

