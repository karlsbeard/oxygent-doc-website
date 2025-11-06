#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度翻译 OxyAPI 文档
补充翻译所有剩余的英文内容
"""

import re
from pathlib import Path

# 完整的句子和短语翻译映射
FULL_TRANSLATIONS = {
    # 列表项前缀
    "Learn": "学习",
    "Explore": "探索",
    "Check out": "查看",
    
    # API 约定
    "Async Operations": "异步操作",
    "Most API methods are asynchronous and require the": "大多数 API 方法都是异步的，需要使用",
    "keyword": "关键字",
    "Type Safety": "类型安全",
    "All APIs provide complete type annotations": "所有 API 都提供完整的类型注释",
    "Error Handling": "错误处理",
    "API methods throw specific exception types for easier error handling": "API 方法会抛出特定的异常类型以便于错误处理",
    "Flexible Configuration": "灵活配置",
    "Support multiple configuration methods, including parameter passing and configuration files": "支持多种配置方法，包括参数传递和配置文件",
    
    # 参数详情常用描述
    "A unique identifier for the agent within the MAS": "在多智能体系统中代理的唯一标识符",
    "This name is used when calling the agent via": "通过以下方式调用代理时使用此名称：",
    "Indicates whether this agent is the entry point for the multi-agent system": "指示此代理是否为多智能体系统的入口点",
    "Only one agent should be marked as master in a MAS": "在多智能体系统中只有一个代理应标记为主代理",
    "Name reference to an LLM component registered in the same MAS": "在同一多智能体系统中注册的大语言模型组件的名称引用",
    "This LLM will be used for all reasoning steps in the ReAct loop": "此大语言模型将用于 ReAct 循环中的所有推理步骤",
    "List of tool names that the agent can invoke": "代理可以调用的工具名称列表",
    "Tools must be registered in the same MAS instance": "工具必须在同一多智能体系统实例中注册",
    "List of sub-agent names that this agent can delegate tasks to": "此代理可以将任务委托给的子代理名称列表",
    "Sub-agents must be registered in the same MAS instance": "子代理必须在同一多智能体系统实例中注册",
    "Maximum number of reasoning-acting iterations before the agent uses fallback mechanisms": "在代理使用后备机制之前的最大推理-行动迭代次数",
    "Each round consists of one reasoning step and one or more tool executions": "每一轮包括一个推理步骤和一个或多个工具执行",
    
    # 内存相关
    "Controls memory retention strategy": "控制内存保留策略",
    "Keep only final question-answer pairs (cleaner history)": "仅保留最终问答对（更清晰的历史）",
    "Retain full ReAct reasoning traces with weighted scoring": "保留完整的 ReAct 推理轨迹并使用加权评分",
    "Number of recent conversation turns to keep in short-term memory": "保留在短期内存中的最近对话轮次数量",
    "Maximum token limit for the memory system": "内存系统的最大令牌限制",
    "When exceeded, older memories are pruned based on weighted scoring": "超出时，较旧的内存将根据加权评分被修剪",
    "Relative importance weight for short-term memory when": "短期内存的相对重要性权重，当",
    "Higher values give more importance to recent conversations": "较高的值会更重视最近的对话",
    "Relative importance weight for ReAct intermediate steps when": "ReAct 中间步骤的相对重要性权重，当",
    
    # 方法相关
    "Execute the agent with given input": "使用给定输入执行代理",
    "List of message dictionaries with": "消息字典列表，包含",
    "fields": "字段",
    "Additional LLM parameters can be passed through": "可以传递额外的大语言模型参数",
    "object containing": "对象，包含",
    "Final agent response": "最终代理响应",
    "Full conversation history": "完整对话历史",
    "Execution metadata (rounds used, tool calls, etc.)": "执行元数据（使用的轮次、工具调用等）",
    "Your query here": "您的查询内容",
    
    # Related Documentation
    "Usage guide and examples": "使用指南和示例",
    "API reference for": "API 参考文档：",
    "Available tools documentation": "可用工具文档",
    "Overview": "概述",
}

def translate_content(content):
    """翻译内容"""
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
        
        # 翻译行
        translated_line = line
        
        # 应用所有翻译规则
        for en, zh in FULL_TRANSLATIONS.items():
            if en in translated_line:
                translated_line = translated_line.replace(en, zh)
        
        result.append(translated_line)
    
    return '\n'.join(result)

def main():
    """主函数"""
    oxyapi_dir = Path("/Users/chengkai48/Documents/AI/oxygent-doc-website/content/oxyapi")
    
    # 获取所有 .zh-CN.mdx 文件
    zh_files = list(oxyapi_dir.glob("*.zh-CN.mdx"))
    
    print(f"找到 {len(zh_files)} 个中文文件需要深度翻译\n")
    
    success_count = 0
    
    for zh_file in zh_files:
        print(f"深度翻译: {zh_file.name}")
        
        try:
            with open(zh_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            translated_content = translate_content(content)
            
            with open(zh_file, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"  ✓ 完成\n")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ 失败: {e}\n")
    
    print(f"{'='*60}")
    print(f"✅ 深度翻译完成！成功处理 {success_count}/{len(zh_files)} 个文件")

if __name__ == "__main__":
    main()


