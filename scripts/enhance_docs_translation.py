#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强 Docs 文档翻译
修复中英文混合问题，提供更完整的句子级翻译
"""

import re
from pathlib import Path

# 完整句子和段落的翻译映射（基于实际文件内容）
FULL_TRANSLATIONS = {
    # ====== 常见句式模板 ======
    " is a ": " 是一个 ",
    " is the ": " 是 ",
    " are the ": " 是 ",
    " provides ": " 提供 ",
    " enables ": " 使 ",
    " allows ": " 允许 ",
    " supports ": " 支持 ",
    " includes ": " 包括 ",
    " designed to ": " 旨在 ",
    " used for ": " 用于 ",
    " can be ": " 可以 ",
    " will be ": " 将 ",
    " should be ": " 应该 ",
    " must be ": " 必须 ",
    # ====== HttpLLM 特定翻译 ======
    "primary LLM integration in OxyGent that connects to remote language model APIs over HTTP": "OxyGent 中主要的 LLM 集成，通过 HTTP 连接到远程语言模型 API",
    "a unified interface for OpenAI-compatible APIs": "为 OpenAI 兼容的 API 提供统一接口",
    "handles authentication, request formatting, response parsing, and streaming support automatically": "自动处理身份验证、请求格式化、响应解析和流式传输支持",
    "Works with OpenAI, Gemini, Ollama, and any OpenAI-compatible API": "适用于 OpenAI、Gemini、Ollama 和任何 OpenAI 兼容的 API",
    "Real-time token streaming for responsive user experiences": "实时令牌流式传输以获得响应式用户体验",
    "Support for images, videos, and documents": "支持图像、视频和文档",
    "Automatically formats requests based on endpoint URL": "根据端点 URL 自动格式化请求",
    "Static, dynamic, and function-based header configuration": "静态、动态和基于函数的请求头配置",
    "User-friendly error messages with automatic retry logic": "用户友好的错误消息和自动重试逻辑",
    "Connect to OpenAI-compatible APIs": "连接到 OpenAI 兼容的 API",
    "Configure multiple LLM providers": "配置多个 LLM 提供商",
    "in same system": "在同一系统中",
    "Call LLMs directly from workflows": "从工作流中直接调用 LLM",
    "Enable real-time token streaming": "启用实时令牌流式传输",
    "Configure headers that change per request": "配置每个请求变化的请求头",
    "Process images and videos": "处理图像和视频",
    "for vision-enabled models": "用于支持视觉的模型",
    "Override default parameters per call": "每次调用时覆盖默认参数",
    "Enable reasoning transparency": "启用推理透明度",
    "automatically detects and formats endpoints": "自动检测和格式化端点",
    "comprehensive error handling": "全面的错误处理",
    # ====== OpenAILLM 特定翻译 ======
    "concrete implementation of the": "具体实现的",
    "class specifically designed for": "类，专门设计用于",
    "Uses the official AsyncOpenAI client for optimal performance": "使用官方 AsyncOpenAI 客户端以获得最佳性能",
    "seamless integration with": "与...无缝集成",
    "supporting all OpenAI models and compatible APIs": "支持所有 OpenAI 模型和兼容的 API",
    "Official Client Integration": "官方客户端集成",
    "Optimized for performance with": "针对...优化性能",
    "Full compatibility with": "与...完全兼容",
    "Dynamic payload construction": "动态负载构建",
    "merging from multiple sources": "从多个源合并",
    "passing from request arguments": "从请求参数传递",
    "Real-time content delivery": "实时内容传递",
    "Incremental message forwarding": "增量消息转发",
    "Thinking process extraction during streaming": "流式传输期间的思考过程提取",
    "Unified response format": "统一的响应格式",
    "Proper handling of completion responses": "正确处理完成响应",
    "Support for reasoning content extraction": "支持推理内容提取",
    "Executes a request using the OpenAI API": "使用 OpenAI API 执行请求",
    "handling payload construction": "处理负载构建",
    "configuration merging": "配置合并",
    "and response processing": "和响应处理",
    "The API key for authentication with OpenAI": "用于 OpenAI 身份验证的 API 密钥",
    "The base URL endpoint for the OpenAI API": "OpenAI API 的基础 URL 端点",
    "can be used for compatible APIs": "可用于兼容的 API",
    "The specific OpenAI model name to use for requests": "用于请求的特定 OpenAI 模型名称",
    "Extra HTTP headers or a function that returns headers": "额外的 HTTP 请求头或返回请求头的函数",
    "is merged from multiple sources": "从多个源合并",
    "in following order of precedence": "按以下优先级顺序",
    "highest priority": "最高优先级",
    "Instance-specific LLM parameters": "实例特定的 LLM 参数",
    "Global LLM configuration": "全局 LLM 配置",
    "both streaming and non-streaming responses": "流式和非流式响应",
    "When streaming is enabled": "当启用流式传输时",
    "content is incrementally forwarded": "内容被增量转发",
    "to client": "到客户端",
    "The class has special handling for": "该类对...有特殊处理",
    "thinking process extraction during streaming": "流式传输期间的思考过程提取",
    "Detects": "检测",
    "in response": "在响应中",
    "Automatically wraps reasoning content with": "自动使用...包装推理内容",
    "Forwards thinking content": "转发思考内容",
    "to frontend in real-time": "实时到前端",
    "For streaming responses": "对于流式响应",
    "the class accumulates the complete response": "该类累积完整响应",
    "while forwarding incremental updates": "同时转发增量更新",
    "is designed to work with all OpenAI models": "旨在与所有 OpenAI 模型配合使用",
    "Compatible APIs include services that implement": "兼容的 API 包括实现...的服务",
    "Proper error handling is built-in for": "对...内置了适当的错误处理",
    "API failures and timeouts": "API 失败和超时",
    "Response formats are standardized across": "响应格式在...中标准化",
    "streaming and non-streaming modes": "流式和非流式模式",
    # ====== FunctionHub 特定翻译 ======
    "decorator-based tool registry that converts regular Python functions into executable tools": "基于装饰器的工具注册表，将常规 Python 函数转换为可执行工具",
    "within OxyGent system": "在 OxyGent 系统中",
    "a simple, Pythonic interface for creating custom tools": "用于创建自定义工具的简单 Pythonic 接口",
    "without needing to understand the underlying tool architecture": "无需理解底层工具架构",
    "can be synchronous or asynchronous": "可以是同步或异步的",
    "automatically handles the conversion": "自动处理转换",
    "Simple": "简单的",
    "decorator for function registration": "用于函数注册的装饰器",
    "Synchronous functions automatically wrapped as async": "同步函数自动包装为异步",
    "Automatic schema extraction from function signatures and type hints": "从函数签名和类型提示自动提取模式",
    "Full support for Pydantic": "完全支持 Pydantic",
    "descriptions": "描述",
    "Tools are created at runtime during MAS initialization": "工具在 MAS 初始化期间在运行时创建",
    "Register many related tools in a single hub": "在单个中心注册多个相关工具",
    "Use FunctionHub when": "在以下情况下使用 FunctionHub",
    "Use MCP Tools when": "在以下情况下使用 MCP 工具",
    "Writing custom business logic": "编写自定义业务逻辑",
    "Integrating internal APIs": "集成内部 API",
    "Quick prototyping and testing": "快速原型开发和测试",
    "Functions are simple and Python-native": "函数简单且是 Python 原生的",
    "Need tight coupling with your code": "需要与您的代码紧密耦合",
    "Using external services": "使用外部服务",
    "filesystem, search": "文件系统、搜索",
    "Need cross-language support": "需要跨语言支持",
    "Want to reuse existing MCP servers": "想要重用现有的 MCP 服务器",
    "Need standardized protocols": "需要标准化协议",
    "Sharing tools across multiple projects": "在多个项目之间共享工具",
    "Register simple Python functions as tools": "将简单的 Python 函数注册为工具",
    "Create a FunctionHub instance": "创建 FunctionHub 实例",
    "Register functions using decorator": "使用装饰器注册函数",
    "Add the hub to oxy_space": "将中心添加到 oxy_space",
    "Reference tools by hub name": "通过中心名称引用工具",
    "Register asynchronous functions for I/O operations": "为 I/O 操作注册异步函数",
    "Group related functions in a single hub": "将相关函数分组到单个中心",
    "Unique identifier for this FunctionHub": "此 FunctionHub 的唯一标识符",
    "used by agents to reference tools": "由智能体用于引用工具",
    "Collection of custom business logic tools": "自定义业务逻辑工具集合",
    "Description of this tool collection": "此工具集合的描述",
    "FunctionHub inherits from BaseTool and supports these parameters": "FunctionHub 继承自 BaseTool 并支持这些参数",
    "Whether agents need permission to call these tools": "智能体是否需要权限来调用这些工具",
    "Maximum execution time per tool in seconds": "每个工具的最大执行时间（秒）",
    "Maximum concurrent executions": "最大并发执行数",
    "Number of retry attempts on failure": "失败时的重试次数",
    "Delay between retries in seconds": "重试之间的延迟（秒）",
    "Register a function as a tool": "将函数注册为工具",
    "in hub": "在中心中",
    "Human-readable description of what the tool does": "工具功能的可读描述",
    "This is shown to LLMs when they choose tools": "在 LLM 选择工具时显示",
    "Automatically converts sync functions to async": "自动将同步函数转换为异步",
    "Extracts parameter schema from function signature": "从函数签名提取参数模式",
    "Registers function with hub's internal dictionary": "使用中心的内部字典注册函数",
    "Returns the async version of the function": "返回函数的异步版本",
    "Use Python type hints for automatic schema generation": "使用 Python 类型提示进行自动模式生成",
    "Example with basic types": "基本类型示例",
    "for detailed parameter descriptions": "用于详细的参数描述",
    "Example with Pydantic Fields": "Pydantic Fields 示例",
    "Use default values for optional parameters": "为可选参数使用默认值",
    "Example with optional parameters": "可选参数示例",
    "Required": "必需",
    "no default": "无默认值",
    "Optional with default": "带默认值的可选",
    "Support for lists, dicts, and nested types": "支持列表、字典和嵌套类型",
    "Example with complex types": "复杂类型示例",
    "Access the full context by including": "通过包含...访问完整上下文",
    "parameter": "参数",
    "Example with context access": "上下文访问示例",
    "Automatically injected, not in schema": "自动注入，不在模式中",
    "Access request context": "访问请求上下文",
    "Your logic": "您的逻辑",
    "parameter is excluded from tool schema": "参数从工具模式中排除",
    "LLMs don't see it": "LLM 看不到它",
    "Create file manipulation tools": "创建文件操作工具",
    "Wrap external API calls": "包装外部 API 调用",
    "Create database query tools": "创建数据库查询工具",
    "Implement domain-specific operations": "实现特定领域的操作",
    "is a factory that creates FunctionTools during MAS initialization": "是一个在 MAS 初始化期间创建 FunctionTool 的工厂",
    "reference the hub name in their": "在其...中引用中心名称",
    "list": "列表",
    "see and call individual function names": "查看并调用单个函数名称",
    "not the hub name": "而不是中心名称",
    "Schema extraction happens automatically from type hints and": "模式提取自动从类型提示和...发生",
    "Implement robust error handling in tools": "在工具中实现健壮的错误处理",
    "Add logging to tools": "向工具添加日志记录",
    "Tool with logging": "带日志记录的工具",
    "for context-aware operations": "用于上下文感知操作",
    "Access conversation history": "访问对话历史",
    "Access shared data": "访问共享数据",
    "Generate contextual response": "生成上下文响应",
    # ====== 通用短语 ======
    "For complete API documentation": "完整的 API 文档请参考",
    "including all constructor parameters, methods, and detailed parameter descriptions": "包括所有构造函数参数、方法和详细的参数描述",
    "see:": "请参考：",
    "Complete API documentation": "完整的 API 文档",
    "Explore practical implementations": "探索实际实现",
    "Simple function registration and usage": "简单的函数注册和使用",
    "Using tools in reasoning agents": "在推理智能体中使用工具",
    "External tool integration via MCP": "通过 MCP 进行外部工具集成",
    "Accessing request context in tools": "在工具中访问请求上下文",
    "Global tool configuration": "全局工具配置",
    "Basic LLM Usage": "基本 LLM 使用",
    "Direct LLM calls in workflows": "在工作流中直接调用 LLM",
    "Multi-Provider Setup": "多提供商设置",
    "Multiple LLMs in one system": "一个系统中的多个 LLM",
    "Custom Headers": "自定义请求头",
    "Dynamic header configuration": "动态请求头配置",
    "Conversational agent using LLMs": "使用 LLM 的对话智能体",
    "Reasoning agent using LLMs": "使用 LLM 的推理智能体",
    "Direct LLM calls from workflows": "从工作流直接调用 LLM",
    "Global LLM configuration": "全局 LLM 配置",
    "Understanding the call API": "理解调用 API",
    # 表格相关
    "Conditional": "条件性",
    "not needed for Ollama": "Ollama 不需要",
    "Base URL of the API endpoint": "API 端点的基础 URL",
    "Model identifier": "模型标识符",
    "Default parameters passed to LLM": "传递给 LLM 的默认参数",
    "Maximum execution time in seconds": "最大执行时间（秒）",
    "5 minutes": "5 分钟",
    "Enable image/video input support": "启用图像/视频输入支持",
    "Convert media URLs to base64": "将媒体 URL 转换为 base64",
    "for APIs that don't support URLs": "用于不支持 URL 的 API",
    "Maximum image size in pixels": "最大图像大小（像素）",
    "Maximum video size in bytes": "最大视频大小（字节）",
    "Maximum file size for base64": "base64 的最大文件大小",
    "Static headers or function returning headers": "静态请求头或返回请求头的函数",
    "Send thinking process messages to frontend": "向前端发送思考过程消息",
    "User-friendly error message on failures": "失败时的用户友好错误消息",
    # 代码注释常见词
    "No API key needed": "不需要 API 密钥",
    "Use in agent": "在智能体中使用",
    "Different agents use different models": "不同的智能体使用不同的模型",
    "Call LLM directly": "直接调用 LLM",
    "Your agent logic here": "您的智能体逻辑在这里",
    "Enable streaming": "启用流式传输",
    "Tokens are streamed to user as they arrive": "令牌在到达时流式传输给用户",
    "Messages are sent with": "消息发送时包含",
    "Final response contains the complete text": "最终响应包含完整文本",
    "Access request context": "访问请求上下文",
    "Function instead of dict": "函数而不是字典",
    "Use URLs directly": "直接使用 URL",
    "In workflow or agent": "在工作流或智能体中",
    "Set defaults": "设置默认值",
    "Override default": "覆盖默认值",
    "Additional parameter": "额外参数",
    "New parameter": "新参数",
    "Extract and send": "提取并发送",
    "tags": "标签",
    "User receives": "用户接收",
    "Think message": "思考消息",
    "Final answer": "最终答案",
    "Input": "输入",
    "Actual request URL": "实际请求 URL",
    "Error Types Handled": "处理的错误类型",
    "Network timeouts": "网络超时",
    "API errors": "API 错误",
    "rate limits, invalid keys": "速率限制、无效密钥",
    "Malformed responses": "格式错误的响应",
    "Connection failures": "连接失败",
    "User Experience": "用户体验",
    "Technical errors are hidden from users": "技术错误对用户隐藏",
    "Friendly error messages are shown instead": "显示友好的错误消息",
    "Automatic retries reduce transient failures": "自动重试减少瞬时失败",
}


def enhance_translation(content):
    """增强翻译质量"""
    # 保护代码块
    code_blocks = []

    def save_code(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"

    content = re.sub(r"```[\s\S]*?```", save_code, content)

    # 应用所有翻译规则（从长到短，避免部分替换）
    translations = sorted(
        FULL_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True
    )

    for en_text, zh_text in translations:
        if en_text in content:
            content = content.replace(en_text, zh_text)

    # 恢复代码块
    for i, code_block in enumerate(code_blocks):
        content = content.replace(f"__CODE_BLOCK_{i}__", code_block)

    return content


def enhance_file(file_path):
    """增强单个文件的翻译"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        print(f"增强翻译: {file_path.name}")

        # 应用增强翻译
        enhanced_content = enhance_translation(content)

        # 如果有改进，写回文件
        if enhanced_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(enhanced_content)
            print(f"  ✓ 已优化\n")
            return True
        else:
            print(f"  - 无需更改\n")
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
    print("开始增强翻译质量...\n")

    improved_count = 0

    for zh_file in sorted(zh_files):
        if enhance_file(zh_file):
            improved_count += 1

    print(f"{'='*60}")
    print(f"✅ 完成！优化了 {improved_count}/{len(zh_files)} 个文件")
    print(f"\n提示：")
    print(f"  - 已修复大量中英文混合问题")
    print(f"  - 完整句子已翻译为中文")
    print(f"  - 代码块保持不变")
    print(f"  - 建议运行 pnpm dev 预览效果")


if __name__ == "__main__":
    main()
