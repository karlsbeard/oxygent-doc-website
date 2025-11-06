#!/usr/bin/env python3
"""
最终润色所有文件 - 翻译提示词和其他剩余英文
"""

import re
from pathlib import Path


def translate_prompts(content: str) -> str:
    """翻译提示词模板"""

    translations = {
        # agents-rag.zh-CN.mdx 的 INSTRUCTION
        "You are a helpful assistant and can use these tools:": "您是一个有帮助的助手，可以使用这些工具：",
        "Experience in choosing tools:": "选择工具的经验：",
        "Select the appropriate tool based on the user's question.": "根据用户的问题选择合适的工具。",
        "If no tool is needed, reply directly.": "如果不需要工具，请直接回复。",
        "If answering the user's question requires calling multiple tools, call only one tool at a time. After the user receives the tool result, they will give you feedback on the tool call result.": "如果回答用户的问题需要调用多个工具，请一次只调用一个工具。用户收到工具结果后，会给您工具调用结果的反馈。",
        "Important notes:": "重要提示：",
        "When you have collected enough information to answer the user's question, please respond in the following format:": "当您收集到足够的信息来回答用户的问题时，请使用以下格式响应：",
        "Your reasoning (if analysis is needed)": "您的推理（如果需要分析）",
        "Your response content": "您的响应内容",
        "When you find that the user's question lacks certain conditions, you can ask them back. Please respond in the following format:": "当您发现用户的问题缺少某些条件时，您可以反问他们。请使用以下格式响应：",
        "Your follow-up question to the user": "您对用户的后续问题",
        "When you need to use a tool, you must respond **only** with the following exact JSON object format, and nothing else:": "当您需要使用工具时，必须**仅**使用以下精确的 JSON 对象格式响应，不要添加其他内容：",
        "Tool name": "工具名称",
        "Parameter name": "参数名称",
        "Parameter value": "参数值",
        # 其他常见提示
        "This is an example for rag. Please modify it according to the specific needs": "这是一个 RAG 示例。请根据具体需求进行修改",
        "print your question": "打印您的问题",
        "Use the remote tools to help me": "使用远程工具帮助我",
        "Process streaming data": "处理流式数据",
        "Hello, workflow!": "你好，工作流！",
        "Hello, how are you?": "你好，你好吗？",
        "What is 5 + 3?": "5 + 3 等于多少？",
        "Use the remote tools to help me": "使用远程工具帮助我",
        # 示例代码中的字符串
        "Random pause for": "随机暂停",
        "seconds": "秒",
        "The revenue of companyA is": "公司A的收入是",
        "The revenue of companyB is": "公司B的收入是",
        "The revenue of companyC is": "公司C的收入是",
        "Answer: ": "答案：",
        "Please fetch revenue data for companies A, B, and C, and sort them from highest to lowest revenue": "请获取公司 A、B 和 C 的收入数据，并按收入从高到低排序",
        "Hi, I'm OxyGent. How can I assist you?": "你好，我是 OxyGent。我能帮您什么？",
        # 文件操作相关
        "Written to": "已写入",
        "Error: Division by zero": "错误：除以零",
        "Error:": "错误：",
        "Email sent": "邮件已发送",
        "User not found": "未找到用户",
        # 日志和调试
        "Tool called with param": "工具调用，参数",
        "Tool completed with result": "工具完成，结果",
        "Request started": "请求开始",
        "Completed in": "完成于",
        # 问候和响应
        "We've been chatting a lot! Hi again": "我们聊了很多！再次问好",
        "Hey": "嘿",
        "Hello": "你好",
        "How may I assist you today?": "今天我能为您做些什么？",
        # 错误消息
        "Answer is too short or empty. Please provide a more detailed and helpful response.": "答案太短或为空。请提供更详细和有帮助的响应。",
        "This is a greeting. Please respond in a more friendly and warm manner.": "这是一个问候。请以更友好和温暖的方式响应。",
        "Your answer doesn't seem helpful. Please try to provide a more constructive answer or suggest alternative solutions.": "您的答案似乎没有帮助。请尝试提供更具建设性的答案或建议替代解决方案。",
        "For mathematical problems, please provide a step-by-step solution showing your work process.": "对于数学问题，请提供逐步解决方案，显示您的工作过程。",
        # 工作流相关
        "Processed query:": "已处理的查询：",
        "Final answer optimized through": "经过优化的最终答案",
        "rounds of reflexion:": "轮反思：",
        "Answer after": "经过",
        "rounds of reflexion attempts:": "轮反思尝试后的答案：",
        # 评估相关
        "Please evaluate the quality of the following answer:": "请评估以下答案的质量：",
        "Original Question:": "原始问题：",
        "Answer:": "答案：",
        "Please return evaluation results in the following format:": "请使用以下格式返回评估结果：",
        "Evaluation Result: [Satisfactory/Unsatisfactory]": "评估结果：[满意/不满意]",
        "Evaluation Reason: [Specific reason]": "评估原因：[具体原因]",
        "Improvement Suggestions: [If unsatisfactory, provide specific improvement suggestions]": "改进建议：[如果不满意，请提供具体的改进建议]",
        "Evaluate this answer comprehensively:": "全面评估这个答案：",
        "Question:": "问题：",
        "Rate on scale 1-10 for:": "在 1-10 的范围内评分：",
        "- Accuracy and factual correctness": "- 准确性和事实正确性",
        "- Completeness of information": "- 信息完整性",
        "- Clarity and readability": "- 清晰度和可读性",
        "- Practical usefulness": "- 实用性",
        "- Professional tone": "- 专业语气",
        "Provide detailed feedback and specific improvement suggestions.": "提供详细反馈和具体的改进建议。",
        "Format:": "格式：",
        "- is_satisfactory: true/false (true only if all aspects score 8+)": "- is_satisfactory: true/false（仅当所有方面得分 8 分以上时为 true）",
        "- evaluation_reason: [Detailed scoring and analysis]": "- evaluation_reason: [详细评分和分析]",
        "- improvement_suggestions: [Specific actionable improvements]": "- improvement_suggestions: [具体可行的改进措施]",
        # 函数文档字符串
        "Custom reflection function to evaluate answer quality.": "自定义反思函数以评估答案质量。",
        "Agent answer to be evaluated": "要评估的智能体答案",
        "Current request context": "当前请求上下文",
        "Reflection message if improvement needed; None otherwise": "如果需要改进则返回反思消息；否则返回 None",
        "Basic checks": "基本检查",
        "Custom business logic checks": "自定义业务逻辑检查",
        "For greeting queries, expect friendly responses": "对于问候查询，期望友好的响应",
        "Check for common unhelpful responses": "检查常见的无用响应",
        "Specialized reflection function for mathematical problems.": "数学问题的专用反思函数。",
        "First apply basic checks": "首先应用基本检查",
        "Math-specific checks": "数学特定检查",
        "Expect step-by-step solutions": "期望逐步解决方案",
        # 工作流文档字符串
        "Workflow implementing an external reflection process:": "实现外部反思过程的工作流：",
        "Get user query": "获取用户查询",
        "Have worker_agent generate initial answer": "让 worker_agent 生成初始答案",
        "Have reflexion_agent evaluate answer quality": "让 reflexion_agent 评估答案质量",
        "If unsatisfactory, provide improvement suggestions and regenerate": "如果不满意，提供改进建议并重新生成",
        "Return final satisfactory answer": "返回最终满意的答案",
        "Execute": "执行",
        "输入 content for reflection": "输入反思内容",
        "Get reflection results": "获取反思结果",
        "Update query with reflection results": "使用反思结果更新查询",
        "If max iterations are used up, return the current best result": "如果达到最大迭代次数，返回当前最佳结果",
        # MCP 相关
        "Start server:": "启动服务器：",
        "Connect client:": "连接客户端：",
        "Problem: Server not running or wrong URL": "问题：服务器未运行或 URL 错误",
        "Solution: Verify server is running and URL is correct": "解决方案：验证服务器正在运行且 URL 正确",
        "Check port and path": "检查端口和路径",
        "Problem: Missing or invalid authentication": "问题：缺少或无效的身份验证",
        "Solution: Add proper authorization headers": "解决方案：添加正确的授权头",
        "Problem: Dynamic headers ignored": "问题：动态头被忽略",
        "Solution: Ensure is_keep_alive=False": "解决方案：确保 is_keep_alive=False",
        "动态请求头所需": "动态请求头所需",
        "Problem: 请求s timing out": "问题：请求超时",
        "Solution: Increase timeout": "解决方案：增加超时时间",
        "Increase to 2 minutes": "增加到 2 分钟",
        "Problem: Long-running streams timeout": "问题：长时间运行的流超时",
        "5 minutes for long streams": "长流 5 分钟",
        "Required": "必需",
        # 各种标签和提示
        "BEST": "最佳",
        "ADVANCED": "高级",
        "STANDARD": "标准",
        "Good": "好",
        "Bad": "差",
        "Recommendation:": "推荐：",
        "Why:": "原因：",
        "Example": "示例",
    }

    # 先处理提示词模板（在字符串中）
    for en, zh in sorted(translations.items(), key=lambda x: len(x[0]), reverse=True):
        content = content.replace(en, zh)

    return content


def clean_mixed_text(content: str) -> str:
    """清理混合文本"""

    # 修复常见的混合问题
    patterns = [
        (r"OxyGent\s*支持", "OxyGent 支持"),
        (r"update_query\s*中", "update_query 中"),
        (r"RAG\s*示例", "RAG 示例"),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    return content


def process_file(file_path: Path) -> int:
    """处理文件"""
    print(f"处理: {file_path.name}")

    content = file_path.read_text(encoding="utf-8")
    original = content

    content = translate_prompts(content)
    content = clean_mixed_text(content)

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
    print("最终润色")
    print("=" * 60)
    print()

    for filename in files:
        file_path = docs_dir / filename
        if file_path.exists():
            changes = process_file(file_path)
            total += changes
        print()

    print("=" * 60)
    print(f"✅ 完成！总计 {total} 处修改")
    print("=" * 60)


if __name__ == "__main__":
    main()
