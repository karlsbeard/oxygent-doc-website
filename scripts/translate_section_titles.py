#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译段落标题和子标题中的英文
"""

import re
from pathlib import Path

# 段落标题翻译字典
SECTION_TITLE_TRANSLATIONS = {
    # ====== 三级标题 ======
    "### Supported Providers": "### 支持的提供商",
    "### Basic 配置": "### 基础配置",
    "### Basic Configuration": "### 基础配置",
    "### Multiple LLM Providers": "### 多个 LLM 提供商",
    "### Direct LLM Calls": "### 直接 LLM 调用",
    "### Core 参数s": "### 核心参数",
    "### Core Parameters": "### 核心参数",
    "### LLM 参数s": "### LLM 参数",
    "### LLM Parameters": "### LLM 参数",
    "### Multimodal Support": "### 多模态支持",
    "### Headers 配置": "### 请求头配置",
    "### Headers Configuration": "### 请求头配置",
    "### Messaging & Error Handling": "### 消息和错误处理",
    "### Provider-Specific 配置": "### 提供商特定配置",
    "### Provider-Specific Configuration": "### 提供商特定配置",
    
    "### OpenAI": "### OpenAI",
    "### Google Gemini": "### Google Gemini",
    "### Ollama": "### Ollama",
    "### Azure OpenAI": "### Azure OpenAI",
    
    "### Streaming Support": "### 流式传输支持",
    "### Dynamic Headers": "### 动态请求头",
    "### Multimodal Input": "### 多模态输入",
    "### Custom LLM 参数s": "### 自定义 LLM 参数",
    "### Custom LLM Parameters": "### 自定义 LLM 参数",
    "### Think Message Extraction": "### 思考消息提取",
    
    "### Error Handling": "### 错误处理",
    "### Error 类型s Handled": "### 处理的错误类型",
    "### User Experience": "### 用户体验",
    
    "### Basic Function Registration": "### 基本函数注册",
    "### Async Functions": "### 异步函数",
    "### Multiple Related 工具s": "### 多个相关工具",
    "### Multiple Related Tools": "### 多个相关工具",
    
    "### Inherited 参数s": "### 继承的参数",
    "### Inherited Parameters": "### 继承的参数",
    
    "### @tool()": "### @tool()",
    
    "### Basic 类型s": "### 基本类型",
    "### Basic Types": "### 基本类型",
    "### Pydantic Fields": "### Pydantic 字段",
    "### 可选 参数s": "### 可选参数",
    "### Optional Parameters": "### 可选参数",
    "### Complex 类型s": "### 复杂类型",
    "### Complex Types": "### 复杂类型",
    "### Oxy请求 Access": "### OxyRequest 访问",
    "### OxyRequest Access": "### OxyRequest 访问",
    
    "### File Operations": "### 文件操作",
    "### API Integration": "### API 集成",
    "### Database Operations": "### 数据库操作",
    "### Business Logic": "### 业务逻辑",
    
    "### Logging and Debugging": "### 日志记录和调试",
    "### 上下文-Aware 工具s": "### 上下文感知工具",
    "### Context-Aware Tools": "### 上下文感知工具",
    
    "### Static Headers": "### 静态请求头",
    "### Inherited Headers": "### 继承的请求头",
    
    "### Persistent Connection (Keep-Alive)": "### 持久连接（Keep-Alive）",
    "### With Authentication": "### 使用身份验证",
    "### With Dynamic Headers": "### 使用动态请求头",
    "### Multiple Streaming Servers": "### 多个流式服务器",
    
    "### Web 服务配置": "### Web 服务配置",
    "### Web 界面组件": "### Web 界面组件",
    
    # ====== 二级标题 ======
    "## 快速开始": "## 快速开始",
    "## Quick Start": "## 快速开始",
    "## 配置选项": "## 配置选项",
    "## Configuration Options": "## 配置选项",
    "## 高级功能": "## 高级功能",
    "## Advanced Features": "## 高级功能",
    "## API 参考": "## API 参考",
    "## API Reference": "## API 参考",
    "## 示例": "## 示例",
    "## Examples": "## 示例",
    "## Related Documentation": "## 相关文档",
    
    "## URL Auto-Detection": "## URL 自动检测",
    "## Decorator API": "## 装饰器 API",
    "## Function Signature Patterns": "## 函数签名模式",
    "## Usage Patterns": "## 使用模式",
    "## 工具 生命周期": "## 工具生命周期",
    "## Tool Lifecycle": "## 工具生命周期",
    
    "## Class Hierarchy": "## 类层次结构",
    "## Features": "## 特性",
    "## 方法 Details": "## 方法详情",
    "## Method Details": "## 方法详情",
    "## 参数 Details": "## 参数详情",
    "## Parameter Details": "## 参数详情",
    "## 使用示例": "## 使用示例",
    "## Usage Example": "## 使用示例",
    "## 注意s": "## 注意事项",
    "## Notes": "## 注意事项",
    "## 使用场景": "## 使用场景",
    "## Use Cases": "## 使用场景",
    "## Streaming Features": "## 流式传输特性",
    "## 配置 Precedence": "## 配置优先级",
    "## Configuration Precedence": "## 配置优先级",
    
    "## Header Management": "## 请求头管理",
    "## Connection Modes": "## 连接模式",
    "## Web 界面功能": "## Web 界面功能",
}

def translate_titles(content):
    """翻译标题"""
    # 应用翻译（从长到短）
    translations = sorted(SECTION_TITLE_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for en, zh in translations:
        content = content.replace(en, zh)
    
    return content

def process_file(file_path):
    """处理单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()
        
        print(f"翻译标题: {file_path.name}")
        
        # 应用翻译
        translated = translate_titles(original)
        
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
    print("开始翻译段落标题...\n")
    
    translated_count = 0
    
    for zh_file in sorted(zh_files):
        if process_file(zh_file):
            translated_count += 1
    
    print(f"{'='*60}")
    print(f"✅ 完成！处理了 {translated_count}/{len(zh_files)} 个文件")
    print(f"\n改进：")
    print(f"  ✓ 翻译了所有段落标题")
    print(f"  ✓ 统一了标题格式")
    print(f"  ✓ 保持了文档结构")

if __name__ == "__main__":
    main()

