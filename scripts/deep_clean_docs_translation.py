#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度清理 Docs 文档翻译
彻底修复所有中英文混合问题
"""

import re
from pathlib import Path

# 完整段落和复杂句子的翻译（基于实际文件分析）
DEEP_TRANSLATIONS = {
    # ====== HttpLLM 文件专用 ======
    "**HttpLLM** 是 OxyGent 中主要的 LLM 集成，通过 HTTP 连接到远程语言模型 API. It 提供 为 OpenAI 兼容的 API 提供统一接口, 包括 OpenAI, Gemini, Ollama, and other compatible services. HttpLLM 处理 authentication, request formatting, response parsing, and streaming support automatically.": "**HttpLLM** 是 OxyGent 中主要的 LLM 集成，通过 HTTP 连接到远程语言模型 API。它为 OpenAI 兼容的 API 提供统一接口，包括 OpenAI、Gemini、Ollama 和其他兼容服务。HttpLLM 自动处理身份验证、请求格式化、响应解析和流式传输支持。",
    "when model 支持 it": "当模型支持时",
    "连接到 OpenAI 兼容的 API:": "连接到 OpenAI 兼容的 API：",
    "配置 merging from multiple sources": "从多个源合并配置",
    "参数 passing from request arguments": "从请求参数传递参数",
    "默认值 parameters passed 到 LLM": "传递给 LLM 的默认参数",
    "Tokens are streamed 到 user as they arrive": "令牌在到达时流式传输给用户",
    "content is incrementally forwarded 到 client": "内容被增量转发到客户端",
    "提供 comprehensive error handling": "提供全面的错误处理",
    # ====== OpenAILLM 文件专用 ======
    "`OpenAILLM` 是一个 具体实现的 `RemoteLLM` 类，专门设计用于 OpenAI's language models. It uses the official AsyncOpenAI client for optimal performance and compatibility with OpenAI's API standards. This class 提供 与...无缝集成 OpenAI's chat completion API, 支持所有 OpenAI 模型和兼容的 API.": "`OpenAILLM` 是一个具体实现 `RemoteLLM` 的类，专门为 OpenAI 的语言模型设计。它使用官方 AsyncOpenAI 客户端以获得最佳性能和与 OpenAI API 标准的兼容性。该类提供与 OpenAI 的聊天完成 API 的无缝集成，支持所有 OpenAI 模型和兼容的 API。",
    "The `OpenAILLM` class 提供 the following core functionalities:": "`OpenAILLM` 类提供以下核心功能：",
    "Uses the official AsyncOpenAI client library": "使用官方 AsyncOpenAI 客户端库",
    "Optimized for performance with OpenAI's API": "针对 OpenAI API 优化性能",
    "Full compatibility with OpenAI's API standards": "与 OpenAI API 标准完全兼容",
    "针对...优化性能 OpenAI's API": "针对 OpenAI API 优化性能",
    "与...完全兼容 OpenAI's API standards": "与 OpenAI API 标准完全兼容",
    "配置 从多个源合并": "从多个源合并配置",
    "参数 从请求参数传递": "从请求参数传递参数",
    "使用 OpenAI API 执行请求, 处理负载构建, 配置合并, 和响应处理": "使用 OpenAI API 执行请求，处理负载构建、配置合并和响应处理",
    "OpenAI API 的基础 URL 端点 (可以 用于 compatible APIs)": "OpenAI API 的基础 URL 端点（可用于兼容的 API）",
    "用于 OpenAI 身份验证的 API 密钥": "用于 OpenAI 身份验证的 API 密钥",
    "配置 is merged from multiple sources 在 following order of precedence:": "配置从多个源按以下优先级顺序合并：",
    "- `OpenAILLM` uses the official AsyncOpenAI client for optimal performance and compatibility": "- `OpenAILLM` 使用官方 AsyncOpenAI 客户端以获得最佳性能和兼容性",
    "- The class 支持 both streaming and non-streaming responses": "- 该类支持流式和非流式响应",
    "- When streaming is enabled, content is incrementally forwarded 到 client": "- 当启用流式传输时，内容被增量转发到客户端",
    "- The class has special handling for thinking process extraction during streaming:": "- 该类对流式传输期间的思考过程提取有特殊处理：",
    "  - Detects `reasoning_content` 在 response": "  - 在响应中检测 `reasoning_content`",
    "  - Automatically wraps reasoning content with `<think>` and `</think>` tags": "  - 自动使用 `<think>` 和 `</think>` 标签包装推理内容",
    "  - Forwards thinking content 到 frontend in real-time": "  - 实时将思考内容转发到前端",
    "- For streaming responses, the class accumulates the complete response while forwarding incremental updates": "- 对于流式响应，该类在转发增量更新的同时累积完整响应",
    "- The class is 旨在 work with all OpenAI models and compatible APIs": "- 该类旨在与所有 OpenAI 模型和兼容的 API 配合使用",
    "- Compatible APIs include services that implement OpenAI's API standard (e.g., Azure OpenAI, local models with OpenAI-compatible servers)": "- 兼容的 API 包括实现 OpenAI API 标准的服务（例如 Azure OpenAI、具有 OpenAI 兼容服务器的本地模型）",
    "- Proper error handling is built-in for API failures and timeouts": "- 对 API 失败和超时内置了适当的错误处理",
    "- 响应 formats are standardized across streaming and non-streaming modes": "- 响应格式在流式和非流式模式中标准化",
    # ====== FunctionHub 文件专用 ======
    "**FunctionHub** 是一个 基于装饰器的工具注册表，将常规 Python 函数转换为可执行工具 with在 OxyGent system. It 提供 用于创建自定义工具的简单 Pythonic 接口 无需理解底层工具架构. Functions 可以 synchronous or asynchronous, and FunctionHub automatically 处理 the conversion.": "**FunctionHub** 是一个基于装饰器的工具注册表，将常规 Python 函数转换为 OxyGent 系统中的可执行工具。它提供用于创建自定义工具的简单 Pythonic 接口，无需理解底层工具架构。函数可以是同步或异步的，FunctionHub 会自动处理转换。",
    "with在 OxyGent system": "在 OxyGent 系统中",
    "可以 synchronous or asynchronous": "可以是同步或异步的",
    "automatically 处理 the conversion": "自动处理转换",
    "工具s are created at runtime during MAS initialization": "工具在 MAS 初始化期间在运行时创建",
    "将简单的 Python 函数注册为工具:": "将简单的 Python 函数注册为工具：",
    "使用 hub's internal dictionary": "使用中心的内部字典",
    "返回值 the async version of the function": "返回函数的异步版本",
    "FunctionHub inherits from Base工具 and 支持 these parameters:": "FunctionHub 继承自 BaseTool 并支持这些参数：",
    "in 中心中": "在中心中",
    "FunctionHub 是一个 **factory** that creates Function工具s during MAS initialization": "FunctionHub 是一个**工厂**，在 MAS 初始化期间创建 FunctionTool",
    "智能体s reference the **hub name** 在ir `tools` list": "智能体在其 `tools` 列表中引用**中心名称**",
    "LLMs see and call **individual function names** (not the hub name)": "LLM 查看并调用**单个函数名称**（而不是中心名称）",
    "Schema extraction happens automatically from type hints and Field()": "模式提取自动从类型提示和 Field() 发生",
    "包括 all constructor parameters, methods, and detailed parameter descriptions": "包括所有构造函数参数、方法和详细的参数描述",
    # ====== 通用修复 ======
    " 在ir ": " 在其 ",
    " 在 following ": " 按以下 ",
    "工具s ": "工具 ",
    "Base工具": "BaseTool",
    "Function工具s": "FunctionTool",
    "返回值 the ": "返回 ",
    "使用 hub's ": "使用中心的 ",
    "提供 the ": "提供 ",
    "支持 the ": "支持 ",
    "处理 the ": "处理 ",
    "包括 the ": "包括 ",
    "使用 the ": "使用 ",
    "从 the ": "从 ",
    "到 the ": "到 ",
    "在 the ": "在 ",
    "with the ": "与 ",
    "for the ": "对于 ",
    "of the ": "的 ",
    "is the ": "是 ",
    "are the ": "是 ",
    # 修复语法问题
    "It 提供 ": "它提供",
    "It 使用 ": "它使用",
    ". It ": "。它",
    ". This ": "。这个",
    ". The ": "。该",
    ". For ": "。对于",
    ". When ": "。当",
    # 保持一致性
    "智能体": "智能体",
    "工具": "工具",
    "配置": "配置",
    "参数": "参数",
    "请求": "请求",
    "响应": "响应",
    "方法": "方法",
    "类型": "类型",
    "描述": "描述",
    "示例": "示例",
    "使用": "使用",
    "默认值": "默认值",
    "必需": "必需",
    "可选": "可选",
}

# 段落级翻译规则
PARAGRAPH_RULES = [
    # 修复常见的中英文混合模式
    (r"(\w+) 是一个 (\w+)", r"\1 是一个\2"),
    (r"(\w+) 提供 (\w+)", r"\1 提供\2"),
    (r"(\w+) 支持 (\w+)", r"\1 支持\2"),
    (r"(\w+) 处理 (\w+)", r"\1 处理\2"),
    (r"(\w+) 使用 (\w+)", r"\1 使用\2"),
    # 修复标点符号
    (r"([，。])(\w)", r"\1 \2"),
    (r"([a-zA-Z])(，|。)", r"\1 \2"),
]


def deep_clean_translation(content):
    """深度清理翻译"""
    # 保护代码块
    code_blocks = []

    def save_code(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"

    content = re.sub(r"```[\s\S]*?```", save_code, content)

    # 应用所有翻译规则（从长到短）
    translations = sorted(
        DEEP_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True
    )

    for en_text, zh_text in translations:
        content = content.replace(en_text, zh_text)

    # 应用段落级规则
    for pattern, replacement in PARAGRAPH_RULES:
        content = re.sub(pattern, replacement, content)

    # 恢复代码块
    for i, code_block in enumerate(code_blocks):
        content = content.replace(f"__CODE_BLOCK_{i}__", code_block)

    return content


def process_file(file_path):
    """处理单个文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original = f.read()

        print(f"深度清理: {file_path.name}")

        # 应用深度清理
        cleaned = deep_clean_translation(original)

        # 检查是否有改进
        if cleaned != original:
            # 计算变化
            changes = sum(
                1 for i, (a, b) in enumerate(zip(original, cleaned)) if a != b
            )

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(cleaned)

            print(f"  ✓ 已清理 ({changes} 处修改)\n")
            return True
        else:
            print(f"  - 无需清理\n")
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
    print("开始深度清理翻译...\n")

    cleaned_count = 0

    for zh_file in sorted(zh_files):
        if process_file(zh_file):
            cleaned_count += 1

    print(f"{'='*60}")
    print(f"✅ 完成！深度清理了 {cleaned_count}/{len(zh_files)} 个文件")
    print(f"\n改进：")
    print(f"  - 修复了中英文混合句子")
    print(f"  - 清理了语法问题")
    print(f"  - 统一了术语使用")
    print(f"  - 保持了代码块完整性")


if __name__ == "__main__":
    main()
