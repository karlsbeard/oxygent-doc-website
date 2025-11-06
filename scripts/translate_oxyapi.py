#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OxyAPI 文档翻译脚本
将 content/oxyapi/*.mdx 翻译为对应的 .zh-CN.mdx 文件
"""

import os
import re
from pathlib import Path

# 术语翻译映射表
TERM_TRANSLATIONS = {
    # Frontmatter
    "API Reference": "API 参考",
    "Complete API reference for": "完整 API 参考文档：",
    "Complete API documentation for": "完整 API 文档：",
    "constructor parameters and methods": "构造函数参数和方法",
    
    # 标题
    "Constructor Parameters": "构造函数参数",
    "Core Parameters": "核心参数",
    "Execution Parameters": "执行参数",
    "Memory Parameters": "内存参数",
    "Configuration Parameters": "配置参数",
    "Callback Parameters": "回调参数",
    "Advanced Parameters": "高级参数",
    "Parameter Details": "参数详情",
    "Methods": "方法",
    "Usage Guidelines": "使用指南",
    "Related Documentation": "相关文档",
    "Quick Start": "快速开始",
    "API Conventions": "API 约定",
    "Getting Help": "获取帮助",
    "Overview": "概述",
    
    # 章节名称
    "Agents": "代理",
    "Flows": "流程",
    "Tools": "工具",
    "LLMs": "大语言模型",
    
    # 表格标题
    "Parameter": "参数",
    "Type": "类型",
    "Default": "默认值",
    "Description": "描述",
    "Required": "必需",
    "Returns": "返回值",
    "Example": "示例",
    "Parameters": "参数",
    
    # 常用词汇
    "Yes": "是",
    "No": "否",
    "None": "无",
    "Optional": "可选",
    "required": "必需",
    "optional": "可选",
}

# 句子翻译映射
SENTENCE_TRANSLATIONS = {
    "Agents are the core components of the OxyGent framework, responsible for executing specific tasks and making decisions.": 
        "代理是 OxyGent 框架的核心组件，负责执行特定任务和做出决策。",
    
    "Flow components define the execution logic and decision-making processes of agents.":
        "流程组件定义了代理的执行逻辑和决策过程。",
    
    "LLM components provide integration interfaces with various large language model services.":
        "大语言模型组件提供了与各种大语言模型服务的集成接口。",
    
    "Tool components provide agents with the ability to interact with external systems.":
        "工具组件为代理提供了与外部系统交互的能力。",
    
    "If you're new to the OxyGent API, we recommend starting with the following steps:":
        "如果您是 OxyGent API 的新手，我们建议从以下步骤开始：",
    
    "All OxyGent APIs follow these conventions:":
        "所有 OxyGent API 都遵循以下约定：",
    
    "If you encounter issues while using the API, you can:":
        "如果您在使用 API 时遇到问题，可以：",
    
    "Check out": "查看",
    "to understand basic agent usage": "以了解基本的代理使用方法",
    "to understand how to configure large language models": "以了解如何配置大语言模型",
    "to understand the tool system": "以了解工具系统",
    
    "Refer to specific component API documentation": "参考特定组件的 API 文档",
    "Review code examples and best practices": "查看代码示例和最佳实践",
    "Check the error handling and troubleshooting sections": "查看错误处理和故障排除章节",
    
    # API 文档特有句子
    "Unique identifier for the agent": "代理的唯一标识符",
    "Whether this is the entry point agent": "此代理是否为入口代理",
    "Name of LLM component to use": "要使用的大语言模型组件名称",
    "List of tool names": "工具名称列表",
    "List of sub-agent names": "子代理名称列表",
    "Maximum reasoning-acting iterations": "最大推理-行动迭代次数",
    "Discard detailed ReAct memory": "丢弃详细的 ReAct 内存",
    "Number of historical conversations to keep": "保留的历史对话数量",
    "Maximum tokens for memory storage": "内存存储的最大令牌数",
    "Weight for short-term memory in scoring": "短期内存在评分中的权重",
    "Weight for ReAct memory in scoring": "ReAct 内存在评分中的权重",
    
    # 通用描述
    "A unique identifier for": "的唯一标识符",
    "within the MAS": "在多智能体系统中",
    "Multi-Agent System": "多智能体系统",
    "This name is used when calling": "调用时使用此名称",
    "Indicates whether": "指示是否",
    "Only one agent should be marked as master": "只有一个代理应标记为主代理",
    "Name reference to an LLM component": "对大语言模型组件的名称引用",
    "registered in the same MAS": "在同一多智能体系统中注册",
    "This LLM will be used for": "此大语言模型将用于",
    "all reasoning steps": "所有推理步骤",
    "that the agent can invoke": "代理可以调用的",
    "Tools must be registered": "工具必须注册",
    "that this agent can delegate tasks to": "此代理可以将任务委托给的",
    "Sub-agents must be registered": "子代理必须注册",
    "Maximum number of": "最大数量",
    "before the agent uses fallback mechanisms": "在代理使用后备机制之前",
    "Each round consists of": "每一轮包括",
    "one reasoning step and one or more tool executions": "一个推理步骤和一个或多个工具执行",
    
    # 列表项
    "Simple tasks": "简单任务",
    "Multi-step tasks": "多步骤任务",
    "Complex reasoning chains": "复杂推理链",
    "rounds": "轮",
    
    # 内存相关
    "Controls memory retention strategy": "控制内存保留策略",
    "Keep only final question-answer pairs": "仅保留最终问答对",
    "cleaner history": "更清晰的历史",
    "Retain full ReAct reasoning traces": "保留完整的 ReAct 推理轨迹",
    "with weighted scoring": "使用加权评分",
    "Number of recent conversation turns": "最近对话轮次的数量",
    "to keep in short-term memory": "保留在短期内存中",
    "Maximum token limit for the memory system": "内存系统的最大令牌限制",
    "When exceeded, older memories are pruned": "超出时，较旧的内存将被修剪",
    "based on weighted scoring": "基于加权评分",
    "Relative importance weight for": "相对重要性权重",
    "when": "当",
    "Higher values give more importance to": "较高的值会更重视",
    "recent conversations": "最近的对话",
    "for ReAct intermediate steps": "用于 ReAct 中间步骤",
    
    # 方法相关
    "Execute the agent with given input": "使用给定输入执行代理",
    "List of message dictionaries": "消息字典列表",
    "with": "包含",
    "and": "和",
    "fields": "字段",
    "Additional LLM parameters can be passed through": "可以传递额外的大语言模型参数",
    "object containing": "对象，包含",
    "Final agent response": "最终代理响应",
    "Full conversation history": "完整对话历史",
    "Execution metadata": "执行元数据",
}

# API 文档链接描述翻译
LINK_DESCRIPTIONS = {
    "Chat-based agent API documentation": "基于聊天的代理 API 文档",
    "Parallel agent API documentation": "并行代理 API 文档",
    "Retrieval-Augmented Generation agent API documentation": "检索增强生成代理 API 文档",
    "ReAct pattern-based agent API documentation": "基于 ReAct 模式的代理 API 文档",
    "Server-Sent Events agent API documentation": "服务器发送事件代理 API 文档",
    "Workflow agent API documentation": "工作流代理 API 文档",
    
    "Workflow flow API documentation": "工作流流程 API 文档",
    "Parallel flow API documentation": "并行流程 API 文档",
    "Plan-and-solve flow API documentation": "计划与求解流程 API 文档",
    "Reflexion flow API documentation": "反思流程 API 文档",
    
    "HTTP-based large language model API documentation": "基于 HTTP 的大语言模型 API 文档",
    
    "Function hub API documentation": "函数中心 API 文档",
    "MCP standard input/output tool API documentation": "MCP 标准输入/输出工具 API 文档",
    "MCP Server-Sent Events tool API documentation": "MCP 服务器发送事件工具 API 文档",
    "MCP streamable tool API documentation": "MCP 流式工具 API 文档",
    
    # Related Documentation
    "Usage guide and examples": "使用指南和示例",
    "API reference for": "API 参考文档：",
    "Available tools documentation": "可用工具文档",
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
                translated_title = title
                for en, zh in TERM_TRANSLATIONS.items():
                    translated_title = translated_title.replace(en, zh)
                result.append(f'title: {translated_title}')
            elif line.startswith('description:'):
                desc = line.replace('description:', '').strip()
                # 翻译描述
                translated_desc = desc
                for en, zh in TERM_TRANSLATIONS.items():
                    translated_desc = translated_desc.replace(en, zh)
                for en, zh in SENTENCE_TRANSLATIONS.items():
                    translated_desc = translated_desc.replace(en, zh)
                result.append(f'description: {translated_desc}')
            else:
                result.append(line)
        else:
            result.append(line)
    
    return '\n'.join(result)

def translate_headers(content):
    """翻译标题"""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        if line.startswith('#'):
            # 提取标题级别和内容
            match = re.match(r'^(#+)\s+(.+)$', line)
            if match:
                level, title = match.groups()
                translated_title = title
                # 先翻译术语
                for en, zh in TERM_TRANSLATIONS.items():
                    translated_title = translated_title.replace(en, zh)
                result.append(f'{level} {translated_title}')
            else:
                result.append(line)
        else:
            result.append(line)
    
    return '\n'.join(result)

def translate_table_headers(content):
    """翻译表格标题行"""
    lines = content.split('\n')
    result = []
    
    for i, line in enumerate(lines):
        # 检测表格标题行
        if '|' in line and i + 1 < len(lines) and '|---' in lines[i + 1]:
            # 这是表格标题行
            cells = [cell.strip() for cell in line.split('|')]
            translated_cells = []
            for cell in cells:
                translated_cell = cell
                for en, zh in TERM_TRANSLATIONS.items():
                    if cell == en:
                        translated_cell = zh
                        break
                translated_cells.append(translated_cell)
            result.append('|'.join(translated_cells))
        else:
            result.append(line)
    
    return '\n'.join(result)

def translate_list_items(content):
    """翻译列表项"""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        if line.strip().startswith(('- ', '* ', '1. ', '2. ', '3. ', '4. ', '5. ')):
            translated_line = line
            # 翻译链接描述
            for en, zh in LINK_DESCRIPTIONS.items():
                translated_line = translated_line.replace(en, zh)
            # 翻译句子
            for en, zh in SENTENCE_TRANSLATIONS.items():
                translated_line = translated_line.replace(en, zh)
            result.append(translated_line)
        else:
            result.append(line)
    
    return '\n'.join(result)

def translate_paragraphs(content):
    """翻译段落"""
    # 保护代码块
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f'__CODE_BLOCK_{len(code_blocks) - 1}__'
    
    # 提取代码块
    content = re.sub(r'```[\s\S]*?```', save_code_block, content)
    
    # 翻译普通段落
    lines = content.split('\n')
    result = []
    
    for line in lines:
        if line.strip() and not line.strip().startswith(('#', '|', '-', '*', '```', '1.', '2.', '3.', '4.', '5.')):
            translated_line = line
            # 翻译完整句子
            for en, zh in SENTENCE_TRANSLATIONS.items():
                translated_line = translated_line.replace(en, zh)
            result.append(translated_line)
        else:
            result.append(line)
    
    content = '\n'.join(result)
    
    # 恢复代码块
    for i, code_block in enumerate(code_blocks):
        content = content.replace(f'__CODE_BLOCK_{i}__', code_block)
    
    return content

def translate_inline_descriptions(content):
    """翻译行内描述（表格中的描述列等）"""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        if '|' in line and not '|---' in line:
            # 可能是表格数据行
            translated_line = line
            for en, zh in SENTENCE_TRANSLATIONS.items():
                translated_line = translated_line.replace(en, zh)
            result.append(translated_line)
        else:
            result.append(line)
    
    return '\n'.join(result)

def translate_content(content, filename):
    """翻译文件内容"""
    print(f"  翻译内容...")
    
    # 1. 翻译 frontmatter
    content = translate_frontmatter(content)
    
    # 2. 翻译标题
    content = translate_headers(content)
    
    # 3. 翻译表格标题
    content = translate_table_headers(content)
    
    # 4. 翻译列表项
    content = translate_list_items(content)
    
    # 5. 翻译行内描述
    content = translate_inline_descriptions(content)
    
    # 6. 翻译段落
    content = translate_paragraphs(content)
    
    return content

def main():
    """主函数"""
    source_dir = Path("/Users/chengkai48/Documents/AI/oxygent-doc-website/content/oxyapi")
    
    # 获取所有 .mdx 文件（排除 .zh-CN.mdx）
    mdx_files = [f for f in source_dir.glob("*.mdx")
                 if not f.name.endswith(".zh-CN.mdx")]
    
    print(f"找到 {len(mdx_files)} 个待翻译文件\n")
    
    success_count = 0
    
    for mdx_file in mdx_files:
        output_file = mdx_file.parent / f"{mdx_file.stem}.zh-CN.mdx"
        
        print(f"翻译: {mdx_file.name} → {output_file.name}")
        
        try:
            with open(mdx_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            translated = translate_content(content, mdx_file.name)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translated)
            
            print(f"  ✓ 翻译完成\n")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ 翻译失败: {e}\n")
    
    print(f"{'='*60}")
    print(f"✅ 翻译完成！成功处理 {success_count}/{len(mdx_files)} 个文件")
    
    # 提示创建 meta.zh-CN.json
    if success_count > 0:
        print(f"\n💡 提示：别忘了创建 meta.zh-CN.json 文件")

if __name__ == "__main__":
    main()


