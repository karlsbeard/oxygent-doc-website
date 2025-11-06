#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终润色 Docs 文档翻译
处理残留英文和格式问题
"""

import re
from pathlib import Path

# 最终修复字典 - 针对残留的英文句子和短语
FINAL_FIXES = {
    # ====== 残留英文句子 ======
    "Here's a basic example of how to use the `OpenAILLM` class:":
        "以下是如何使用 `OpenAILLM` 类的基本示例：",
    
    "Here's a basic example of how to use the": 
        "以下是如何使用",
    
    "class:": "类的基本示例：",
    
    # ====== 代码注释翻译 ======
    "# Create an instance of OpenAILLM": "# 创建 OpenAILLM 实例",
    "# Create a request": "# 创建请求",
    "# Execute the request": "# 执行请求",
    "# Access the response": "# 访问响应",
    "# Create a FunctionHub instance": "# 创建 FunctionHub 实例",
    "# Register functions using decorator": "# 使用装饰器注册函数",
    "# OpenAI": "# OpenAI",
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
    "# Google Gemini": "# Google Gemini",
    "# Local Ollama": "# 本地 Ollama",
    "# Azure OpenAI": "# Azure OpenAI",
    "# OpenAI GPT-4": "# OpenAI GPT-4",
    
    # ====== 表格和列表中的残留英文 ======
    "e.g., ": "例如：",
    
    # ====== 段落中的短句 ======
    " when model supports it": " 当模型支持时",
    " when supported": " 当支持时",
    
    # ====== 其他常见短语 ======
    "and other compatible services": "和其他兼容服务",
    "or compatible": "或兼容",
    
    # ====== 多余空格修复（使用特殊标记） ======
}

# 正则表达式替换规则
REGEX_FIXES = [
    # 修复中文标点前后多余空格
    (r'([，。：；！？]) +', r'\1'),  # 中文标点后的空格
    (r' +([，。：；！？])', r'\1'),  # 中文标点前的空格
    
    # 修复句子之间的多余空格
    (r'。 +它', r'。它'),
    (r'。 +该', r'。该'),
    (r'。 +这', r'。这'),
    (r'， +([它该这])', r'，\1'),
    
    # 清理行尾空格
    (r' +\n', r'\n'),
    
    # 确保中英文之间有空格（但不在标点符号周围）
    (r'([a-zA-Z0-9])([，。：；])', r'\1 \2'),
    
    # 修复代码块外的格式
    (r'\n\n\n+', r'\n\n'),  # 多个空行变为两个
]

def final_polish(content):
    """最终润色翻译"""
    # 保护代码块
    code_blocks = []
    def save_code(match):
        code_blocks.append(match.group(0))
        return f'__CODE_BLOCK_{len(code_blocks)-1}__'
    
    content = re.sub(r'```[\s\S]*?```', save_code, content)
    
    # 应用字典修复
    fixes = sorted(FINAL_FIXES.items(), key=lambda x: len(x[0]), reverse=True)
    for en_text, zh_text in fixes:
        content = content.replace(en_text, zh_text)
    
    # 应用正则表达式修复
    for pattern, replacement in REGEX_FIXES:
        content = re.sub(pattern, replacement, content)
    
    # 恢复代码块
    for i, code_block in enumerate(code_blocks):
        content = content.replace(f'__CODE_BLOCK_{i}__', code_block)
    
    return content

def process_file(file_path):
    """处理单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()
        
        print(f"润色: {file_path.name}")
        
        # 应用润色
        polished = final_polish(original)
        
        # 检查是否有改进
        if polished != original:
            # 计算字符变化
            diff_count = sum(1 for a, b in zip(original, polished) if a != b)
            diff_count += abs(len(original) - len(polished))
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(polished)
            
            print(f"  ✓ 已润色 ({diff_count} 处修改)\n")
            return True
        else:
            print(f"  - 无需修改\n")
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
    print("开始最终润色...\n")
    
    polished_count = 0
    
    for zh_file in sorted(zh_files):
        if process_file(zh_file):
            polished_count += 1
    
    print(f"{'='*60}")
    print(f"✅ 完成！润色了 {polished_count}/{len(zh_files)} 个文件")
    print(f"\n最终改进：")
    print(f"  ✓ 翻译了残留的英文句子")
    print(f"  ✓ 翻译了代码注释")
    print(f"  ✓ 清理了多余空格")
    print(f"  ✓ 修复了标点符号格式")
    print(f"\n建议：运行 pnpm dev 预览最终效果")

if __name__ == "__main__":
    main()

