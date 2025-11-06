# OxyAPI 内容翻译策略与执行规划

## 📋 项目概述

**目标**: 将 `content/oxyapi/` 目录下的所有英文 API 文档翻译为中文，创建对应的 `.zh-CN.mdx` 文件

**文件数量**: 16 个 MDX 文件 + 1 个 meta.json

**执行者**: AI Coding 工具

## 📂 目录结构

```
content/oxyapi/
├── meta.json                          # 导航配置文件
├── index.mdx                          # API 参考主页
│
├── [Agents - 6 files]
│   ├── agents-react-api.mdx
│   ├── agents-chat-api.mdx
│   ├── agents-parallel-api.mdx
│   ├── agents-rag-api.mdx
│   ├── agents-sse-agent-api.mdx
│   └── agents-workflow-api.mdx
│
├── [Flows - 4 files]
│   ├── flows-workflow-api.mdx
│   ├── flows-parallel-api.mdx
│   ├── flows-plan-and-solve-api.mdx
│   └── flows-reflexion-api.mdx
│
├── [LLMs - 1 file]
│   └── llms-http-api.mdx
│
└── [Tools - 4 files]
    ├── tools-function-hub-api.mdx
    ├── tools-mcp-stdio-api.mdx
    ├── tools-mcp-sse-api.mdx
    └── tools-mcp-streamable-api.mdx
```

## 🎯 翻译策略

### 1. 文件命名规范

遵循项目已有的国际化约定：

- **英文原文**: `filename.mdx`
- **中文翻译**: `filename.zh-CN.mdx`

**示例**:

```
agents-react-api.mdx          → agents-react-api.zh-CN.mdx
flows-workflow-api.mdx        → flows-workflow-api.zh-CN.mdx
tools-function-hub-api.mdx    → tools-function-hub-api.zh-CN.mdx
```

### 2. 翻译原则

#### ✅ 需要翻译的内容

1. **Frontmatter 元数据**
   - `title`: 标题翻译为中文
   - `description`: 描述翻译为中文
   - `icon`: 保持不变

2. **Markdown 正文**
   - 所有标题（# ## ### 等）
   - 段落文本
   - 列表项说明文字
   - 表格中的描述列

3. **代码块说明**
   - 代码块前后的说明文字
   - 注释转为中文

#### ❌ 不翻译的内容

1. **技术术语**
   - API 名称: `ReActAgent`, `ChatAgent`, `HttpLLM`
   - 参数名: `name`, `is_master`, `llm_model`
   - 类型: `str`, `bool`, `int`, `list`
   - 代码示例中的所有 Python 代码

2. **专有名词**
   - ReAct, RAG, SSE, MCP
   - GitHub, HTTP, JSON

3. **链接路径**
   - URL 路径保持不变
   - 内部链接路径保持不变

### 3. 翻译质量要求

#### 术语一致性

建立术语词汇表，确保翻译一致：

| English | 中文 | 说明 |
|---------|------|------|
| Agent | 代理/智能体 | 根据上下文选择 |
| Constructor | 构造函数 | - |
| Parameter | 参数 | - |
| Method | 方法 | - |
| Flow | 流程 | - |
| Tool | 工具 | - |
| Memory | 记忆/内存 | 根据上下文 |
| Reasoning | 推理 | - |
| Multi-Agent System | 多智能体系统 | - |
| Default | 默认值 | - |
| Required | 必需 | - |
| Optional | 可选 | - |

#### 专业性

- 使用准确的技术术语
- 保持 API 文档的专业性和准确性
- 参数说明要清晰明确

#### 可读性

- 句子流畅自然
- 避免生硬直译
- 适当调整语序以符合中文习惯

## 📝 翻译模板

### Frontmatter 翻译示例

**英文原文**:

```yaml
---
title: ReActAgent API Reference
description: Complete API reference for ReActAgent constructor parameters and methods
icon: Code
---
```

**中文翻译**:

```yaml
---
title: ReActAgent API 参考
description: ReActAgent 构造函数参数和方法的完整 API 参考文档
icon: Code
---
```

### 标题翻译示例

