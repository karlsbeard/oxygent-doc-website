#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度翻译 Docs 文档
基于成功的 oxyapi 翻译脚本改造，用于 content/docs/*.mdx
完整翻译所有英文内容为中文
"""

import re
from pathlib import Path

# 完整的文档翻译映射表（基于 oxyapi 翻译经验）
DOC_TRANSLATIONS = {
    # ====== 标题和章节 ======
    "Overview": "概述",
    "Quick Start": "快速开始",
    "Configuration Options": "配置选项",
    "API Reference": "API 参考",
    "Usage Example": "使用示例",
    "Usage Examples": "使用示例",
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
    "Core Concepts": "核心概念",
    "What ": "什么是 ",
    "Why use": "为什么使用",
    "What is": "什么是",
    "How to": "如何",
    "Understanding the": "理解",
    
    # ====== 核心术语 ======
    "Agent": "智能体",
    "Agents": "智能体",
    "Tool": "工具",
    "Tools": "工具",
    "Flow": "流程",
    "Flows": "流程",
    "Workflow": "工作流",
    "Multi-Agent System": "多智能体系统",
    "Large Language Model": "大语言模型",
    "LLM": "LLM",
    "Reasoning": "推理",
    "Memory": "内存",
    "Context": "上下文",
    "Lifecycle": "生命周期",
    "Visualization": "可视化",
    "Configuration": "配置",
    "Scope": "域",
    "Request": "请求",
    "Response": "响应",
    "Session": "会话",
    
    # ====== 参数和配置相关 ======
    "Parameter": "参数",
    "Parameters": "参数",
    "Method": "方法",
    "Methods": "方法",
    "Returns": "返回值",
    "Description": "描述",
    "Default": "默认值",
    "Required": "必需",
    "Optional": "可选",
    "Type": "类型",
    "Value": "值",
    
    # ====== 常用动词和短语 ======
    "provides": "提供",
    "enables": "使",
    "enables you to": "使您能够",
    "allows": "允许",
    "allows you to": "允许您",
    "supports": "支持",
    "includes": "包括",
    "designed to": "旨在",
    "suitable for": "适用于",
    "ideal for": "适合",
    "used for": "用于",
    "responsible for": "负责",
    "manages": "管理",
    "handles": "处理",
    "executes": "执行",
    "processes": "处理",
    "coordinates": "协调",
    "integrates": "集成",
    "implements": "实现",
    
    # ====== 句子模板 ======
    "is a": "是一个",
    "is the": "是",
    "are the": "是",
    "can be": "可以",
    "will be": "将",
    "should be": "应该",
    "must be": "必须",
    "may be": "可能",
    "for example": "例如",
    "such as": "例如",
    "like": "如",
    "including": "包括",
    "with the": "使用",
    "through the": "通过",
    "by the": "通过",
    "in the": "在",
    "on the": "在",
    "at the": "在",
    "to the": "到",
    "from the": "从",
    
    # ====== 文档结构相关 ======
    "For practical examples": "实际示例请参考",
    "For detailed": "详细信息请参考",
    "See all examples": "查看所有示例",
    "Examples Gallery": "示例库",
    "Learn more": "了解更多",
    "Read more": "阅读更多",
    "Check out": "查看",
    "Explore": "探索",
    "Dive deeper": "深入了解",
    "Note": "注意",
    "Important": "重要",
    "Warning": "警告",
    "Tip": "提示",
    
    # ====== 智能体相关完整句子 ======
    "is a conversational agent": "是一个对话智能体",
    "implements the ReAct paradigm": "实现了 ReAct 范式",
    "designed to handle": "旨在处理",
    "provides functionality for": "提供以下功能",
    "enables autonomous behavior": "实现自主行为",
    "coordinates communication": "协调通信",
    "manages conversation history": "管理对话历史",
    "processes user queries": "处理用户查询",
    "generates responses": "生成响应",
    
    # ====== 配置和参数描述 ======
    "Configure the": "配置",
    "Set the": "设置",
    "Specify the": "指定",
    "Define the": "定义",
    "Provide the": "提供",
    "Pass the": "传递",
    "Update the": "更新",
    "Override the": "覆盖",
    "Customize the": "自定义",
    
    # ====== 代码相关（但不翻译代码本身）======
    "The following example": "以下示例",
    "Here is an example": "这是一个示例",
    "Example code": "示例代码",
    "Usage example": "使用示例",
    "Basic example": "基本示例",
    "Advanced example": "高级示例",
    "Complete example": "完整示例",
}

# 特定段落和完整句子的翻译
FULL_SENTENCE_TRANSLATIONS = {
    # Visualization 相关
    "OxyGent provides powerful visualization capabilities that help developers understand, debug, and monitor multi-agent system execution in real-time through an interactive web interface and automated flow chart generation.":
        "OxyGent 提供强大的可视化功能，帮助开发者通过交互式 Web 界面和自动流程图生成，实时理解、调试和监控多智能体系统的执行情况。",
    
    "The visualization system in OxyGent enables you to:":
        "OxyGent 中的可视化系统使您能够：",
    
    "Track agent execution, message flow, and system state through an interactive web interface":
        "通过交互式 Web 界面跟踪智能体执行、消息流和系统状态",
    
    "View the hierarchical structure of agents, tools, and their relationships":
        "查看智能体、工具及其关系的层次结构",
    
    "Automatically generate visual flowcharts of agent workflows and decision processes":
        "自动生成智能体工作流和决策过程的可视化流程图",
    
    "Step through execution history with playback controls for debugging":
        "通过播放控件逐步浏览执行历史以进行调试",
    
    "Review complete interaction logs with context and state information":
        "查看包含上下文和状态信息的完整交互日志",
    
    # Four-Scope 相关
    "OxyGent implements a sophisticated four-scope system for managing data, context, and state across different levels of the multi-agent system.":
        "OxyGent 实现了一个复杂的四域系统，用于管理多智能体系统不同层级的数据、上下文和状态。",
    
    "This hierarchical scoping enables precise control over data visibility, lifetime, and sharing patterns between agents.":
        "这种分层域使得能够精确控制智能体之间的数据可见性、生命周期和共享模式。",
    
    # ChatAgent 相关
    "is a conversational agent module in the OxyGent framework, designed to handle dialogue interactions with language models.":
        "是 OxyGent 框架中的对话智能体模块，旨在处理与语言模型的对话交互。",
    
    "It inherits from the LocalAgent class and provides functionality for managing conversation memory, processing user queries, and coordinating with language models to generate responses.":
        "它继承自 LocalAgent 类，提供管理对话记忆、处理用户查询以及协调语言模型生成响应的功能。",
    
    "is the most basic conversational agent in the OxyGent framework, with the following key features:":
        "是 OxyGent 框架中最基础的对话智能体，具有以下关键特性：",
    
    "Maintains conversation history, supporting multi-turn dialogues":
        "维护对话历史，支持多轮对话",
    
    "Default prompt is \"You are a helpful assistant.\", which can be customized":
        "默认提示词为 \"You are a helpful assistant.\"，可以自定义",
    
    "Coordinates communication with the underlying language model":
        "协调与底层语言模型的通信",
    
    "Supports passing custom parameters to the language model":
        "支持向语言模型传递自定义参数",
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
    """翻译普通文本"""
    # 先尝试完整句子翻译
    for en_sentence, zh_sentence in FULL_SENTENCE_TRANSLATIONS.items():
        if en_sentence in text:
            text = text.replace(en_sentence, zh_sentence)
    
    # 再进行词汇级别的翻译
    for en_term, zh_term in DOC_TRANSLATIONS.items():
        # 使用正则表达式进行单词边界匹配（避免部分替换）
        # 但对于某些短语，直接替换
        text = text.replace(en_term, zh_term)
    
    return text

def translate_headers(content):
    """翻译 Markdown 标题"""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        if line.startswith('#'):
            match = re.match(r'^(#+)\s+(.+)$', line)
            if match:
                level, title = match.groups()
                translated_title = translate_text(title)
                result.append(f'{level} {translated_title}')
            else:
                result.append(line)
        else:
            result.append(line)
    
    return '\n'.join(result)

def translate_content_body(content):
    """翻译正文内容，保护代码块"""
    # 保护代码块
    code_blocks = []
    def save_code(match):
        code_blocks.append(match.group(0))
        return f'__CODE_BLOCK_{len(code_blocks)-1}__'
    
    content = re.sub(r'```[\s\S]*?```', save_code, content)
    
    # 翻译非代码部分
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # 如果是代码块占位符，不翻译
        if '__CODE_BLOCK_' in line:
            result.append(line)
            continue
        
        # 如果是空行或只有标点，不翻译
        if not line.strip() or line.strip() in ['|', '-', '*']:
            result.append(line)
            continue
        
        # 翻译这一行
        translated_line = translate_text(line)
        result.append(translated_line)
    
    content = '\n'.join(result)
    
    # 恢复代码块
    for i, code_block in enumerate(code_blocks):
        content = content.replace(f'__CODE_BLOCK_{i}__', code_block)
    
    return content

def translate_file(source_file, target_file):
    """翻译单个文件"""
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"正在翻译: {source_file.name}")
        
        # 1. 翻译 frontmatter
        content = translate_frontmatter(content)
        
        # 2. 翻译标题
        content = translate_headers(content)
        
        # 3. 翻译正文
        content = translate_content_body(content)
        
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ 完成: {target_file.name}\n")
        return True
        
    except Exception as e:
        print(f"  ✗ 错误: {e}\n")
        return False

def main():
    """主函数"""
    source_dir = Path("content/docs")
    
    # 获取所有需要翻译的 .mdx 文件
    mdx_files = [f for f in source_dir.glob("*.mdx")
                 if not f.name.endswith(".zh-CN.mdx")]
    
    # 排除已经手动翻译的文件
    manually_translated = [
        "index.mdx",
        "quick-start.mdx", 
        "mas.mdx",
        "visualization.mdx",
        "agents-chat.mdx"
    ]
    
    files_to_translate = [f for f in mdx_files 
                          if f.name not in manually_translated]
    
    print(f"找到 {len(files_to_translate)} 个待翻译文件")
    print(f"(已排除 {len(manually_translated)} 个已手动翻译的文件)\n")
    
    success_count = 0
    
    for mdx_file in sorted(files_to_translate):
        output_file = mdx_file.parent / f"{mdx_file.stem}.zh-CN.mdx"
        
        if translate_file(mdx_file, output_file):
            success_count += 1
    
    print(f"{'='*60}")
    print(f"✅ 翻译完成！成功处理 {success_count}/{len(files_to_translate)} 个文件")
    print(f"\n提示：翻译后建议人工检查以下内容：")
    print(f"  1. 术语一致性")
    print(f"  2. 句子流畅度")
    print(f"  3. 代码示例中的注释（如需翻译）")
    print(f"  4. 链接和引用的准确性")

if __name__ == "__main__":
    main()

