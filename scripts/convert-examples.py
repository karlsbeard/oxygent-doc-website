#!/usr/bin/env python3
"""
Convert Python example files to MDX format
"""
import os
import re
from pathlib import Path

# Title mapping for better English titles
TITLE_MAP = {
    "00_环境安装": "Environment Setup",
    "01_hello_world": "Hello World",
    "02_配置参数": "Configuration Parameters",
    "03_RAG": "RAG Implementation",
    "04_MoA简单实现": "MoA Simple Implementation",
    "05_FunctionHub工具": "FunctionHub Tools",
    "06_LocalMCP工具": "Local MCP Tools",
    "07_SSEMCP工具": "SSE MCP Tools",
    "08_引用外部MCP工具": "External MCP Tools",
    "09_并发测试模式启动": "Concurrent Test Mode",
    "10_限制并发数量": "Limit Concurrency",
    "11_配置生产环境参数": "Production Configuration",
    "12_多环境配置": "Multi-Environment Configuration",
    "13_自动召回topK个工具": "Auto Recall Top-K Tools",
    "14_多智能体": "Multi-Agent System",
    "15_全局设置llm_model": "Global LLM Model Configuration",
    "16_多层级智能体": "Multi-Level Agents",
    "17_自定义解析函数": "Custom Parsing Function",
    "18_Workflow": "Workflow",
    "19_用户级query": "User-Level Query",
    "20_Reflexion": "Reflexion",
    "21_分布式": "Distributed System",
    "22_多模态": "Multimodal",
}

def extract_description(content: str) -> str:
    """Extract description from Python file comments"""
    lines = content.split('\n')
    descriptions = []

    # Look for comments at the start or in docstrings
    for line in lines[:20]:  # Check first 20 lines
        if line.strip().startswith('#') and '实现' in line:
            desc = line.strip('#').strip()
            descriptions.append(desc)
        elif '"""' in line or "'''" in line:
            desc = line.replace('"""', '').replace("'''", '').strip()
            if desc:
                descriptions.append(desc)

    return descriptions[0] if descriptions else ""

def convert_file(source_path: Path, target_dir: Path):
    """Convert a single Python file to MDX"""
    # Read source file
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract filename without extension
    filename_base = source_path.stem

    # Get title from map or create from filename
    title = TITLE_MAP.get(filename_base, filename_base.replace('_', ' ').title())

    # Extract description
    description = extract_description(content)
    if not description:
        description = f"Example demonstrating {title.lower()}"

    # Create MDX content
    mdx_content = f"""---
title: {title}
description: {description}
---

## Overview

This example demonstrates {title.lower()} in OxyGent.

## Code

```python
{content.strip()}
```

## Key Points

- This example shows how to use OxyGent for {title.lower()}
- Follow the code comments for detailed explanations
- Make sure to set up your environment variables before running

## Running the Example

To run this example:

```bash
python {source_path.name}
```
"""

    # Write MDX file
    target_file = target_dir / f"{filename_base}.mdx"
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(mdx_content)

    print(f"✓ Converted: {source_path.name} -> {target_file.name}")

def main():
    # Paths
    source_dir = Path("OxyGent/docs_building/docs_en/Examples")
    target_dir = Path("content/examples")

    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    # Convert all Python files
    py_files = sorted(source_dir.glob("*.py"))

    print(f"Converting {len(py_files)} Python files to MDX...\n")

    for py_file in py_files:
        if py_file.name == "__init__.py":
            continue
        convert_file(py_file, target_dir)

    print(f"\n✓ Conversion complete! {len(py_files)} files converted.")

if __name__ == "__main__":
    main()
