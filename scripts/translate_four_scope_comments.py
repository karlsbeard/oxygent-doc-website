#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译 four-scope.zh-CN.mdx 文件中的代码注释
"""

import re
from pathlib import Path

# 代码注释翻译
CODE_COMMENT_TRANSLATIONS = {
    # 第一个示例
    "# Node Scope: arguments specific to this call": "# 节点作用域：此调用特定的参数",
    "# Request Scope: shared_data for this execution chain": "# 请求作用域：此执行链的 shared_data",
    "# Session Group Scope: group_data for conversation history": "# 会话组作用域：对话历史的 group_data",
    "# Optional: Pass shared data for request scope": "# 可选：传递请求作用域的共享数据",
    "# Optional: Pass group data for session scope": "# 可选：传递会话作用域的组数据",
    
    # 第二个示例
    "# Access Node Scope": "# 访问节点作用域",
    "# Access Request Scope (shared within this call chain)": "# 访问请求作用域（在此调用链内共享）",
    "# Access Session Group Scope (persistent across requests)": "# 访问会话组作用域（跨请求持久化）",
    "# Access Global Scope (MAS registry)": "# 访问全局作用域（MAS 注册表）",
    "# Your agent logic here": "# 您的智能体逻辑在这里",
    "# Optionally update shared/group data for downstream agents": "# 可选：为下游智能体更新 shared/group 数据",
    
    # arguments 示例
    "# Each call has its own arguments scope": "# 每次调用都有自己的参数作用域",
    "# Scope 1": "# 作用域 1",
    "# Scope 2 (completely separate)": "# 作用域 2（完全独立）",
    
    # shared_data 示例
    "# shared_data is automatically available to master_agent": "# shared_data 自动可用于 master_agent",
    "# and ALL sub-agents it calls (file_agent, math_agent, etc.)": "# 以及它调用的所有子智能体（file_agent、math_agent 等）",
    
    # group_data 示例
    "# First turn: Initialize session": "# 第一轮：初始化会话",
    "# Get trace_id for session continuity": "# 获取会话连续性的 trace_id",
    "# Second turn: Continue same session": "# 第二轮：继续同一会话",
    "# Links to previous conversation": "# 链接到之前的对话",
    "# Agent can access group_data from previous turn": "# 智能体可以访问之前轮次的 group_data",
    "# Result: \"Your name is Alice\"": "# 结果：\"Your name is Alice\"",
    
    # Global 示例
    "# Access global MAS instance": "# 访问全局 MAS 实例",
    "# Look up other components": "# 查找其他组件",
    "# Check if component exists": "# 检查组件是否存在",
    
    # 配置示例
    "# Configure session persistence": "# 配置会话持久化",
    "# Enable Elasticsearch for group_data persistence": "# 启用 Elasticsearch 进行 group_data 持久化",
    "# Enable Redis for caching": "# 启用 Redis 进行缓存",
    "# Configure data retention": "# 配置数据保留",
    
    # 内存管理示例
    "# Keep last 10 interactions in memory": "# 在内存中保留最后 10 次交互",
    "# Clean up intermediate reasoning": "# 清理中间推理",
    "# Token limit for context": "# 上下文的令牌限制",
    
    # 最佳实践示例
    "# ❌ Bad: Polluting shared_data with node-specific data": "# ❌ 错误：用节点特定数据污染 shared_data",
    "# ✅ Good: Keep node-specific data in arguments": "# ✅ 正确：将节点特定数据保留在 arguments 中",
    
    # 清理敏感数据示例
    "# Clean up sensitive data after use": "# 使用后清理敏感数据",
    "# Process payment...": "# 处理支付...",
    "# Clean up sensitive data": "# 清理敏感数据",
    
    # 文档示例
    "# Implementation...": "# 实现...",
}

def translate_comments(content):
    """翻译代码注释"""
    # 按长度排序，避免部分替换
    translations = sorted(CODE_COMMENT_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for en, zh in translations:
        content = content.replace(en, zh)
    
    return content

def main():
    """主函数"""
    file_path = Path("content/docs/four-scope.zh-CN.mdx")
    
    print(f"翻译代码注释: {file_path.name}\n")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original = f.read()
        
        # 应用翻译
        translated = translate_comments(original)
        
        # 计算变化
        changes = sum(1 for a, b in zip(original, translated) if a != b)
        changes += abs(len(original) - len(translated))
        
        if changes > 0:
            # 写回文件
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(translated)
            
            print(f"✅ 代码注释翻译完成！")
            print(f"   修改了 {changes} 处")
        else:
            print(f"✓ 所有代码注释已经是中文")
        
    except Exception as e:
        print(f"✗ 错误: {e}")

if __name__ == "__main__":
    main()

