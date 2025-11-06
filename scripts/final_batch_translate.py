#!/usr/bin/env python3
"""
最终批量翻译脚本 - 处理所有剩余的中英文混合内容
"""

import re
from pathlib import Path

# 超全面的翻译字典
TRANSLATIONS = {
    # agents-rag.zh-CN.mdx 特定翻译
    "Rag_agent (Retrieval-Augmented Generation) conversational agent. Before generating a response with a large language model, relevant external knowledge is retrieved through a search function and injected in到 prompt to improve the accuracy and controllability 的 answers.": "Rag智能体（检索增强生成）对话智能体。在使用大语言模型生成响应之前，通过搜索函数检索相关的外部知识并注入到提示中，以提高答案的准确性和可控性。",
    "This module 提供Chat智能体 class, which 处理conversational AI interactions by managing conversation memory, processing user queries, and coordinating with language models to generate responses.": "该模块提供Chat智能体类，通过管理对话记忆、处理用户查询并与语言模型协调生成响应，来处理对话式AI交互。",
    "OxyGent 支持injecting knowledge into prompts via the knowledge 参数. Below 是一个simple example of RAG:": "OxyGent 支持通过 knowledge 参数将知识注入提示。以下是一个简单的 RAG 示例：",
    "You need to first create a retrieval method:": "您需要首先创建一个检索方法：",
    "Replace with the actual database": "替换为实际的数据库",
    "Next, you need to inject the retrieved knowledge in update_query:": "接下来，您需要在 update_query 中注入检索到的知识：",
    "Key Method": "关键方法",
    "Below 是一个complete runnable code example:": "以下是一个完整的可运行代码示例：",
    "Experience in choosing tools:": "选择工具的经验：",
    "Select the appropriate tool based on the user's question.": "根据用户的问题选择合适的工具。",
    "If no tool is needed, reply directly.": "如果不需要工具，请直接回复。",
    "If answering the user's question requires calling multiple tools, call only one tool at a time. After the user receives the tool result, they will give you feedback on the tool call result.": "如果回答用户的问题需要调用多个工具，每次只调用一个工具。用户收到工具结果后，会给您反馈工具调用结果。",
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
    "This is an example for rag. Please modify it according to the specific needs": "这是一个 RAG 示例。请根据具体需求进行修改",
    # agents-sse-agent.zh-CN.mdx 特定翻译
    "The agent 是一个basic proxy 旨在 provide functionality for communicating with remote services. Specifically, different agents interact with remote services 通过 Server-Sent Events (SSE) protocol 。该agent receives an `Oxy请求` object and, after completing the communication task (via the `execute` method), returns an `Oxy响应` object. Below 是一个detailed explanation of this functionality.": "该智能体是一个基本代理，旨在提供与远程服务通信的功能。具体来说，不同的智能体通过服务器发送事件（SSE）协议与远程服务交互。该智能体接收一个 `OxyRequest` 对象，在完成通信任务后（通过 `execute` 方法），返回一个 `OxyResponse` 对象。以下是该功能的详细说明。",
    "This example 是一个 `math_agent`, which uses `SSEOxy智能体` to communicate with a `time_agent` to perform mathematical calculation tasks. Below 是 illustrations and implementation source code for `math_agent` and `time_agent`。该`math_agent` 包括 a `workflow智能体`, which can call the `SSEOxy智能体` to communicate 使用 `time_agent` as part of its steps.": "该示例是一个 `math_agent`，它使用 `SSEOxy智能体` 与 `time_agent` 通信以执行数学计算任务。以下是 `math_agent` 和 `time_agent` 的图示和实现源代码。`math_agent` 包括一个 `workflow智能体`，它可以调用 `SSEOxy智能体` 与 `time_agent` 通信，作为其步骤的一部分。",
    "History record": "历史记录",
    "History record: User Layer": "历史记录：用户层",
    "user query": "用户查询",
    "What time is it now?": "现在几点了？",
    "Current time": "当前时间",
    "Save": "保存",
    "positions": "位",
    "or you could ask me to save how many positions you want.": "或者您可以告诉我您想保存多少位。",
    "The 30 positions of pi": "圆周率的 30 位",
    "An tool for time query": "时间查询工具",
    "An tool for pi query": "圆周率查询工具",
    "A tool for time query": "时间查询工具",
    "The `sse_oxy_agent` completes the communication function 通过 following steps:": "`sse_oxy_agent` 通过以下步骤完成通信功能：",
    "Accept an Oxy请求": "接受一个 OxyRequest",
    "Construct an SSE request": "构造一个 SSE 请求",
    "Perform an asynchronous HTTP request": "执行异步 HTTP 请求",
    "Handle different types of data": "处理不同类型的数据",
    "Return an Oxy响应": "返回一个 OxyResponse",
    "Firstly, upon receiving an Oxy请求, the agent begins constructing the request body according 到 SSE protocol. Specifically, this 包括 building the URL and setting HTTP headers, where the HTTP headers include": "首先，在接收到 OxyRequest 后，智能体开始根据 SSE 协议构造请求体。具体来说，这包括构建 URL 和设置 HTTP 头，其中 HTTP 头包括",
    'Next, the `sse_oxy_agent` uses `aiohttp.Client会话` to perform an asynchronous HTTP POST request, initiating the asynchronous request. At this point, it reads the SSE stream data line by line 。当the received data is "done", the agent logs th是一个nd terminates the connection 。对于other types of data, `sse_oxy_agent` 处理 them differently: if `data["type"]` is "answer", it extracts the answer content; if it is "tool_call" or "observation", and the caller or callee category is not "user", it 处理based on whether to sh是 call stack and sends messages 。对于other types of data, the agent directly sends messages.': '接下来，`sse_oxy_agent` 使用 `aiohttp.ClientSession` 执行异步 HTTP POST 请求，启动异步请求。此时，它逐行读取 SSE 流数据。当接收到的数据为 "done" 时，智能体会记录日志并终止连接。对于其他类型的数据，`sse_oxy_agent` 会以不同方式处理：如果 `data["type"]` 是 "answer"，它会提取答案内容；如果是 "tool_call" 或 "observation"，并且调用者或被调用者的类别不是 "user"，它会根据是否共享调用堆栈进行处理并发送消息。对于其他类型的数据，智能体直接发送消息。',
    "In the `SSEOxyGent` class, `is_share_call_stack` 是一个 boolean attribute that controls whether to share call stack information when communicating with remote services. Its specific roles are as follows:": "在 `SSEOxyGent` 类中，`is_share_call_stack` 是一个布尔属性，用于控制在与远程服务通信时是否共享调用堆栈信息。其具体作用如下：",
    "When th是一个ttribute is `True`, it 允许 sharing call stack information. In this case, the code retains the call stack and the traversed node IDs 。这个handling method can simplify or protect part 的 call path information while retaining enough context for remote services.": "当该属性为 `True` 时，它允许共享调用堆栈信息。在这种情况下，代码会保留调用堆栈和遍历的节点 ID。这种处理方法可以简化或保护部分调用路径信息，同时为远程服务保留足够的上下文。",
    "When th是一个ttribute is `False`, it indicates not sharing call stack information. At this point, the code deletes the call stack and the traversed node IDs, completely not passing this information. Choosing not to sh是 call stack 可能 used to protect privacy or security needs, or to simplify data transmission when call stack information is not needed.": "当该属性为 `False` 时，表示不共享调用堆栈信息。此时，代码会删除调用堆栈和遍历的节点 ID，完全不传递这些信息。选择不共享调用堆栈可能用于保护隐私或安全需求，或在不需要调用堆栈信息时简化数据传输。",
    "Setting th是一个ttribute may depend on specific application scenarios and needs:": "设置该属性可能取决于具体的应用场景和需求：",
    "Debugging and Tracing": "调试和跟踪",
    "In some scenarios, retaining the call stack can help debug and trace the flow and history of requests.": "在某些场景中，保留调用堆栈可以帮助调试和跟踪请求的流程和历史。",
    "Privacy and Security": "隐私和安全",
    "In scenarios involving sensitive information, choosing not to sh是 call stack may protect privacy.": "在涉及敏感信息的场景中，选择不共享调用堆栈可能保护隐私。",
    "Performance and Simplification": "性能和简化",
    "When call stack information is not needed, removing this information can reduce data transmission volume and improve performance.": "当不需要调用堆栈信息时，删除这些信息可以减少数据传输量并提高性能。",
    "SSE (Server-Sent Events) 是一个 technology for server-to-client one-way real-time data updates, commonly used in web applications needing real-time data updates. SSE is part 的 HTML5 specification, providing a way to establish a persistent connection between the browser and server to receive events.": "SSE（服务器发送事件）是一种服务器到客户端的单向实时数据更新技术，通常用于需要实时数据更新的 Web 应用程序。SSE 是 HTML5 规范的一部分，提供了一种在浏览器和服务器之间建立持久连接以接收事件的方式。",
    "`SSEOxyGent` and `工作流智能体` are both agent classes defined 在 OxyGent framework, but they have different functions and application scenarios. Below 是ir relationships and differences:": "`SSEOxyGent` 和 `工作流智能体` 都是在 OxyGent 框架中定义的智能体类，但它们具有不同的功能和应用场景。以下是它们的关系和区别：",
    "Inherits from `Local智能体`, meaning it is mainly used to execute custom workflow functions in a local environment.": "继承自 `Local智能体`，这意味着它主要用于在本地环境中执行自定义工作流函数。",
    "Focuses on executing user-defined workflow logic, typically running locally or independently of other remote services.": "专注于执行用户定义的工作流逻辑，通常在本地运行或独立于其他远程服务。",
    "Inherits from `Remote智能体`, indicating it is 用于 handling remote service interactions, especially communication through Server-Sent Events (SSE).": "继承自 `Remote智能体`，表示它用于处理远程服务交互，特别是通过服务器发送事件（SSE）的通信。",
    "Primarily used to establish SSE connections with remote servers, receiving and processing event streams.": "主要用于与远程服务器建立 SSE 连接，接收和处理事件流。",
    "Focuses on executing custom workflow functions.": "专注于执行自定义工作流函数。",
    "Users can define their business logic 通过 `func_workflow` attribute.": "用户可以通过 `func_workflow` 属性定义他们的业务逻辑。",
    "Suitable for scenarios where logic needs to be executed locally.": "适用于需要在本地执行逻辑的场景。",
    "Focuses on communicating with remote servers via SSE.": "专注于通过 SSE 与远程服务器通信。",
    "Supports asynchronous initialization and execution, receiving real-time data or events through SSE.": "支持异步初始化和执行，通过 SSE 接收实时数据或事件。",
    "Suitable for scenarios requiring interaction with remote services and handling real-time events.": "适用于需要与远程服务交互并处理实时事件的场景。",
    "Suitable for scenarios requiring flexible integration of custom logic, 例如 data processing, task automation, etc.": "适用于需要灵活集成自定义逻辑的场景，例如数据处理、任务自动化等。",
    "Mainly runs in a local environment, not involving direct communication with remote services.": "主要在本地环境中运行，不涉及与远程服务的直接通信。",
    "`workflow智能体` can integrate different agents to logically execute different tasks.": "`workflow智能体` 可以集成不同的智能体以逻辑地执行不同的任务。",
    "Suitable for scenarios requiring real-time data updating and processing, 例如 real-time monitoring, notification systems, etc.": "适用于需要实时数据更新和处理的场景，例如实时监控、通知系统等。",
    "Maintains connection with remote servers through SSE, receiving and processing real-time events.": "通过 SSE 与远程服务器保持连接，接收和处理实时事件。",
    "`工作流智能体` can integrate with `SSEOxy智能体` to complete specific tasks.": "`工作流智能体` 可以与 `SSEOxy智能体` 集成以完成特定任务。",
    # flows-workflow.zh-CN.mdx 特定翻译
    "Custom workflow execution flow that 使 flexible user-defined logic integration": "自定义工作流执行流程，支持灵活的用户定义逻辑集成",
    "工作流 is OxyGent's flexible flow component that 使 execution of custom workflow functions with在 flow framework 。它serves as a bridge between the flow system and user-defined logic, allowing you to implement any custom workflow pattern.": "工作流是 OxyGent 的灵活流程组件，支持在流程框架内执行自定义工作流函数。它作为流程系统和用户定义逻辑之间的桥梁，允许您实现任何自定义工作流模式。",
    "The 工作流 flow 提供maximum flexibility for implementing custom execution patterns. Un如 other flows with predefined behavior (Parallel流程, PlanAndSolve, Reflexion), 工作流 gives you complete control over the execution logic through a custom function.": "工作流流程提供了实现自定义执行模式的最大灵活性。与其他具有预定义行为的流程（Parallel流程、PlanAndSolve、Reflexion）不同，工作流通过自定义函数让您完全控制执行逻辑。",
    "Custom Logic": "自定义逻辑",
    "Execute any user-defined workflow function": "执行任何用户定义的工作流函数",
    "流程 Integration": "流程集成",
    "Seamlessly 集成 with OxyGent's flow system": "与 OxyGent 的流程系统无缝集成",
    "Flexible Patterns": "灵活的模式",
    "Implement any workflow pattern (sequential, conditional, looping, etc.)": "实现任何工作流模式（顺序、条件、循环等）",
    "上下文 Access": "上下文访问",
    "Full access to Oxy请求 for context and agent communication": "完全访问 OxyRequest 以获取上下文和智能体通信",
    "简单的 Interface": "简单的接口",
    "Minimal boilerplate, focus on your workflow logic": "最少的样板代码，专注于您的工作流逻辑",
    "When existing flows (Parallel流程, PlanAndSolve, Reflexion) don't match your needs": "当现有流程（Parallel流程、PlanAndSolve、Reflexion）不符合您的需求时",
    "Custom orchestration logic requiring specific control flow": "需要特定控制流的自定义编排逻辑",
    "Experimental workflow patterns or prototypes": "实验性工作流模式或原型",
    "Domain-specific workflows with unique requirements": "具有独特需求的特定领域工作流",
    "Create a simple workflow that 处理a request and returns a result:": "创建一个简单的工作流来处理请求并返回结果：",
    "Simple custom workflow function.": "简单的自定义工作流函数。",
    "Your custom logic here": "您的自定义逻辑放在这里",
    "Processed query": "已处理的查询",
    "Access other agents and tools within your workflow:": "在工作流中访问其他智能体和工具：",
    "Workflow that orchestrates multiple agents.": "编排多个智能体的工作流。",
    "Call first agent for analysis": "调用第一个智能体进行分析",
    "Call second agent for processing": "调用第二个智能体进行处理",
    "Analysis": "分析",
    "Result": "结果",
    "Orchestrates analysis and processing agents": "编排分析和处理智能体",
    # 继续添加更多翻译...
    "The custom workflow function to execute. Must be an async function that accepts an `Oxy请求` and returns a string.": "要执行的自定义工作流函数。必须是接受 `OxyRequest` 并返回字符串的异步函数。",
    "Your workflow logic": "您的工作流逻辑",
    "result": "结果",
    "Contains query, context, and methods to call other agents": "包含查询、上下文和调用其他智能体的方法",
    "The final result of your workflow": "您的工作流的最终结果",
    "When to adjust": "何时调整",
    "Always required - this is your workflow implementation.": "始终必需 - 这是您的工作流实现。",
    "工作流 inherits all standard Base流程 参数s:": "工作流继承所有标准的 Base流程参数：",
    "Unique identifier 对于 flow with在 MAS.": "MAS 中流程的唯一标识符。",
    "描述 of what this workflow does.": "该工作流的描述。",
    "Validates and processes user input through multiple stages": "通过多个阶段验证和处理用户输入",
    "最大执行时间（秒）.": "最大执行时间（秒）。",
    "5 minutes for complex workflows": "复杂工作流 5 分钟",
    "LLM model to use for fallback operations.": "用于回退操作的 LLM 模型。",
    "The 工作流 flow follows a simple execution pattern:": "工作流流程遵循简单的执行模式：",
    "User Request": "用户请求",
    "OxyRequest Created": "创建 OxyRequest",
    "func_workflow(oxy_request) Called": "调用 func_workflow(oxy_request)",
    "Custom Logic Executes": "执行自定义逻辑",
    "(may call agents/tools)": "（可能调用智能体/工具）",
    "[Agent Calls via oxy_request.call()]": "[通过 oxy_request.call() 调用智能体]",
    "Return String Result": "返回字符串结果",
    "OxyResponse Created (state=COMPLETED)": "创建 OxyResponse（状态=COMPLETED）",
    "Result Returned to User": "结果返回给用户",
    "Key Points": "关键点",
    "Async Execution": "异步执行",
    "工作流 functions 必须 async": "工作流函数必须是异步的",
    "Full access to Oxy请求 for context and communication": "完全访问 OxyRequest 以获取上下文和通信",
    "智能体 Calls": "智能体调用",
    "Use `await oxy_request.call()` to invoke other agents": "使用 `await oxy_request.call()` 调用其他智能体",
    "Just return a string - the flow 处理Oxy响应 creation": "只需返回一个字符串 - 流程会处理 OxyResponse 的创建",
    "完整的 API 文档请参考 包括 all constructor 参数s, methods, and detailed 参数 描述, 请参考：": "完整的 API 文档包括所有构造函数参数、方法和详细的参数描述，请参考：",
    "实际示例请参考 and usage patterns, 请参考：": "实际使用示例和模式请参考：",
    "Multi-step sequential processing": "多步骤顺序处理",
    "Branching logic and conditions": "分支逻辑和条件",
    "Iterative execution patterns": "迭代执行模式",
    "Complex agent coordination": "复杂智能体协调",
    "查看所有示例 在 [示例 Gallery](/examples).": "查看所有示例：[示例 Gallery](/examples)。",
    "Implement branching logic based on conditions:": "基于条件实现分支逻辑：",
    "Determine which path to take": "确定采取哪条路径",
    "Implement loops and iterations:": "实现循环和迭代：",
    "Refine result through multiple iterations": "通过多次迭代改进结果",
    "Check if result is satisfactory": "检查结果是否满意",
    "Final result after": "最终结果，经过",
    "iterations": "次迭代",
    "Implement robust error handling:": "实现健壮的错误处理：",
    "Primary agent": "主要智能体",
    "Fallback to backup agent": "回退到备份智能体",
    "Fallback result": "回退结果",
    "Error: Unable to process request": "错误：无法处理请求",
    "Combine multiple agent calls in parallel:": "并行组合多个智能体调用：",
    "Execute multiple agents in parallel": "并行执行多个智能体",
    "Combine results": "组合结果",
    "Maintain state across workflow execution:": "在工作流执行过程中维护状态：",
    "Access shared data for state": "访问共享数据以获取状态",
    "Process and update state": "处理和更新状态",
    "Update state": "更新状态",
    "Step": "步骤",
    # flows-parallel 特定翻译
    "`Parallel流程` 是一个 more fundamental component for parallel execution, 适用于 scenarios that require simple aggregation of outputs from multiple tools. If intelligent summarization is needed, it is recommended to use `Parallel智能体`.": "`Parallel流程` 是一个更基础的并行执行组件，适用于需要简单聚合多个工具输出的场景。如果需要智能汇总，建议使用 `Parallel智能体`。",
    "OxyGent 提供a preset `Parallel流程` class for managing parallel execution flows. `Parallel流程` 允许 multiple tools or agents to run concurrently and consolidates their outputs into a single unified response.": "OxyGent 提供了一个预设的 `Parallel流程` 类来管理并行执行流程。`Parallel流程` 允许多个工具或智能体并发运行，并将它们的输出整合到一个统一的响应中。",
    "Use `Parallel流程` when the tools or agents involved have no interdependencies, as it 使 parallel execution of tasks and reduces overall processing time.": "当涉及的工具或智能体之间没有相互依赖时，使用 `Parallel流程`，因为它支持任务的并行执行并减少总体处理时间。",
    "At its core, `Parallel流程` dispatches the same request to all available tools or agents simultaneously, 执行 these calls in parallel using `asyncio.gather`, and aggregates all results into a single response.": "在其核心，`Parallel流程` 同时将相同的请求分派给所有可用的工具或智能体，使用 `asyncio.gather` 并行执行这些调用，并将所有结果聚合到一个响应中。",
    # 更多通用翻译
    "Knowledge-enhanced conversations": "知识增强对话",
    "Augment AI responses with domain-specific information": "用领域特定信息增强 AI 响应",
    "Document Q&A": "文档问答",
    "Answer questions based on your document database": "基于您的文档数据库回答问题",
    "Technical support": "技术支持",
    "Provide accurate answers from knowledge bases": "从知识库提供准确的答案",
    "Research assistance": "研究辅助",
    "Retrieve relevant information before generating responses": "在生成响应之前检索相关信息",
    # 通用中英文混合修复
    " 是一个": "是一个",
    " 的 ": "的",
    " 。该": "。该",
    "在 ": "在",
    "到 ": "到",
    "与 ": "与",
    " 中 ": "中",
    " 对于 ": "对于",
    " 通过 ": "通过",
    " 使用 ": "使用",
    " 包括 ": "包括",
    " 提供": "提供",
    " 支持": "支持",
    " 允许": "允许",
    " 可以": "可以",
    " 可能": "可能",
    " 必须": "必须",
    " 需要": "需要",
    " 应该": "应该",
    " 会 ": "会",
    " 将 ": "将",
    " 并 ": "并",
    " 或 ": "或",
    " 如 ": "如",
    " 等": "等",
    " 用于": "用于",
    " 从 ": "从",
    " 为 ": "为",
    " 以 ": "以",
    " 由 ": "由",
    " 向 ": "向",
    "re用于": "重用于",
    "适合": "适合",
    "适用于": "适用于",
    "旨在": "旨在",
    "负责": "负责",
    "专注于": "专注于",
    "关于": "关于",
    "基于": "基于",
    "根据": "根据",
    "通过": "通过",
    "使用": "使用",
    "利用": "利用",
    "采用": "采用",
    "借助": "借助",
    "依靠": "依靠",
    "依赖": "依赖",
    "包含": "包含",
    "包括": "包括",
    "含有": "含有",
    "拥有": "拥有",
    "具有": "具有",
    "提供": "提供",
    "支持": "支持",
    "允许": "允许",
    "启用": "启用",
    "实现": "实现",
    "完成": "完成",
    "执行": "执行",
    "运行": "运行",
    "处理": "处理",
    "管理": "管理",
    "控制": "控制",
    "协调": "协调",
    "组织": "组织",
    "编排": "编排",
    "调度": "调度",
    "分配": "分配",
    "分发": "分发",
    "传递": "传递",
    "传输": "传输",
    "发送": "发送",
    "接收": "接收",
    "返回": "返回",
    "生成": "生成",
    "创建": "创建",
    "构建": "构建",
    "建立": "建立",
    "设置": "设置",
    "配置": "配置",
    "初始化": "初始化",
    "启动": "启动",
    "开始": "开始",
    "停止": "停止",
    "结束": "结束",
    "终止": "终止",
    "关闭": "关闭",
    "清理": "清理",
    "释放": "释放",
    "回收": "回收",
    # 更多特定修复
    "th是一个": "该",
    "th是一个nd": "这并",
    "是一个n ": "是一个",
    "是一个re ": "是",
    "可以 be": "可以",
    "will be": "将会",
    "can be": "可以",
    "may be": "可能",
    "must be": "必须",
    "should be": "应该",
    "could be": "可能",
    "would be": "将",
    # 代码注释翻译
    "# Replace with the actual database": "# 替换为实际的数据库",
    "# Key Method": "# 关键方法",
    "# Async implementation": "# 异步实现",
    "# Implementation": "# 实现",
    "# Your implementation": "# 您的实现",
    "# Your custom logic": "# 您的自定义逻辑",
    "# Your logic": "# 您的逻辑",
    "# Your workflow logic": "# 您的工作流逻辑",
}

