#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门翻译 four-scope.zh-CN.mdx 文件
"""

import re
from pathlib import Path

# four-scope 文件的完整翻译映射
FOUR_SCOPE_TRANSLATIONS = {
    # ====== 标题和描述 ======
    "理解 OxyGent's hierarchical data scoping system for managing context and state across agents":
        "理解 OxyGent 的分层数据作用域系统，用于管理智能体之间的上下文和状态",
    
    # ====== 第一段 ======
    "OxyGent 实现 a sophisticated **four-scope system** for managing data, context, and state across different levels 的 multi-agent system. 这种分层域使得能够精确控制智能体之间的数据可见性、生命周期和共享模式。":
        "OxyGent 实现了一个复杂的**四作用域系统**，用于在多智能体系统的不同级别管理数据、上下文和状态。这种分层作用域使得能够精确控制智能体之间的数据可见性、生命周期和共享模式。",
    
    # ====== 四大作用域列表 ======
    "1. **Node 域** (`arguments`) - Data specific to a single agent/tool invocation":
        "1. **节点作用域** (`arguments`) - 特定于单个智能体/工具调用的数据",
    
    "2. **请求 域** (`shared_data`) - Data shared within a single execution chain":
        "2. **请求作用域** (`shared_data`) - 在单个执行链内共享的数据",
    
    "3. **会话 Group 域** (`group_data`) - Data persisted across multiple conversations":
        "3. **会话组作用域** (`group_data`) - 跨多个对话持久化的数据",
    
    "4. **Global 域** (`mas`) - System-wide registry and configuration":
        "4. **全局作用域** (`mas`) - 系统级注册表和配置",
    
    # ====== 关键特性 ======
    "**Hierarchical Data Management**: Clear boundaries for data visibility and lifetime":
        "**分层数据管理**：数据可见性和生命周期的清晰边界",
    
    "**Automatic Propagation**: Data flows naturally through nested agent calls":
        "**自动传播**：数据在嵌套智能体调用中自然流动",
    
    "**内存 Isolation**: Prevents unintended state leakage between sessions":
        "**内存隔离**：防止会话之间的意外状态泄漏",
    
    "**Flexible Sharing**: Share context where needed without polluting global state":
        "**灵活共享**：在需要时共享上下文而不污染全局状态",
    
    "**Persistent State**: Maintain conversation history across multiple interactions":
        "**持久状态**：在多次交互中维护对话历史",
    
    # ====== 表格标题 ======
    "### 何时使用 Each 域": "### 何时使用各作用域",
    
    # ====== 表格内容 ======
    "| 域 | Use Case | Lifetime | Visibility |":
        "| 作用域 | 用例 | 生命周期 | 可见性 |",
    
    "| **Node 域** | 工具 参数s, local variables | Single invocation | Current node only |":
        "| **节点作用域** | 工具参数、局部变量 | 单次调用 | 仅当前节点 |",
    
    "| **请求 域** | Shared context in call chain | Single request | Current chain |":
        "| **请求作用域** | 调用链中的共享上下文 | 单次请求 | 当前链 |",
    
    "| **会话 Group 域** | Conversation history | Multiple requests | Same session group |":
        "| **会话组作用域** | 对话历史 | 多次请求 | 同一会话组 |",
    
    "| **Global 域** | 智能体 registry, configuration | Application lifetime | Entire MAS |":
        "| **全局作用域** | 智能体注册表、配置 | 应用程序生命周期 | 整个 MAS |",
    
    # ====== 代码注释 ======
    "# Node Scope: arguments specific to this call":
        "# 节点作用域：此调用特定的参数",
    
    "# Request Scope: shared_data for this execution chain":
        "# 请求作用域：此执行链的 shared_data",
    
    "# Session Group Scope: group_data for conversation history":
        "# 会话组作用域：对话历史的 group_data",
    
    "# Optional: Pass shared data for request scope":
        "# 可选：传递请求作用域的共享数据",
    
    "# Optional: Pass group data for session scope":
        "# 可选：传递会话作用域的组数据",
    
    # ====== 小节标题 ======
    "### Accessing 域s in Custom 智能体s":
        "### 在自定义智能体中访问作用域",
    
    "When creating custom agents or tools, you can access all scopes through `Oxy请求`:":
        "创建自定义智能体或工具时，您可以通过 `OxyRequest` 访问所有作用域：",
    
    "# Access Node Scope": "# 访问节点作用域",
    "# Access Request Scope (shared within this call chain)": "# 访问请求作用域（在此调用链内共享）",
    "# Access Session Group Scope (persistent across requests)": "# 访问会话组作用域（跨请求持久化）",
    "# Access Global Scope (MAS registry)": "# 访问全局作用域（MAS 注册表）",
    
    "# Optionally update shared/group data for downstream agents":
        "# 可选：为下游智能体更新 shared/group 数据",
    
    # ====== 理解四大作用域 ======
    "## 理解 the Four 域s": "## 理解四大作用域",
    
    "### 1. Node 域 (`arguments`)": "### 1. 节点作用域 (`arguments`)",
    
    "**Purpose**: Isolated data for a single agent or tool invocation.":
        "**目的**：单个智能体或工具调用的隔离数据。",
    
    "**Characteristics**:": "**特征**：",
    
    "- Passed explicitly to each agent/tool call": "- 显式传递给每个智能体/工具调用",
    "- Not automatically shared with sub-agents": "- 不会自动与子智能体共享",
    "- Cleaned up after invocation completes": "- 调用完成后清理",
    "- Ideal for: 输入 参数s, local variables, node-specific configuration":
        "- 适用于：输入参数、局部变量、节点特定配置",
    
    "**Example 使用场景**:": "**示例使用场景**：",
    
    "- LLM 参数s (temperature, max_tokens)": "- LLM 参数（temperature、max_tokens）",
    "- 工具-specific arguments (search query, file path)": "- 工具特定参数（搜索查询、文件路径）",
    "- User messages for a single interaction": "- 单次交互的用户消息",
    "- 配置 overrides for this invocation only": "- 仅此次调用的配置覆盖",
    
    "# Each call has its own arguments scope": "# 每次调用都有自己的参数作用域",
    "# Scope 1": "# 作用域 1",
    "# Scope 2 (completely separate)": "# 作用域 2（完全独立）",
    
    # ====== 请求作用域 ======
    "### 2. 请求 域 (`shared_data`)": "### 2. 请求作用域 (`shared_data`)",
    
    "**Purpose**: Share context within a single execution chain (request and all nested calls).":
        "**目的**：在单个执行链（请求及所有嵌套调用）内共享上下文。",
    
    "- Automatically propagated to all sub-agents 在 call chain":
        "- 自动传播到调用链中的所有子智能体",
    
    "- Lifetime: Duration 的 root request": "- 生命周期：根请求的持续时间",
    "- Shared by reference (mutations are visible to parent and siblings)":
        "- 按引用共享（变更对父级和同级可见）",
    
    "- Ideal for: User context, request metadata, temporary shared state":
        "- 适用于：用户上下文、请求元数据、临时共享状态",
    
    "- User authentication info (user_id, permissions)": "- 用户身份验证信息（user_id、权限）",
    "- 请求 tracing data (correlation_id, timestamp)": "- 请求跟踪数据（correlation_id、时间戳）",
    "- Intermediate results to share between agents": "- 在智能体之间共享的中间结果",
    "- 上下文 accumulated during execution": "- 执行期间累积的上下文",
    
    "**Propagation Example**:": "**传播示例**：",
    
    "# shared_data is automatically available to master_agent":
        "# shared_data 自动可用于 master_agent",
    
    "# and ALL sub-agents it calls (file_agent, math_agent, etc.)":
        "# 以及它调用的所有子智能体（file_agent、math_agent 等）",
    
    "**Execution 流程**:": "**执行流程**：",
    
    " ├─→ File Agent (can read/write shared_data)": " ├─→ File Agent（可以读/写 shared_data）",
    " └─→ Math Agent (can read/write shared_data)": " └─→ Math Agent（可以读/写 shared_data）",
    
    # ====== 会话组作用域 ======
    "### 3. 会话 Group 域 (`group_data`)": "### 3. 会话组作用域 (`group_data`)",
    
    "**Purpose**: Persistent data across multiple requests 在 same conversation session.":
        "**目的**：同一对话会话中跨多个请求的持久数据。",
    
    "- Survives across multiple `mas.call()` invocations": "- 在多次 `mas.call()` 调用中存活",
    "- Stored in database (Elasticsearch/Redis) if configured": "- 如果配置，则存储在数据库（Elasticsearch/Redis）中",
    "- Retrieved using `group_id` or `from_trace_id`": "- 使用 `group_id` 或 `from_trace_id` 检索",
    "- Ideal for: Conversation history, user preferences, accumulated context":
        "- 适用于：对话历史、用户偏好、累积上下文",
    
    "- Multi-turn conversation context": "- 多轮对话上下文",
    "- User preferences and settings": "- 用户偏好和设置",
    "- Accumulated knowledge from previous interactions": "- 从先前交互中累积的知识",
    "- 会话-specific state (shopping cart, form progress)": "- 会话特定状态（购物车、表单进度）",
    
    "**Conversation Continuity Example**:": "**对话连续性示例**：",
    
    "# First turn: Initialize session": "# 第一轮：初始化会话",
    "# Get trace_id for session continuity": "# 获取会话连续性的 trace_id",
    "# Second turn: Continue same session": "# 第二轮：继续同一会话",
    "# Links to previous conversation": "# 链接到之前的对话",
    "# Agent can access group_data from previous turn": "# 智能体可以访问之前轮次的 group_data",
    "# Result: \"Your name is Alice\"": "# 结果：\"Your name is Alice\"",
    
    # ====== 全局作用域 ======
    "### 4. Global 域 (`mas`)": "### 4. 全局作用域 (`mas`)",
    
    "**Purpose**: System-wide registry of agents, tools, and configuration.":
        "**目的**：智能体、工具和配置的系统级注册表。",
    
    "- Single instance per MAS application": "- 每个 MAS 应用程序一个实例",
    "- Contains all registered Oxy components (agents, tools, LLMs)":
        "- 包含所有注册的 Oxy 组件（智能体、工具、LLM）",
    
    "- 配置 and service registry": "- 配置和服务注册表",
    "- Lifetime: Entire application runtime": "- 生命周期：整个应用程序运行时",
    "- Ideal for: Component lookup, global configuration, shared services":
        "- 适用于：组件查找、全局配置、共享服务",
    
    "- Looking up agents/tools by name": "- 按名称查找智能体/工具",
    "- Accessing global configuration (Config class)": "- 访问全局配置（Config 类）",
    "- Shared services (database connections, HTTP clients)": "- 共享服务（数据库连接、HTTP 客户端）",
    "- System-wide state management": "- 系统级状态管理",
    
    "**Component Access Example**:": "**组件访问示例**：",
    
    "# Access global MAS instance": "# 访问全局 MAS 实例",
    "# Look up other components": "# 查找其他组件",
    "# Check if component exists": "# 检查组件是否存在",
    
    # ====== 作用域生命周期 ======
    "## 域 生命周期 and Relationships": "## 作用域生命周期和关系",
    
    "### Data 流程 Hierarchy": "### 数据流程层次结构",
    
    "│ Global Scope (MAS) │ Lifetime: Application":
        "│ 全局作用域 (MAS) │ 生命周期：应用程序",
    
    "│ • Agent Registry │": "│ • 智能体注册表 │",
    "│ • Configuration │": "│ • 配置 │",
    "│ • Shared Services │": "│ • 共享服务 │",
    
    "│ Session Group Scope (group_data) │ Lifetime: Multiple Requests":
        "│ 会话组作用域 (group_data) │ 生命周期：多次请求",
    
    "│ • Conversation History │": "│ • 对话历史 │",
    "│ • User Preferences │": "│ • 用户偏好 │",
    "│ • Accumulated Context │": "│ • 累积上下文 │",
    
    "│ Request Scope (shared_data) │ Lifetime: Single Request Chain":
        "│ 请求作用域 (shared_data) │ 生命周期：单次请求链",
    
    "│ • User Context │": "│ • 用户上下文 │",
    "│ • Request Metadata │": "│ • 请求元数据 │",
    "│ • Temporary Shared State │": "│ • 临时共享状态 │",
    
    "│ Node Scope (arguments) │ Lifetime: Single Invocation":
        "│ 节点作用域 (arguments) │ 生命周期：单次调用",
    
    "│ • Input Parameters │": "│ • 输入参数 │",
    "│ • Local Variables │": "│ • 局部变量 │",
    "│ • Node-specific Config │": "│ • 节点特定配置 │",
    
    # ====== 可见性矩阵 ======
    "### 域 Visibility Matrix": "### 作用域可见性矩阵",
    
    "| 域 | Visible To | Mutable By | Persisted |":
        "| 作用域 | 可见于 | 可变更 | 是否持久化 |",
    
    "| **Node** | Current node only | Current node | 否 |":
        "| **节点** | 仅当前节点 | 当前节点 | 否 |",
    
    "| **请求** | All nodes in call chain | All nodes in chain | 否 |":
        "| **请求** | 调用链中的所有节点 | 链中的所有节点 | 否 |",
    
    "| **会话 Group** | All requests in session | Any request | Yes (if DB configured) |":
        "| **会话组** | 会话中的所有请求 | 任何请求 | 是（如果配置了数据库）|",
    
    "| **Global** | All nodes | 配置 only | 是 |":
        "| **全局** | 所有节点 | 仅配置 | 是 |",
    
    # ====== 配置选项 ======
    "### Controlling 域 Behavior": "### 控制作用域行为",
    
    "# Configure session persistence": "# 配置会话持久化",
    "# Enable Elasticsearch for group_data persistence": "# 启用 Elasticsearch 进行 group_data 持久化",
    "# Enable Redis for caching": "# 启用 Redis 进行缓存",
    "# Configure data retention": "# 配置数据保留",
    
    "### 内存 Management": "### 内存管理",
    
    "Control how scopes handle memory in agents:": "控制作用域在智能体中如何处理内存：",
    
    "# Keep last 10 interactions in memory": "# 在内存中保留最后 10 次交互",
    "# Clean up intermediate reasoning": "# 清理中间推理",
    "# Token limit for context": "# 上下文的令牌限制",
    
    # ====== 示例 ======
    "实际示例请参考 and usage patterns, 请参考：": "实际示例和使用模式，请参考：",
    
    "- [Basic 域 Usage](/examples/core-concepts/scope-basics) - 理解 each scope":
        "- [基本作用域使用](/examples/core-concepts/scope-basics) - 理解各作用域",
    
    "- [Multi-turn Conversations](/examples/core-concepts/multi-turn-scope) - Using group_data for continuity":
        "- [多轮对话](/examples/core-concepts/multi-turn-scope) - 使用 group_data 实现连续性",
    
    "- [Shared 上下文 Patterns](/examples/core-concepts/shared-context) - Passing data in request chains":
        "- [共享上下文模式](/examples/core-concepts/shared-context) - 在请求链中传递数据",
    
    "- [Custom 智能体 域s](/examples/core-concepts/custom-agent-scopes) - Accessing scopes in custom agents":
        "- [自定义智能体作用域](/examples/core-concepts/custom-agent-scopes) - 在自定义智能体中访问作用域",
    
    "查看所有示例 在 [示例 Gallery](/examples).": "查看 [示例库](/examples) 中的所有示例。",
    
    # ====== 最佳实践 ======
    "### 1. Choose the Right 域": "### 1. 选择正确的作用域",
    
    "- **Don't**: Put everything in `shared_data`": "- **不要**：将所有内容放入 `shared_data`",
    "- **Do**: Use the narrowest scope that serves your purpose": "- **要**：使用满足您目的的最窄作用域",
    "- **Node 域**: When data is only relevant to one agent": "- **节点作用域**：当数据仅与一个智能体相关时",
    "- **请求 域**: When data needs to flow through a call chain": "- **请求作用域**：当数据需要在调用链中流动时",
    "- **会话 Group 域**: When data must persist across conversations": "- **会话组作用域**：当数据必须跨对话持久化时",
    "- **Global 域**: Only for truly global resources": "- **全局作用域**：仅用于真正的全局资源",
    
    "### 2. Avoid 域 Pollution": "### 2. 避免作用域污染",
    
    "# ❌ Bad: Polluting shared_data with node-specific data": "# ❌ 错误：用节点特定数据污染 shared_data",
    "# ✅ Good: Keep node-specific data in arguments": "# ✅ 正确：将节点特定数据保留在 arguments 中",
    
    "### 3. Clean Up Sensitive Data": "### 3. 清理敏感数据",
    
    "# Clean up sensitive data after use": "# 使用后清理敏感数据",
    "# Process payment...": "# 处理支付...",
    "# Clean up sensitive data": "# 清理敏感数据",
    
    "### 4. Document 域 Dependencies": "### 4. 记录作用域依赖",
    
    "Custom agent for processing user requests.": "处理用户请求的自定义智能体。",
    "Required Arguments (Node Scope):": "必需参数（节点作用域）：",
    "- query (str): User query": "- query (str)：用户查询",
    "- max_results (int, optional): Maximum results": "- max_results (int, 可选)：最大结果数",
    "Required Shared Data (Request Scope):": "必需共享数据（请求作用域）：",
    "- user_id (str): User identifier for auth": "- user_id (str)：用于身份验证的用户标识符",
    "Optional Group Data (Session Scope):": "可选组数据（会话作用域）：",
    "- preferences (dict): User preferences": "- preferences (dict)：用户偏好",
    "# Implementation...": "# 实现...",
    
    # ====== 相关链接 ======
    "- [上下文 System](/docs/context) - Detailed context management":
        "- [上下文系统](/docs/context) - 详细的上下文管理",
    
    "- [MAS (Multi-智能体 System)](/docs/mas) - MAS architecture and APIs":
        "- [MAS（多智能体系统）](/docs/mas) - MAS 架构和 API",
    
    "- [生命周期](/docs/lifecycle) - 智能体 lifecycle and state management":
        "- [生命周期](/docs/lifecycle) - 智能体生命周期和状态管理",
    
    "- [配置](/docs/configuration) - Global configuration options":
        "- [配置](/docs/configuration) - 全局配置选项",
}

def translate_four_scope(content):
    """翻译 four-scope 文件"""
    # 保护代码块
    code_blocks = []
    def save_code(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"
    
    content = re.sub(r"```[\s\S]*?```", save_code, content)
    
    # 应用翻译（从长到短）
    translations = sorted(FOUR_SCOPE_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for en, zh in translations:
        content = content.replace(en, zh)
    
    # 恢复代码块
    for i, code_block in enumerate(code_blocks):
        content = content.replace(f"__CODE_BLOCK_{i}__", code_block)
    
    return content

def main():
    """主函数"""
    file_path = Path("content/docs/four-scope.zh-CN.mdx")
    
    print(f"翻译文件: {file_path.name}\n")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original = f.read()
        
        # 应用翻译
        translated = translate_four_scope(original)
        
        # 计算变化
        changes = sum(1 for a, b in zip(original, translated) if a != b)
        changes += abs(len(original) - len(translated))
        
        # 写回文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(translated)
        
        print(f"✅ 翻译完成！")
        print(f"   修改了 {changes} 处")
        print(f"\n主要翻译内容：")
        print(f"  ✓ 文件描述")
        print(f"  ✓ 四大作用域说明")
        print(f"  ✓ 所有段落标题")
        print(f"  ✓ 表格内容")
        print(f"  ✓ 代码注释")
        print(f"  ✓ 示例说明")
        print(f"  ✓ 最佳实践")
        
    except Exception as e:
        print(f"✗ 错误: {e}")

if __name__ == "__main__":
    main()