```markdown
# 英文 → 中文

## Constructor Parameters → ## 构造函数参数
## Core Parameters → ## 核心参数
## Parameter Details → ## 参数详情
## Methods → ## 方法
## Usage Guidelines → ## 使用指南
## Related Documentation → ## 相关文档
```

### 表格翻译示例

**英文**:

```markdown
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | str | Required | Unique identifier for the agent |
```

**中文**:

```markdown
| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `name` | str | 必需 | 代理的唯一标识符 |
```

## 🛠️ 执行方案

### 方案 A: 手动创建脚本（推荐）

创建专门的翻译脚本 `scripts/translate_oxyapi.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OxyAPI 文档翻译脚本
将 content/oxyapi/*.mdx 翻译为对应的 .zh-CN.mdx 文件
"""

import os
import re
from pathlib import Path

# 翻译映射表
TRANSLATIONS = {
    # Frontmatter
    "API Reference": "API 参考",
    "Complete API reference for": "完整的 API 参考文档：",
    "Complete API documentation for": "完整的 API 文档：",

    # 标题
    "Constructor Parameters": "构造函数参数",
    "Core Parameters": "核心参数",
    "Execution Parameters": "执行参数",
    "Memory Parameters": "内存参数",
    "Parameter Details": "参数详情",
    "Methods": "方法",
    "Usage Guidelines": "使用指南",
    "Related Documentation": "相关文档",
    "Quick Start": "快速开始",
    "API Conventions": "API 约定",
    "Getting Help": "获取帮助",

    # 常用短语
    "Agents": "代理",
    "Flows": "流程",
    "Tools": "工具",
    "LLMs": "大语言模型",
    "Overview": "概述",

    # 表格标题
    "Parameter": "参数",
    "Type": "类型",
    "Default": "默认值",
    "Description": "描述",
    "Required": "必需",

    # 其他
    "If you encounter issues": "如果您在使用过程中遇到问题",
    "you can": "您可以",
}

def translate_content(content, filename):
    """翻译文件内容"""
    # 1. 翻译 frontmatter
    # 2. 翻译标题
    # 3. 翻译表格
    # 4. 翻译段落
    # 保持代码块不变

    return translated_content

def main():
    source_dir = Path("content/oxyapi")

    # 获取所有 .mdx 文件（排除 .zh-CN.mdx）
    mdx_files = [f for f in source_dir.glob("*.mdx")
                 if not f.name.endswith(".zh-CN.mdx")]

    print(f"找到 {len(mdx_files)} 个待翻译文件\n")

    for mdx_file in mdx_files:
        output_file = mdx_file.parent / f"{mdx_file.stem}.zh-CN.mdx"

        print(f"翻译: {mdx_file.name} → {output_file.name}")

        with open(mdx_file, 'r', encoding='utf-8') as f:
            content = f.read()

        translated = translate_content(content, mdx_file.name)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translated)

    print(f"\n✅ 翻译完成！共处理 {len(mdx_files)} 个文件")

if __name__ == "__main__":
    main()
```

**使用方法**:

```bash
python scripts/translate_oxyapi.py
```

### 方案 B: 使用 AI 批量翻译

**步骤**:

1. 读取英文 MDX 文件
2. 提取需要翻译的部分
3. 调用 AI 翻译 API（如 OpenAI/Claude）
4. 替换翻译内容
5. 生成 .zh-CN.mdx 文件

### 方案 C: 逐文件手动处理

AI Coding 工具逐个文件处理：

1. 读取 `agents-react-api.mdx`
2. 翻译内容
3. 创建 `agents-react-api.zh-CN.mdx`
4. 重复以上步骤处理所有文件

## 📊 执行清单

### Phase 1: 配置文件

- [ ] 创建 `meta.zh-CN.json`
  - 翻译导航标题
  - 保持页面引用路径不变

### Phase 2: 主页

- [ ] 翻译 `index.mdx` → `index.zh-CN.mdx`

### Phase 3: Agents 部分 (6 个文件)