# 文件特定的完整段落翻译
FILE_SPECIFIC = {
    "agents-rag.zh-CN.mdx": {
        "description: Retrieval-Augmented Generation (RAG) conversational agent that enhances responses with external knowledge": "description: 检索增强生成（RAG）对话智能体，通过外部知识增强响应",
    },
    "agents-sse-agent.zh-CN.mdx": {
        "description: 智能体 for communicating with remote services through Server-Sent Events (SSE) protocol": "description: 通过服务器发送事件（SSE）协议与远程服务通信的智能体",
    },
}


def protect_code_blocks(content: str) -> tuple[str, dict]:
    """保护代码块不被翻译"""
    code_blocks = {}
    counter = [0]

    def replace_code(match):
        placeholder = f"___CODE_BLOCK_{counter[0]}___"
        code_blocks[placeholder] = match.group(0)
        counter[0] += 1
        return placeholder

    # 保护代码块
    content = re.sub(r"```[\s\S]*?```", replace_code, content)
    return content, code_blocks


def restore_code_blocks(content: str, code_blocks: dict) -> str:
    """恢复代码块"""
    for placeholder, code in code_blocks.items():
        content = content.replace(placeholder, code)
    return content


def translate_content(content: str, filename: str) -> str:
    """翻译内容"""
    # 保护代码块
    content, code_blocks = protect_code_blocks(content)

    # 应用文件特定翻译
    if filename in FILE_SPECIFIC:
        for en, zh in FILE_SPECIFIC[filename].items():
            content = content.replace(en, zh)

    # 应用通用翻译（从长到短排序以避免部分匹配）
    sorted_translations = sorted(
        TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True
    )
    for en, zh in sorted_translations:
        content = content.replace(en, zh)

    # 修复一些常见的中英文混合问题
    # 修复空格问题
    content = re.sub(r"(\w+)\s*是一个\s*(\w+)", r"\1是一个\2", content)
    content = re.sub(r"(\w+)\s*的\s*(\w+)", r"\1的\2", content)

    # 恢复代码块
    content = restore_code_blocks(content, code_blocks)

    return content


