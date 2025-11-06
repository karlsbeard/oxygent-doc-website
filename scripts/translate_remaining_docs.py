#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译剩余的文档文件
处理 lifecycle, context, agents-react, agents-workflow, agents-parallel
"""

import re
from pathlib import Path

# 综合翻译字典
COMPREHENSIVE_TRANSLATIONS = {
    # ====== lifecycle.zh-CN.mdx ======
    "title: 生命周期 Management": "title: 生命周期管理",
    "理解 OxyGent's component lifecycle, state management, and resource cleanup patterns": 
        "理解 OxyGent 的组件生命周期、状态管理和资源清理模式",
    
    "OxyGent 实现 a comprehensive lifecycle management system that governs how components (agents, tools, flows) are initialized, executed, and cleaned up. 理解 this lifecycle is crucial for building reliable, resource-efficient multi-agent systems.":
        "OxyGent 实现了一个全面的生命周期管理系统，管理组件（智能体、工具、流程）如何初始化、执行和清理。理解这个生命周期对于构建可靠、资源高效的多智能体系统至关重要。",
    
    "The OxyGent lifecycle system operates at two primary levels:":
        "OxyGent 生命周期系统在两个主要级别运行：",
    
    "1. **MAS (Multi-智能体 System) 生命周期**: Application-level initialization and cleanup":
        "1. **MAS（多智能体系统）生命周期**：应用程序级初始化和清理",
    
    "2. **Component Execution 生命周期**: 请求-level processing for agents and tools":
        "2. **组件执行生命周期**：智能体和工具的请求级处理",
    
    "- **Async 上下文 Management**: Automatic resource setup and teardown using `async with`":
        "- **异步上下文管理**：使用 `async with` 自动设置和清理资源",
    
    "- **Structured Execution 流程**: Pre-process → Execute → Post-process hooks":
        "- **结构化执行流程**：预处理 → 执行 → 后处理钩子",
    
    "- **State Tracking**: Comprehensive state management for monitoring execution":
        "- **状态跟踪**：用于监控执行的全面状态管理",
    
    "- **Resource Cleanup**: Guaranteed cleanup even when errors occur":
        "- **资源清理**：即使发生错误也保证清理",
    
    "- **Database Persistence**: Automatic saving of traces and execution history":
        "- **数据库持久化**：自动保存追踪和执行历史",
    
    "### Component States": "### 组件状态",
    
    "OxyGent tracks execution state 通过 `OxyState` enum:":
        "OxyGent 通过 `OxyState` 枚举跟踪执行状态：",
    
    "| State | 描述 | When Applied |": "| 状态 | 描述 | 何时应用 |",
    "| `CREATED` | Component instantiated but not started | Initial state |":
        "| `CREATED` | 组件已实例化但未启动 | 初始状态 |",
    "| `RUNNING` | Currently executing | During execution |":
        "| `RUNNING` | 当前正在执行 | 执行期间 |",
    "| `COMPLETED` | Successfully finished | Normal completion |":
        "| `COMPLETED` | 成功完成 | 正常完成 |",
    "| `FAILED` | Execution error occurred | Exception raised |":
        "| `FAILED` | 执行错误发生 | 抛出异常 |",
    "| `PAUSED` | Temporarily suspended | Manual pause |":
        "| `PAUSED` | 临时暂停 | 手动暂停 |",
    "| `SKIPPED` | Not executed (conditional) | 工作流 skip |":
        "| `SKIPPED` | 未执行（条件性）| 工作流跳过 |",
    "| `CANCELED` | Aborted before completion | User cancellation |":
        "| `CANCELED` | 完成前中止 | 用户取消 |",
    
    "### Basic MAS 生命周期": "### 基本 MAS 生命周期",
    
    "The MAS lifecycle is managed through Python's async context manager protocol:":
        "MAS 生命周期通过 Python 的异步上下文管理器协议管理：",
    
    "# __aenter__: Initialization phase": "# __aenter__：初始化阶段",
    "# MAS is fully initialized here": "# MAS 在这里完全初始化",
    "# - All components registered": "# - 所有组件已注册",
    "# - Databases connected": "# - 数据库已连接",
    "# - Agent organization built": "# - 智能体组织已构建",
    
    "# __aexit__: Cleanup phase (automatic)": "# __aexit__：清理阶段（自动）",
    "# - Close database connections": "# - 关闭数据库连接",
    "# - Wait for background tasks": "# - 等待后台任务",
    "# - Release resources": "# - 释放资源",
    
    # ====== context.zh-CN.mdx ======
    "title: Oxy请求 & 上下文": "title: OxyRequest & 上下文",
    "理解 the Oxy请求 API and context management in OxyGent":
        "理解 OxyGent 中的 OxyRequest API 和上下文管理",
    
    "**Oxy请求** 是 core context object that flows 通过 entire OxyGent system 。它serves as both a message envelope for agent-to-agent communication and a context manager providing access to memory, data scopes, and execution capabilities. Every agent, tool, and workflow receives an Oxy请求 and uses it to interact 使用rest 的 system.":
        "**OxyRequest** 是流经整个 OxyGent 系统的核心上下文对象。它既是智能体间通信的消息信封，也是提供访问内存、数据作用域和执行功能的上下文管理器。每个智能体、工具和工作流都接收一个 OxyRequest 并使用它与系统的其余部分交互。",
    
    "### 什么是 is Oxy请求?": "### 什么是 OxyRequest？",
    
    "Oxy请求 encapsulates:": "OxyRequest 封装了：",
    "- **Query & 内存**: Current query text and conversation history":
        "- **查询和内存**：当前查询文本和对话历史",
    "- **Data 域s**: Four levels of data sharing (arguments, shared_data, group_data, global_data)":
        "- **数据作用域**：四级数据共享（arguments、shared_data、group_data、global_data）",
    "- **Trace Information**: Conversation DAG structure and parent relationships":
        "- **追踪信息**：对话 DAG 结构和父级关系",
    "- **Execution API**: 方法s to call agents/tools and send messages":
        "- **执行 API**：调用智能体/工具和发送消息的方法",
    "- **Identity**: Unique IDs for tracking and resuming requests":
        "- **身份**：用于跟踪和恢复请求的唯一 ID",
    
    # ====== agents-react.zh-CN.mdx ======
    "The ReAct智能体 实现 the **ReAct (推理 and Acting)** paradigm, enabling autonomous agent behavior by combining language model reasoning with tool execution in an iterative loop.":
        "ReAct 智能体实现了 **ReAct（推理和行动）** 范式，通过在迭代循环中结合语言模型推理和工具执行来实现自主智能体行为。",
    
    "ReAct智能体 is OxyGent's most versatile agent for complex tasks requiring multiple tool interactions 。它intelligently alternates between:":
        "ReAct 智能体是 OxyGent 中用于需要多次工具交互的复杂任务的最通用智能体。它智能地在以下方面交替进行：",
    
    "1. **推理**: Using LLMs to analyze the task and decide next actions":
        "1. **推理**：使用 LLM 分析任务并决定下一步行动",
    "2. **Acting**: Executing tools based on reasoning decisions":
        "2. **行动**：基于推理决策执行工具",
    "3. **Observing**: Processing tool results to inform next reasoning step":
        "3. **观察**：处理工具结果以指导下一步推理",
    
    "This cycle continues until the agent reaches a satisfactory answer or hits the maximum iteration limit.":
        "这个循环持续进行，直到智能体达到满意的答案或达到最大迭代限制。",
    
    # ====== agents-workflow.zh-CN.mdx ======
    "title: 工作流 智能体": "title: 工作流智能体",
    
    "**工作流智能体** 是一个 specialized agent that 执行 custom workflow functions, providing full programmatic control over agent behavior. Un如 ReAct or Chat agents that rely on LLM reasoning, 工作流智能体 允许 you to define explicit logic flows using Python code while seamlessly integrating with other agents, tools, and LLMs.":
        "**工作流智能体** 是一个专门的智能体，执行自定义工作流函数，提供对智能体行为的完全程序化控制。与依赖 LLM 推理的 ReAct 或 Chat 智能体不同，工作流智能体允许您使用 Python 代码定义显式逻辑流程，同时与其他智能体、工具和 LLM 无缝集成。",
    
    # ====== agents-parallel.zh-CN.mdx ======
    "title: Parallel智能体": "title: 并行智能体",
    "description: 智能体 that 执行 tasks in parallel across multiple team members for enhanced thinking capabilities":
        "description: 在多个团队成员之间并行执行任务以增强思维能力的智能体",
    
    "Suppose you need to use agents to accomplish business needs, and if the capacity 的 agent model is small, you can use agent clusters to enhance your thinking skills. OxyGent natively 支持parallel work of agents, which can synthesize the execution results of multiple groups of agents and automatically summarize and reflect. You can arrange agents 如 a real work organization without worrying about conflicts between agents.":
        "假设您需要使用智能体来完成业务需求，如果智能体模型的能力较小，您可以使用智能体集群来增强思维能力。OxyGent 原生支持智能体的并行工作，可以综合多组智能体的执行结果并自动总结和反思。您可以像真实工作组织一样安排智能体，而无需担心智能体之间的冲突。",
    
    # ====== 通用短语 ======
    "实际示例请参考 and usage patterns, 请参考：":
        "实际示例和使用模式，请参考：",
    
    "查看所有示例 在 [示例 Gallery](/examples).":
        "查看 [示例库](/examples) 中的所有示例。",
    
    "实际使用示例和模式请参考：": "实际使用示例和模式，请参考：",
    
    "完整的 API 文档请参考 包括 all constructor 参数s, methods, and detailed 参数 描述, 请参考：":
        "完整的 API 文档，包括所有构造函数参数、方法和详细的参数描述，请参考：",
    
    "探索 practical implementations:": "探索实际实现：",
    
    # ====== 代码注释 ======
    "Pre-processing hook: Prepare request before execution.":
        "预处理钩子：在执行前准备请求。",
    "Access parent class pre-processing":
        "访问父类预处理",
    "Add custom pre-processing logic":
        "添加自定义预处理逻辑",
    "Main execution logic.": "主执行逻辑。",
    "Your agent implementation": "您的智能体实现",
    "Process the query": "处理查询",
    "Post-processing hook: Modify response after execution.":
        "后处理钩子：在执行后修改响应。",
    "Access parent class post-processing":
        "访问父类后处理",
    "Add custom post-processing logic":
        "添加自定义后处理逻辑",
    
    # Get the user's query
    "# Get the user's query": "# 获取用户的查询",
    "# Call a tool": "# 调用工具",
    "# Access memory context": "# 访问内存上下文",
    "# Get queries at different levels": "# 获取不同级别的查询",
    "# Send intermediate messages": "# 发送中间消息",
    "# Call an agent": "# 调用智能体",
    "# Call an LLM directly": "# 直接调用 LLM",
    "# Call a tool": "# 调用工具",
    
    # ====== 表格标题 ======
    "| 参数 | 类型 | 必需 | 描述 |": "| 参数 | 类型 | 必需 | 描述 |",
    "| 参数 | 类型 | 默认值 | 描述 |": "| 参数 | 类型 | 默认值 | 描述 |",
    
    # ====== 修复常见混合 ======
    " 是一个 ": " 是一个",
    " 的 ": " 的",
    " 通过 ": " 通过",
    " 使用": " 使用",
    "。它": "。它",
    "，它": "，它",
    " 对于 ": " ",
    " 在 ": " ",
    
    # Simple/Advanced mode
    "- **True**: 简单的 mode - only keeps final question-answer pairs":
        "- **True**：简单模式 - 只保留最终的问答对",
    "- **False**: Advanced mode - retains detailed ReAct reasoning steps with weighted scoring":
        "- **False**：高级模式 - 保留详细的 ReAct 推理步骤和加权评分",
    
    # For more detailed...
    "For more detailed configuration options and advanced features, please refer 到 source documentation.":
        "有关更详细的配置选项和高级功能，请参考源文档。",
    
    # Understanding
    "## 理解 ReAct Execution 流程": "## 理解 ReAct 执行流程",
    "## 理解 the Four 域s": "## 理解四大作用域",
    
    # Use Cases
    "### 使用场景": "### 使用场景",
    "**使用场景:**": "**使用场景：**",
    "**使用场景:**": "**使用场景：**",
    
    # WorkflowAgent specific
    "icon: 工作流": "icon: Workflow",
    
    "- **Custom Logic 流程**: Define explicit control flow using Python async functions":
        "- **自定义逻辑流程**：使用 Python 异步函数定义显式控制流",
    "- **Oxy请求 API**: Full access to memory, queries, messages, and agent calls":
        "- **OxyRequest API**：完全访问内存、查询、消息和智能体调用",
    "- **Seamless Integration**: Call other agents, tools, and LLMs from within workflows":
        "- **无缝集成**：从工作流内调用其他智能体、工具和 LLM",
    "- **Master 智能体 Support**: Can orchestrate multiple sub-agents as a master agent":
        "- **主智能体支持**：可以作为主智能体编排多个子智能体",
    "- **内存 Access**: Access both local and master-level memory contexts":
        "- **内存访问**：访问本地和主级别的内存上下文",
    "- **Flexible Composition**: Combine deterministic logic with AI capabilities":
        "- **灵活组合**：将确定性逻辑与 AI 能力相结合",
    
    # Calling Components
    "### Calling Components": "### 调用组件",
    "### Sending Messages": "### 发送消息",
    
    # ParallelAgent specific
    "## 定义": "## 定义",
    "## 适用场景": "## 适用场景",
    
    "This code demonstrates the design of a Multi-智能体 System (MAS) for conducting comprehensive feasibility assessments of AI product projects 。该system employs `Parallel智能体` to schedule multiple expert teams to work in parallel, achieving a true agentic working model:":
        "此代码演示了用于进行 AI 产品项目综合可行性评估的多智能体系统（MAS）的设计。该系统采用 `并行智能体` 调度多个专家团队并行工作，实现真正的智能体工作模式：",
    
    "- **Multi-expert analysis**: Gather opinions from multiple specialized agents":
        "- **多专家分析**：收集多个专业智能体的意见",
    "- **Comprehensive assessments**: Technical, business, risk, and legal evaluations":
        "- **全面评估**：技术、业务、风险和法律评估",
    "- **Team collaboration**: Multiple agents working on different aspects of a problem":
        "- **团队协作**：多个智能体处理问题的不同方面",
    "- **Enhanced decision-making**: Synthesize diverse perspectives for better decisions":
        "- **增强决策**：综合不同观点以做出更好的决策",
}

def translate_file(file_path):
    """翻译单个文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"翻译: {file_path.name}")
        
        # 保护代码块
        code_blocks = []
        def save_code(match):
            code_blocks.append(match.group(0))
            return f"__CODE_BLOCK_{len(code_blocks)-1}__"
        
        content = re.sub(r"```[\s\S]*?```", save_code, content)
        
        # 应用翻译（从长到短）
        translations = sorted(COMPREHENSIVE_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
        
        for en, zh in translations:
            content = content.replace(en, zh)
        
        # 恢复代码块
        for i, code_block in enumerate(code_blocks):
            content = content.replace(f"__CODE_BLOCK_{i}__", code_block)
        
        # 计算变化
        with open(file_path, "r", encoding="utf-8") as f:
            original = f.read()
        
        changes = sum(1 for a, b in zip(original, content) if a != b)
        changes += abs(len(original) - len(content))
        
        if changes > 0:
            # 写回文件
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
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
    
    # 要翻译的文件列表
    files_to_translate = [
        "lifecycle.zh-CN.mdx",
        "context.zh-CN.mdx",
        "agents-react.zh-CN.mdx",
        "agents-workflow.zh-CN.mdx",
        "agents-parallel.zh-CN.mdx",
    ]
    
    print(f"开始翻译 {len(files_to_translate)} 个文件...\n")
    
    translated_count = 0
    
    for filename in files_to_translate:
        file_path = docs_dir / filename
        if file_path.exists():
            if translate_file(file_path):
                translated_count += 1
        else:
            print(f"⚠️  文件不存在: {filename}\n")
    
    print(f"{'='*60}")
    print(f"✅ 完成！处理了 {translated_count}/{len(files_to_translate)} 个文件")
    print(f"\n翻译内容：")
    print(f"  ✓ lifecycle.zh-CN.mdx - 生命周期管理")
    print(f"  ✓ context.zh-CN.mdx - OxyRequest & 上下文")
    print(f"  ✓ agents-react.zh-CN.mdx - ReAct 智能体")
    print(f"  ✓ agents-workflow.zh-CN.mdx - 工作流智能体")
    print(f"  ✓ agents-parallel.zh-CN.mdx - 并行智能体")

if __name__ == "__main__":
    main()