- [ ] `agents-react-api.mdx` → `agents-react-api.zh-CN.mdx`
- [ ] `agents-chat-api.mdx` → `agents-chat-api.zh-CN.mdx`
- [ ] `agents-parallel-api.mdx` → `agents-parallel-api.zh-CN.mdx`
- [ ] `agents-rag-api.mdx` → `agents-rag-api.zh-CN.mdx`
- [ ] `agents-sse-agent-api.mdx` → `agents-sse-agent-api.zh-CN.mdx`
- [ ] `agents-workflow-api.mdx` → `agents-workflow-api.zh-CN.mdx`

### Phase 4: Flows 部分 (4 个文件)

- [ ] `flows-workflow-api.mdx` → `flows-workflow-api.zh-CN.mdx`
- [ ] `flows-parallel-api.mdx` → `flows-parallel-api.zh-CN.mdx`
- [ ] `flows-plan-and-solve-api.mdx` → `flows-plan-and-solve-api.zh-CN.mdx`
- [ ] `flows-reflexion-api.mdx` → `flows-reflexion-api.zh-CN.mdx`

### Phase 5: LLMs 部分 (1 个文件)

- [ ] `llms-http-api.mdx` → `llms-http-api.zh-CN.mdx`

### Phase 6: Tools 部分 (4 个文件)

- [ ] `tools-function-hub-api.mdx` → `tools-function-hub-api.zh-CN.mdx`
- [ ] `tools-mcp-stdio-api.mdx` → `tools-mcp-stdio-api.zh-CN.mdx`
- [ ] `tools-mcp-sse-api.mdx` → `tools-mcp-sse-api.zh-CN.mdx`
- [ ] `tools-mcp-streamable-api.mdx` → `tools-mcp-streamable-api.zh-CN.mdx`

### Phase 7: 质量检查

- [ ] 验证所有文件已创建
- [ ] 检查翻译质量和一致性
- [ ] 确保链接路径正确
- [ ] 测试中英文切换功能

## 🔍 质量检查脚本

创建 `scripts/validate_oxyapi_translation.py`:

```python
#!/usr/bin/env python3
"""验证 OxyAPI 翻译完整性"""

from pathlib import Path

def validate():
    oxyapi_dir = Path("content/oxyapi")

    # 获取所有英文文件
    en_files = [f for f in oxyapi_dir.glob("*.mdx")
                if not f.name.endswith(".zh-CN.mdx")]

    missing = []
    for en_file in en_files:
        zh_file = en_file.parent / f"{en_file.stem}.zh-CN.mdx"
        if not zh_file.exists():
            missing.append(en_file.name)

    if missing:
        print("❌ 缺少以下中文翻译:")
        for f in missing:
            print(f"  - {f}")
        return False
    else:
        print(f"✅ 所有 {len(en_files)} 个文件已翻译完成")
        return True

if __name__ == "__main__":
    validate()
```

## 📌 注意事项

1. **备份**: 翻译前备份原始文件
2. **编码**: 使用 UTF-8 编码
3. **格式**: 保持 Markdown 格式完整性
4. **链接**: 验证内部链接在中文版本中仍然有效
5. **代码块**: 代码示例保持原样，只翻译注释
6. **术语**: 参考已有的 `content/examples/*.zh-CN.mdx` 中的术语翻译

## 🚀 执行命令

```bash
# 1. 创建翻译脚本
# 编辑 scripts/translate_oxyapi.py

# 2. 执行翻译
python scripts/translate_oxyapi.py

# 3. 验证完整性
python scripts/validate_oxyapi_translation.py

# 4. 测试构建
pnpm build

# 5. 本地预览
pnpm dev
```

## 📖 参考资料

- **现有翻译示例**: `content/examples/*.zh-CN.mdx`
- **翻译脚本参考**: `scripts/translate_script.py`
- **项目 README**: `scripts/README.md`
- **国际化配置**: `lib/i18n.ts`

## ✅ 完成标准

- [ ] 所有 16 个 MDX 文件都有对应的 `.zh-CN.mdx`
- [ ] `meta.zh-CN.json` 已创建
- [ ] 翻译质量通过验证
- [ ] 中英文切换功能正常
- [ ] 本地构建成功
- [ ] 无遗留英文内容在中文版本中

---

**文档版本**: v1.0
**创建日期**: 2025-11-05
**适用项目**: oxygent-doc-website
**执行者**: AI Coding 工具
