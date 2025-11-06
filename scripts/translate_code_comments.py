#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译代码注释和修复残留英文
"""

import re
from pathlib import Path

# 代码注释翻译字典
CODE_COMMENT_TRANSLATIONS = {
    # ====== 常见代码注释 ======
    "# OpenAI": "# OpenAI",
    "# OpenAI GPT-4": "# OpenAI GPT-4",
    "# Google Gemini": "# Google Gemini",
    "# Local Ollama": "# 本地 Ollama",
    "# Azure OpenAI": "# Azure OpenAI",
    
    "# Use in agent": "# 在智能体中使用",
    "# Different agents use different models": "# 不同的智能体使用不同的模型",
    "# Call LLM directly": "# 直接调用 LLM",
    "# Enable streaming": "# 启用流式传输",
    "# Access request context": "# 访问请求上下文",
    "# Function instead of dict": "# 使用函数而不是字典",
    "# Use URLs directly": "# 直接使用 URL",
    "# In workflow or agent": "# 在工作流或智能体中",
    "# Set defaults": "# 设置默认值",
    "# Override default": "# 覆盖默认值",
    "# Additional parameter": "# 额外参数",
    "# New parameter": "# 新参数",
    "# Extract and send": "# 提取并发送",
    "# User receives:": "# 用户接收：",
    "# Think message:": "# 思考消息：",
    "# Final answer:": "# 最终答案：",
    "# Input": "# 输入",
    "# Actual request URL": "# 实际请求 URL",
    "# No API key needed": "# 不需要 API 密钥",
    "# Create an instance": "# 创建实例",
    "# Create a request": "# 创建请求",
    "# Execute the request": "# 执行请求",
    "# Access the response": "# 访问响应",
    "# Create a FunctionHub instance": "# 创建 FunctionHub 实例",
    "# Register functions using decorator": "# 使用装饰器注册函数",
    "# Add the hub to oxy_space": "# 将中心添加到 oxy_space",
    "# Reference tools by hub name": "# 通过中心名称引用工具",
    
    # ====== 代码注释中的完整句子 ======
    "Ollama doesn't need API key": "Ollama 不需要 API 密钥",
    "doesn't need": "不需要",
    
    "Add the hub to oxy_space": "将中心添加到 oxy_space",
    "Reference tools by hub name": "通过中心名称引用工具",
    
    # ====== 残留英文短语 ======
    " 在 same system": "在同一系统中",
    " in same system": "在同一系统中",
    " for same ": " 用于相同 ",
    " at same ": " 在相同 ",
    " with same ": " 使用相同 ",
    
    # ====== 其他常见残留 ======
    " (when model supports it)": "（当模型支持时）",
    " (when supported)": "（当支持时）",
    " when model supports": " 当模型支持",
    " when supported": " 当支持",
    
    # ====== 更多代码注释模式 ======
    "# LLM response:": "# LLM 响应：",
    "# Example:": "# 示例：",
    "# Your logic": "# 您的逻辑",
    "# Your agent logic here": "# 您的智能体逻辑在这里",
    "# Tokens are streamed to user": "# 令牌流式传输给用户",
    "# Messages are sent with": "# 消息发送时包含",
    "# Final response contains": "# 最终响应包含",
    
    # Base headers
    "# Base headers": "# 基础请求头",
    "# Enable dynamic headers": "# 启用动态请求头",
    "# Inherit from context": "# 从上下文继承",
    "# Required for dynamic headers": "# 动态请求头所需",
    "# Enable dynamic updates": "# 启用动态更新",
    "# Headers from upstream automatically forwarded": "# 来自上游的请求头自动转发",
    
    # Production / Development
    "# Production streaming API": "# 生产环境流式 API",
    "# Analytics streaming": "# 分析流式传输",
    "# Local development": "# 本地开发",
    
    # Other
    "# Provide dynamic headers in tool call": "# 在工具调用中提供动态请求头",
}

# 文本中的残留英文短语（非代码块）
TEXT_TRANSLATIONS = {
    "在 same system:": "在同一系统中：",
    "在 same system：": "在同一系统中：",
    "from workflows:": "从工作流：",
    "from workflows：": "从工作流：",
    "在ir ": "在其 ",
}

def translate_content(content):
    """翻译内容"""
    # 先处理文本部分（非代码块）
    parts = re.split(r'(```[\s\S]*?```)', content)
    
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 0:  # 非代码块
            # 应用文本翻译
            for en, zh in TEXT_TRANSLATIONS.items():
                part = part.replace(en, zh)
        else:  # 代码块
            # 应用代码注释翻译
            for en, zh in CODE_COMMENT_TRANSLATIONS.items():
                part = part.replace(en, zh)
        
        result.append(part)
    
    return ''.join(result)

def process_file(file_path):
    """处理单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()
        
        print(f"翻译注释: {file_path.name}")
        
        # 应用翻译
        translated = translate_content(original)
        
        # 检查是否有变化
        if translated != original:
            changes = sum(1 for a, b in zip(original, translated) if a != b)
            changes += abs(len(original) - len(translated))
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(translated)
            
            print(f"  ✓ 已翻译 ({changes} 处修改)\n")
            return True
        else:
            print(f"  - 无需翻译\n")
            return False
        
    except Exception as e:
        print(f"  ✗ 错误: {e}\n")
        return False

def main():
    """主函数"""
    docs_dir = Path("content/docs")
    
    # 获取所有中文翻译文件
    zh_files = list(docs_dir.glob("*.zh-CN.mdx"))
    
    print(f"找到 {len(zh_files)} 个中文翻译文件")
    print("开始翻译代码注释和修复残留英文...\n")
    
    translated_count = 0
    
    for zh_file in sorted(zh_files):
        if process_file(zh_file):
            translated_count += 1
    
    print(f"{'='*60}")
    print(f"✅ 完成！处理了 {translated_count}/{len(zh_files)} 个文件")
    print(f"\n改进：")
    print(f"  ✓ 翻译了代码注释")
    print(f"  ✓ 修复了残留英文短语")
    print(f"  ✓ 保持了代码逻辑完整")

if __name__ == "__main__":
    main()

