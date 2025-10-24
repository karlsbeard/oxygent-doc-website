#!/usr/bin/env python3
"""
Rename Chinese example files to English and create zh-CN copies
"""
import os
import shutil
from pathlib import Path

# Mapping from Chinese names to English names
RENAME_MAP = {
    "00_环境安装": "00_environment-setup",
    "01_hello_world": "01_hello-world",
    "02_配置参数": "02_configuration",
    "03_RAG": "03_rag",
    "04_MoA简单实现": "04_moa-implementation",
    "05_FunctionHub工具": "05_functionhub-tools",
    "06_LocalMCP工具": "06_local-mcp-tools",
    "07_SSEMCP工具": "07_sse-mcp-tools",
    "08_引用外部MCP工具": "08_external-mcp-tools",
    "09_并发测试模式启动": "09_concurrent-testing",
    "10_限制并发数量": "10_concurrency-limits",
    "11_配置生产环境参数": "11_production-config",
    "12_多环境配置": "12_multi-environment-config",
    "13_自动召回topK个工具": "13_auto-recall-tools",
    "14_多智能体": "14_multi-agent",
    "15_全局设置llm_model": "15_global-llm-config",
    "16_多层级智能体": "16_multi-level-agents",
    "17_自定义解析函数": "17_custom-parsing",
    "18_Workflow": "18_workflow",
    "19_用户级query": "19_user-level-query",
    "20_Reflexion": "20_reflexion",
    "21_分布式": "21_distributed",
    "22_多模态": "22_multimodal",
}

def rename_and_duplicate():
    examples_dir = Path("content/examples")

    print("Starting rename and duplication process...\n")

    # Process each file
    for old_name, new_name in RENAME_MAP.items():
        old_file = examples_dir / f"{old_name}.mdx"
        new_file = examples_dir / f"{new_name}.mdx"
        new_file_cn = examples_dir / f"{new_name}.zh-CN.mdx"

        if not old_file.exists():
            print(f"⚠️  File not found: {old_file}")
            continue

        # Read original content
        with open(old_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Create English version
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created: {new_file.name}")

        # Create Chinese version
        with open(new_file_cn, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created: {new_file_cn.name}")

        # Remove old file
        old_file.unlink()
        print(f"✓ Removed: {old_file.name}\n")

    print("✅ All files renamed and duplicated successfully!")

if __name__ == "__main__":
    rename_and_duplicate()
