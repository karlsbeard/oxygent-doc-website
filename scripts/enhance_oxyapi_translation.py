#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版 OxyAPI 文档翻译脚本
使用更完整的翻译规则和智能替换
"""

import re
from pathlib import Path

# 完整的翻译映射表
TRANSLATIONS = {
    # 标题和说明
    "Learn": "学习",
    "Explore": "探索",
    "Check out": "查看",
    "to understand": "以了解",
    "basic agent usage": "基本的代理使用方法",
    "how to configure large language models": "如何配置大语言模型",
    "the tool system": "工具系统",
    
    # API 约定相关
    "Async Operations": "异步操作",
    "Most API methods are asynchronous": "大多数 API 方法都是异步的",
    "require the": "需要使用",
    "keyword": "关键字",
    "Type Safety": "类型安全",
    "All APIs provide complete type annotations": "所有 API 都提供完整的类型注释",
    "Error Handling": "错误处理",
    "API methods throw specific exception types for easier error handling": "API 方法会抛出特定的异常类型以便于错误处理",
    "Flexible Configuration": "灵活配置",
    "Support multiple configuration methods": "支持多种配置方法",
    "including parameter passing": "包括参数传递",
    "configuration files": "配置文件",
    
    # 参数详情常用短语
    "Type": "类型",
    "Required": "必需",
    "Default": "默认",
    "Description": "描述",
    "Yes": "是",
    "No": "否",
    "False": "False",
    "True": "True",
    
    # 完整句子
    "A unique identifier for the agent": "代理的唯一标识符",
    "within the": "在",
    "Multi-Agent System": "多智能体系统",
    "This name is used when calling the agent via": "调用代理时使用此名称，通过",
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
    
    # 使用指南
    "Usage Guidelines": "使用指南",
    "Simple tasks": "简单任务",
    "Multi-step tasks": "多步骤任务",
    "Complex reasoning chains": "复杂推理链",
    "rounds": "轮",
    
    # 内存相关
    "Controls memory retention strategy": "控制内存保留策略",
    "Keep only final question-answer pairs": "仅保留最终问答对",
    "cleaner history": "更清晰的历史",
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
    "Returns": "返回",
    "object containing": "对象，包含",
    "Final agent response": "最终代理响应",
    "Full conversation history": "完整对话历史",
    "Execution metadata": "执行元数据",
    "rounds used": "使用的轮次",
    "tool calls": "工具调用",
    "etc": "等",
    "Example": "示例",
    "Your query here": "您的查询内容",
    
    # Related Documentation
    "Usage guide and examples": "使用指南和示例",
    "API reference for": "API 参考文档：",
    "Available tools documentation": "可用工具文档",
    
    # 常用连接词 (只在特定上下文中翻译，不要单独翻译避免误伤)
    " and ": " 和 ",
    " or ": " 或 ",
}

def fix_chinese_spacing(text):
    """修复中英文混排时的空格问题"""
    # 移除中文和英文/数字之间多余的空格
    text = re.sub(r'([\u4e00-\u9fa5])\s+([a-zA-Z0-9])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z0-9])\s+([\u4e00-\u9fa5])', r'\1 \2', text)
    return text

def translate_line(line):
    """智能翻译单行文本"""
    if not line.strip():
        return line
    
    # 跳过代码块标记
    if line.strip().startswith('```'):
        return line
    
    # 跳过纯代码行（包含特定编程符号）
    if any(x in line for x in ['import ', 'from ', 'async ', 'await ', 'def ', 'class ', '```']):
        return line
    
    # 跳过已经完全是中文的行
    if re.search(r'^[\u4e00-\u9fa5\s\-\*\#\|`]+$', line.strip()):
        return line
    
    # 翻译文本
    translated = line
    
    # 按长度从长到短排序，优先匹配长短语
    sorted_items = sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for en, zh in sorted_items:
        if en in translated:
            translated = translated.replace(en, zh)
    
    return translated

def translate_file_content(file_path):
    """翻译文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
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
        
        # 翻译普通行
        translated_line = translate_line(line)
        translated_line = fix_chinese_spacing(translated_line)
        result.append(translated_line)
    
    return ''.join(result)

def main():
    """主函数"""
    oxyapi_dir = Path("/Users/chengkai48/Documents/AI/oxygent-doc-website/content/oxyapi")
    
    # 获取所有 .zh-CN.mdx 文件
    zh_files = list(oxyapi_dir.glob("*.zh-CN.mdx"))
    
    print(f"找到 {len(zh_files)} 个中文文件需要增强翻译\n")
    
    success_count = 0
    
    for zh_file in zh_files:
        print(f"增强翻译: {zh_file.name}")
        
        try:
            translated_content = translate_file_content(zh_file)
            
            with open(zh_file, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"  ✓ 完成\n")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ 失败: {e}\n")
    
    print(f"{'='*60}")
    print(f"✅ 增强翻译完成！成功处理 {success_count}/{len(zh_files)} 个文件")

if __name__ == "__main__":
    main()

