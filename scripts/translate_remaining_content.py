#!/usr/bin/env python3
"""
翻译剩余内容 - 包括代码注释、标题等
"""

import re
from pathlib import Path


def translate_code_comments(content: str) -> str:
    """翻译Python代码块中的注释"""

    def process_code_block(match):
        code = match.group(0)

        # 翻译注释
        translations = {
            "# Replace with the actual database": "# 替换为实际的数据库",
            "# Key Method": "# 关键方法",
            "Replace with the actual database": "替换为实际的数据库",
            "Key Method": "关键方法",
        }

        for en, zh in translations.items():
            code = code.replace(en, zh)

        return code

    # 处理Python代码块
    content = re.sub(r"```python[\s\S]*?```", process_code_block, content)

    return content


def translate_headings(content: str) -> str:
    """翻译标题"""
    translations = {
        "Complete Runnable Example": "完整可运行示例",
        "Communication Process": "通信过程",
        "SSE Protocol Explanation": "SSE 协议说明",
        "Relationship between SSEOxyGent and 工作流智能体": "SSEOxyGent 与工作流智能体的关系",
        "Function Comparison": "功能对比",
        "Usage Scenarios": "使用场景",
        "SSEOxy智能体 Principle": "SSEOxy智能体原理",
        "Execution Model": "执行模型",
        "Performance Characteristics": "性能特征",
        "配置 Complexity": "配置复杂度",
        "Use Case Matrix": "用例矩阵",
        "By Task 类型": "按任务类型",
        "By Constraints": "按约束条件",
        "Combination Patterns": "组合模式",
        "Migration Guide": "迁移指南",
        "最佳实践 Summary": "最佳实践摘要",
        "Detailed Feature Comparison": "详细功能对比",
        "Decision Tree": "决策树",
        "高级功能": "高级功能",
        "条件性 Logic": "条件逻辑",
        "Iterative Processing": "迭代处理",
        "错误处理": "错误处理",
        "Parallel Execution": "并行执行",
        "State Management": "状态管理",
        # 更多标题
        "With 智能体 Calls": "使用智能体调用",
        "配置选项": "配置选项",
        "核心参数": "核心参数",
        "Base流程 参数s": "Base流程参数",
        "理解 工作流 Execution": "理解工作流执行",
        "理解 SSE MCP 流程": "理解 SSE MCP 流程",
        "理解 Streamable HTTP 流程": "理解 Streamable HTTP 流程",
        "请求头管理": "请求头管理",
        "静态请求头": "静态请求头",
        "动态请求头": "动态请求头",
        "继承的请求头": "继承的请求头",
        "连接模式": "连接模式",
        "持久连接（Keep-Alive）": "持久连接（Keep-Alive）",
        "Transient Connection (Per-请求)": "瞬态连接（每请求一次）",
        "Middleware Support": "中间件支持",
        "Adding Middlewares": "添加中间件",
        "URL Building": "URL 构建",
        "Connection Health": "连接健康状况",
        "Server Setup Example": "服务器设置示例",
        "Troubleshooting": "故障排除",
        "Common Issues": "常见问题",
        "Performance Considerations": "性能考虑",
        "Connection Mode Impact": "连接模式影响",
        "Concurrency Tuning": "并发调优",
        "概述 Comparison": "概述对比",
        "Detailed Comparison": "详细对比",
        "Transport & Communication": "传输与通信",
        "使用场景": "使用场景",
        "Basic Setup": "基本设置",
        "使用身份验证": "使用身份验证",
        "使用身份验证 Headers": "使用身份验证头",
        "使用动态请求头": "使用动态请求头",
        "Multiple Remote Servers": "多个远程服务器",
        "多个流式服务器": "多个流式服务器",
        "必需 参数s": "必需参数",
        "可选参数": "可选参数",
        "继承的参数": "继承的参数",
        "Bidirectional Streaming": "双向流式传输",
        "Connection Pooling": "连接池",
        "Quick Decision Tree": "快速决策树",
        "Feature Matrix": "功能矩阵",
        "Common Scenarios": "常见场景",
        "Scenario 1: Local Development": "场景 1：本地开发",
        "Scenario 2: Production Web Service": "场景 2：生产 Web 服务",
        "Scenario 3: Multi-Environment Setup": "场景 3：多环境设置",
        "Scenario 4: Dynamic Authentication": "场景 4：动态身份验证",
        "From Stdio to SSE": "从 Stdio 到 SSE",
        "From SSE to Streamable": "从 SSE 到 Streamable",
        "For StdioMCPClient": "对于 StdioMCPClient",
        "For SSEMCPClient": "对于 SSEMCPClient",
        "For StreamableMCPClient": "对于 StreamableMCPClient",
        "StdioMCPClient Issues": "StdioMCPClient 问题",
        "SSEMCPClient Issues": "SSEMCPClient 问题",
        "StreamableMCPClient Issues": "StreamableMCPClient 问题",
    }

    for en, zh in translations.items():
        # 翻译二级标题
        content = content.replace(f"## {en}", f"## {zh}")
        # 翻译三级标题
        content = content.replace(f"### {en}", f"### {zh}")
        # 翻译四级标题
        content = content.replace(f"#### {en}", f"#### {zh}")

    return content


