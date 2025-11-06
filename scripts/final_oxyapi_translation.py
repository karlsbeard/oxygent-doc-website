#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终 OxyAPI 文档翻译脚本
包含最完整的翻译规则
"""

import re
from pathlib import Path

# 超级全面的翻译映射表
TRANSLATIONS = {
    # 类和结构
    "Class Overview": "类概述",
    "class": "类",
    "Constructor": "构造函数",
    "Parameters": "参数",
    "Inherited Parameters": "继承参数",
    "from": "从",
    "Methods": "方法",
    "Execution Flow": "执行流程",
    "Usage Example": "使用示例",
    "Usage Examples": "使用示例",
    "Usage Guidelines": "使用指南",
    "Best Practices": "最佳实践",
    "Common Patterns": "常见模式",
    "Error Handling": "错误处理",
    "Troubleshooting": "故障排除",
    
    # 描述性前缀
    "the ChatAgent class including": "ChatAgent 类，包括",
    "the ReActAgent class including": "ReActAgent 类，包括",
    "the WorkflowAgent class including": "WorkflowAgent 类，包括",
    "the ParallelAgent class including": "ParallelAgent 类，包括",
    "the RAGAgent class including": "RAGAgent 类，包括",
    "the SSEAgent class including": "SSEAgent 类，包括",
    "including constructor parameters, methods,": "包括构造函数参数、方法",
    "usage examples": "和使用示例",
    
    # 继承相关
    "inherits from": "继承自",
    "provides": "提供",
    "provides basic conversational functionality": "提供基本的对话功能",
    "including conversation history management": "包括对话历史管理",
    "user query processing": "用户查询处理",
    "language model coordination": "和大语言模型协调",
    
    # 参数描述
    "Agent name for identification and calling": "用于识别和调用的代理名称",
    "Agent description explaining its functionality": "解释代理功能的描述",
    "Language model identifier to use": "要使用的大语言模型标识符",
    "System prompt defining agent behavior": "定义代理行为的系统提示",
    "Additional user-defined prompt": "额外的用户自定义提示",
    "List of other agent names this agent can delegate to": "此代理可以委托的其他代理名称列表",
    "List of tools available to this agent": "此代理可用的工具列表",
    "List of tools explicitly forbidden for this agent": "此代理明确禁止使用的工具列表",
    "Whether to enable dynamic tool retrieval": "是否启用动态工具检索",
    "Number of tools to retrieve": "要检索的工具数量",
    "Number of short-term memory entries to retain": "要保留的短期内存条目数",
    "Whether to retrieve user history": "是否检索用户历史",
    "Whether to support multimodal input": "是否支持多模态输入",
    "Number of instances for team execution": "团队执行的实例数",
    "Tool/agent category": "工具/代理类别",
    "Input parameter schema": "输入参数模式",
    "Whether this is a master agent": "此代理是否为主代理",
    "Execution timeout in seconds": "执行超时时间（秒）",
    "Input processing function": "输入处理函数",
    "Output processing function": "输出处理函数",
    "Input formatting function": "输入格式化函数",
    "Output formatting function": "输出格式化函数",
    "List of permitted tool names": "允许的工具名称列表",
    
    # 方法相关
    "Execute a chat interaction with the language model": "与大语言模型执行聊天交互",
    "Request object containing": "请求对象，包含",
    "user query": "用户查询",
    "conversation history": "对话历史",
    "additional parameters": "和额外参数",
    "Response from the language model containing the generated answer": "来自大语言模型的响应，包含生成的答案",
    "Create temporary memory": "创建临时内存",
    "Creates a new Memory object to manage the conversation": "创建一个新的 Memory 对象来管理对话",
    "Add system message": "添加系统消息",
    "Adds system prompt using built instruction": "使用构建的指令添加系统提示",
    "Process input messages": "处理输入消息",
    "Processes user messages and appends them to memory": "处理用户消息并将其附加到内存",
    "Call LLM": "调用大语言模型",
    "Calls the configured language model with the current context": "使用当前上下文调用配置的大语言模型",
    "Generate response": "生成响应",
    "Returns the model's generated response": "返回模型生成的响应",
    
    # 通用描述
    "Config default": "配置默认值",
    "Required": "必需",
    "Optional": "可选",
    "Default": "默认",
    "returns": "返回",
    "containing": "包含",
    "with": "使用",
    "object": "对象",
    
    # 技术术语保持但添加说明
    "A conversational agent that manages chat interactions with language models.": "一个管理与大语言模型聊天交互的对话代理。",
}

def translate_line_by_line(content):
    """逐行翻译内容"""
    lines = content.split('\n')
    result = []
    in_code_block = False
    
    for line in lines:
        # 检测代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue
        
        # 代码块内不翻译
        if in_code_block:
            result.append(line)
            continue
        
        # 跳过纯代码行
        if any(keyword in line for keyword in ['import ', 'from ', 'class ', 'def ', 'async ', 'await ']):
            result.append(line)
            continue
        
        # 翻译行
        translated_line = line
        
        # 按长度从长到短排序，优先匹配长短语
        sorted_items = sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
        
        for en, zh in sorted_items:
            if en in translated_line:
                translated_line = translated_line.replace(en, zh)
        
        result.append(translated_line)
    
    return '\n'.join(result)

def main():
    """主函数"""
    oxyapi_dir = Path("/Users/chengkai48/Documents/AI/oxygent-doc-website/content/oxyapi")
    
    # 获取所有 .zh-CN.mdx 文件
    zh_files = list(oxyapi_dir.glob("*.zh-CN.mdx"))
    
    print(f"找到 {len(zh_files)} 个中文文件需要最终翻译\n")
    
    success_count = 0
    
    for zh_file in zh_files:
        print(f"最终翻译: {zh_file.name}")
        
        try:
            with open(zh_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            translated_content = translate_line_by_line(content)
            
            with open(zh_file, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"  ✓ 完成\n")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ 失败: {e}\n")
    
    print(f"{'='*60}")
    print(f"✅ 最终翻译完成！成功处理 {success_count}/{len(zh_files)} 个文件")

if __name__ == "__main__":
    main()