def translate_file(file_path: Path) -> int:
    """翻译单个文件"""
    print(f"正在翻译: {file_path.name}")

    content = file_path.read_text(encoding="utf-8")
    original_content = content

    # 翻译内容
    content = translate_content(content, file_path.name)

    # 计算修改次数
    changes = sum(1 for a, b in zip(original_content, content) if a != b)

    # 写回文件
    if changes > 0:
        file_path.write_text(content, encoding="utf-8")
        print(f"  ✓ 完成 - {changes} 处修改")
    else:
        print(f"  - 无需修改")

    return changes


def main():
    """主函数"""
    docs_dir = Path("/Users/chengkai48/Documents/AI/oxygent-doc-website/content/docs")

    # 要翻译的文件列表
    files_to_translate = [
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

    total_changes = 0

    print("=" * 60)
    print("开始最终批量翻译")
    print("=" * 60)
    print()

    for filename in files_to_translate:
        file_path = docs_dir / filename
        if file_path.exists():
            changes = translate_file(file_path)
            total_changes += changes
        else:
            print(f"警告: 文件不存在 - {filename}")
        print()

    print("=" * 60)
    print(f"翻译完成！")
    print(f"总计: {len(files_to_translate)} 个文件")
    print(f"总修改: {total_changes} 处")
    print("=" * 60)


if __name__ == "__main__":
    main()