def fix_spacing(content: str) -> str:
    """修复空格问题"""
    # 修复中文和英文之间的空格
    content = re.sub(r"([a-zA-Z])\s+支持", r"\1支持", content)
    content = re.sub(r"([a-zA-Z])\s+提供", r"\1提供", content)
    content = re.sub(r"OxyGent\s+支持", "OxyGent 支持", content)

    # 修复多余的空格
    content = re.sub(r"\s+。", "。", content)
    content = re.sub(r"\s+，", "，", content)

    return content


def translate_inline_text(content: str) -> str:
    """翻译行内文本"""

    # 保护代码块
    code_blocks = {}
    counter = [0]

    def replace_code(match):
        placeholder = f"___CODE_{counter[0]}___"
        code_blocks[placeholder] = match.group(0)
        counter[0] += 1
        return placeholder

    content = re.sub(r"```[\s\S]*?```", replace_code, content)
    content = re.sub(r"`[^`]+`", replace_code, content)

    # 行内翻译
    translations = {
        "RAG 示例": "RAG 示例",
        " 示例": "示例",
        " 中注入": "中注入",
        " 中": "中",
        # 修复特定短语
        "支持通过 knowledge 参数": "支持通过 knowledge 参数",
        "在update_query 中": "在 update_query 中",
    }

    for en, zh in translations.items():
        content = content.replace(en, zh)

    # 恢复代码块
    for placeholder, code in code_blocks.items():
        content = content.replace(placeholder, code)

    return content


def process_file(file_path: Path) -> int:
    """处理单个文件"""
    print(f"处理: {file_path.name}")

    content = file_path.read_text(encoding="utf-8")
    original = content

    # 应用所有翻译
    content = translate_headings(content)
    content = translate_code_comments(content)
    content = fix_spacing(content)
    content = translate_inline_text(content)

    # 计算变化
    changes = sum(1 for a, b in zip(original, content) if a != b)

    if changes > 0:
        file_path.write_text(content, encoding="utf-8")
        print(f"  ✓ {changes} 处修改")
    else:
        print(f"  - 无需修改")

    return changes


def main():
    """主函数"""
    docs_dir = Path("/Users/chengkai48/Documents/AI/oxygent-doc-website/content/docs")

    files = [
        "agents-rag.zh-CN.mdx",
        "agents-sse-agent.zh-CN.mdx",
        "flows-workflow.zh-CN.mdx",
        "flows-parallel.zh-CN.mdx",
        "flows-plan-and-solve.zh-CN.mdx",
        "flows-reflexion.zh-CN.mdx",
        "flows-comparison.zh-CN.mdx",
        "llms-openai.zh-CN.mdx",
        "tools-function-hub.zh-CN.mdx",
        "tools-mcp-sse.zh-CN.mdx",
        "tools-mcp-streamable.zh-CN.mdx",
        "tools-mcp-comparison.zh-CN.mdx",
    ]

    total = 0

    print("=" * 60)
    print("处理剩余内容")
    print("=" * 60)
    print()

    for filename in files:
        file_path = docs_dir / filename
        if file_path.exists():
            changes = process_file(file_path)
            total += changes
        print()

    print("=" * 60)
    print(f"完成！总计 {total} 处修改")
    print("=" * 60)


if __name__ == "__main__":
    main()
