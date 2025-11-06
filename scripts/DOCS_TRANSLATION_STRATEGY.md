# OxyGent Docs Translation Strategy

## 📋 Project Overview

**Objective**: Translate all English documentation in `content/docs/` to Chinese, creating corresponding `.zh-CN.mdx` files and completing `meta.zh-CN.json`

**Scope**:
- 27 MDX documentation files
- 1 meta.json configuration update

**Executor**: AI Coding Tool (Automated)

**Reference Success**:
- ✅ `content/oxyapi/` - 16 files translated
- ✅ `content/examples/` - 22 files translated
- ✅ Proven scripts and workflow

---

## 🔍 Current Status

### File Structure

```
content/docs/
├── meta.json                          ✅ Complete English version
├── meta.zh-CN.json                    ⚠️ Only 5 pages defined (incomplete)
│
├── [27 English .mdx files]            ❌ No Chinese translations
└── [0 Chinese .zh-CN.mdx files]       ❌ To be created
```

### File Categories

| Category | Count | Files |
|----------|-------|-------|
| **Getting Started** | 2 | index.mdx, quick-start.mdx |
| **Core Concepts** | 6 | mas, visualization, four-scope, lifecycle, configuration, context |
| **Agents** | 6 | chat, react, workflow, parallel, rag, sse-agent |
| **Flows** | 5 | workflow, parallel, plan-and-solve, reflexion, comparison |
| **LLMs** | 2 | http, openai |
| **Tools** | 5 | function-hub, mcp-stdio, mcp-sse, mcp-streamable, mcp-comparison |

**Total**: 27 documentation pages + 1 navigation config = **28 tasks**

---

## 🎯 Translation Principles

### ✅ What to Translate

1. **Frontmatter Metadata**
   - `title`: Translate to Chinese
   - `description`: Translate to Chinese
   - `icon`: Keep unchanged

2. **Markdown Content**
   - All headings (# ## ### etc.)
   - Paragraph text
   - List item descriptions
   - Table description columns
   - Admonition content (Note, Warning, Tip, etc.)

3. **Code Explanations**
   - Text before/after code blocks
   - Convert code comments to Chinese

### ❌ What NOT to Translate

1. **Technical Terms**
   - Class names: `MAS`, `ChatAgent`, `ReActAgent`
   - Method names: `start_web_service()`, `run()`
   - Parameter names: `name`, `llm_model`, `prompt`
   - Types: `str`, `bool`, `int`, `list`
   - Python code itself in examples

2. **Proper Nouns**
   - OxyGent, ReAct, RAG, SSE, MCP
   - GAIA, OpenAI, HTTP
   - GitHub, JSON, YAML

3. **Link Paths**
   - URL paths unchanged
   - Internal link paths unchanged (e.g., `/docs/agents-chat`)

---

## 📖 Standard Terminology

Use consistent translations across all documents:

| English | Chinese | Context |
|---------|---------|---------|
| Agent | 智能体 | Primary usage |
| Multi-Agent System | 多智能体系统 | MAS related |
| Flow | 流程 | Flows section |
| Tool | 工具 | Tools section |
| LLM | 大语言模型 | First mention (full form) |
| LLM | LLM | Subsequent usage (abbreviation) |
| Constructor | 构造函数 | Technical docs |
| Parameter | 参数 | - |
| Method | 方法 | - |
| Configuration | 配置 | - |
| Memory | 记忆/内存 | Context-dependent |
| Reasoning | 推理 | - |
| Lifecycle | 生命周期 | - |
| Context | 上下文 | - |
| Workflow | 工作流 | - |
| Parallel | 并行 | - |
| Visualization | 可视化 | - |
| Default | 默认值 | - |
| Required | 必需 | - |
| Optional | 可选 | - |
| Overview | 概述 | Section heading |
| Quick Start | 快速开始 | - |
| Getting Started | 入门指南 | - |
| Core Concepts | 核心概念 | - |
| Best Practices | 最佳实践 | - |
| Example | 示例 | - |

---

## 📝 Translation Templates

### Frontmatter Translation

**English**:
```yaml
---
title: Multi-Agent System
description: Understanding the core architecture of OxyGent's multi-agent system
icon: Network
---
```

**Chinese**:
```yaml
---
title: 多智能体系统
description: 了解 OxyGent 多智能体系统的核心架构
icon: Network
---
```

### Heading Translation

```markdown
English → Chinese

## Getting Started → ## 入门指南
## Core Concepts → ## 核心概念
## Installation → ## 安装
## Configuration → ## 配置
## Best Practices → ## 最佳实践
## API Reference → ## API 参考
## Usage Examples → ## 使用示例
## Advanced Topics → ## 高级主题
```

---

## 📂 Complete File Checklist

### Phase 1: Configuration (1 file)

- [ ] **meta.zh-CN.json** - Complete with all 27 pages

### Phase 2: Getting Started (2 files)

- [ ] `index.mdx` → `index.zh-CN.mdx`
- [ ] `quick-start.mdx` → `quick-start.zh-CN.mdx`

### Phase 3: Core Concepts (6 files)

- [ ] `mas.mdx` → `mas.zh-CN.mdx`
- [ ] `visualization.mdx` → `visualization.zh-CN.mdx`
- [ ] `four-scope.mdx` → `four-scope.zh-CN.mdx`
- [ ] `lifecycle.mdx` → `lifecycle.zh-CN.mdx`
- [ ] `configuration.mdx` → `configuration.zh-CN.mdx`
- [ ] `context.mdx` → `context.zh-CN.mdx`

### Phase 4: Agents (6 files)

- [ ] `agents-chat.mdx` → `agents-chat.zh-CN.mdx`
- [ ] `agents-react.mdx` → `agents-react.zh-CN.mdx`
- [ ] `agents-workflow.mdx` → `agents-workflow.zh-CN.mdx`
- [ ] `agents-parallel.mdx` → `agents-parallel.zh-CN.mdx`
- [ ] `agents-rag.mdx` → `agents-rag.zh-CN.mdx`
- [ ] `agents-sse-agent.mdx` → `agents-sse-agent.zh-CN.mdx`

### Phase 5: Flows (5 files)

- [ ] `flows-workflow.mdx` → `flows-workflow.zh-CN.mdx`
- [ ] `flows-parallel.mdx` → `flows-parallel.zh-CN.mdx`
- [ ] `flows-plan-and-solve.mdx` → `flows-plan-and-solve.zh-CN.mdx`
- [ ] `flows-reflexion.mdx` → `flows-reflexion.zh-CN.mdx`
- [ ] `flows-comparison.mdx` → `flows-comparison.zh-CN.mdx`

### Phase 6: LLMs (2 files)

- [ ] `llms-http.mdx` → `llms-http.zh-CN.mdx`
- [ ] `llms-openai.mdx` → `llms-openai.zh-CN.mdx`

### Phase 7: Tools (5 files)

- [ ] `tools-function-hub.mdx` → `tools-function-hub.zh-CN.mdx`
- [ ] `tools-mcp-stdio.mdx` → `tools-mcp-stdio.zh-CN.mdx`
- [ ] `tools-mcp-sse.mdx` → `tools-mcp-sse.zh-CN.mdx`
- [ ] `tools-mcp-streamable.mdx` → `tools-mcp-streamable.zh-CN.mdx`
- [ ] `tools-mcp-comparison.mdx` → `tools-mcp-comparison.zh-CN.mdx`

---

## 📋 meta.zh-CN.json Update Plan

### Current (Incomplete)

```json
{
  "pages": [
    "index",
    "---入门指南---",
    "quick-start",
    "installation",
    "common-strategies",
    "---核心功能---",
    "agents"
  ]
}
```

### Target (Complete)

```json
{
  "title": "文档",
  "pages": [
    "index",
    "---入门指南---",
    "quick-start",
    "---核心概念---",
    "mas",
    "visualization",
    "four-scope",
    "lifecycle",
    "configuration",
    "context",
    "---智能体---",
    "agents-chat",
    "agents-react",
    "agents-workflow",
    "agents-parallel",
    "agents-rag",
    "agents-sse-agent",
    "---流程---",
    "flows-workflow",
    "flows-parallel",
    "flows-plan-and-solve",
    "flows-reflexion",
    "flows-comparison",
    "---大语言模型---",
    "llms-http",
    "llms-openai",
    "---工具---",
    "tools-function-hub",
    "tools-mcp-stdio",
    "tools-mcp-sse",
    "tools-mcp-streamable",
    "tools-mcp-comparison"
  ]
}
```

**Changes**:
- Add `"title": "文档"` field
- Remove non-existent `installation` and `common-strategies`
- Add all 27 pages
- Translate section headers:
  - `Getting Started` → `入门指南`
  - `Core Concepts` → `核心概念`
  - `Agents` → `智能体`
  - `Flows` → `流程`
  - `LLMs` → `大语言模型`
  - `Tools` → `工具`

---

## 🚀 AI Coding Execution Plan (Optimized)

### Automated Execution Workflow

#### **Step 1: Update meta.zh-CN.json** ⚡ (AI Auto)
**Time**: 5 minutes
**Action**: Replace current content with complete version
```bash
# AI Coding will:
# 1. Read content/docs/meta.zh-CN.json
# 2. Replace with complete version from strategy
# 3. Verify JSON format is valid
```

#### **Step 2: Batch Create Translation Script** ⚡ (AI Auto)
**Time**: 10 minutes
**Action**: Create `scripts/translate_docs.py` based on proven patterns
```bash
# AI Coding will:
# 1. Create translate_docs.py using translate_oxyapi.py as template
# 2. Adapt translation mappings for docs content
# 3. Include all 27 files in processing list
```

#### **Step 3: Generate All Chinese Files** ⚡ (AI Auto)
**Time**: 15 minutes
**Action**: Execute script to create all 27 .zh-CN.mdx files
```bash
# AI Coding will:
# 1. Run: python scripts/translate_docs.py
# 2. Generate all 27 .zh-CN.mdx files
# 3. Report completion status
```

#### **Step 4: AI Quality Enhancement** ⚡ (AI Auto)
**Time**: 30-45 minutes
**Action**: AI Coding reviews and enhances each file
```bash
# AI Coding will:
# 1. Review each generated .zh-CN.mdx file
# 2. Enhance translation quality:
#    - Improve sentence fluency
#    - Ensure terminology consistency
#    - Fix formatting issues
# 3. Mark files as reviewed
```

#### **Step 5: Automated Validation** ⚡ (AI Auto)
**Time**: 5 minutes
**Action**: Run validation scripts
```bash
# AI Coding will:
# 1. Create and run validate_docs_translation.py
# 2. Check all 27 files exist
# 3. Verify meta.zh-CN.json completeness
# 4. Report any issues found
```

#### **Step 6: Human Testing** 👤 (Manual)
**Time**: 10-15 minutes
**Action**: Human verifies functionality
```bash
# Human will:
# 1. Run: pnpm build
# 2. Run: pnpm dev
# 3. Test language switching
# 4. Spot-check translation quality
```

### Total Time Estimate
- **AI Automated**: 1-1.5 hours
- **Human Verification**: 15 minutes
- **Total**: ~1.5-2 hours

---

## 🛠️ Translation Script Template

### scripts/translate_docs.py (Auto-generated by AI)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translate content/docs/*.mdx to Chinese .zh-CN.mdx files
Auto-generated by AI Coding based on proven oxyapi translation script
"""

import re
from pathlib import Path

# Translation mappings from strategy
TRANSLATIONS = {
    # Frontmatter
    "Welcome to OxyGent": "欢迎使用 OxyGent",
    "Quick Start": "快速开始",
    "Multi-Agent System": "多智能体系统",
    "Visualization": "可视化",
    "Configuration": "配置",
    "Context": "上下文",
    # ... more mappings

    # Headings
    "## Getting Started": "## 入门指南",
    "## Core Concepts": "## 核心概念",
    "## Overview": "## 概述",
    # ... more headings

    # Common phrases
    "This document describes": "本文档介绍",
    # ... more phrases
}

# Standard terminology
TERMINOLOGY = {
    "Agent": "智能体",
    "Multi-Agent System": "多智能体系统",
    "Flow": "流程",
    "Tool": "工具",
    # ... from terminology table
}

def translate_file(source_file, target_file):
    """Translate a single MDX file"""
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Translate frontmatter
    # 2. Translate headings
    # 3. Translate paragraphs
    # 4. Keep code blocks unchanged
    # 5. Apply terminology consistently

    translated = content  # Apply translations

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(translated)

    print(f"✓ Translated: {source_file.name} → {target_file.name}")

def main():
    docs_dir = Path("content/docs")

    # Get all .mdx files (exclude .zh-CN.mdx)
    mdx_files = [f for f in docs_dir.glob("*.mdx")
                 if not f.name.endswith(".zh-CN.mdx")]

    print(f"Found {len(mdx_files)} files to translate\n")

    for mdx_file in mdx_files:
        output_file = mdx_file.parent / f"{mdx_file.stem}.zh-CN.mdx"
        translate_file(mdx_file, output_file)

    print(f"\n✅ Translation complete! Processed {len(mdx_files)} files")

if __name__ == "__main__":
    main()
```

---

## 🔍 Validation Script Template

### scripts/validate_docs_translation.py (Auto-generated by AI)

```python
#!/usr/bin/env python3
"""Validate Docs translation completeness"""

from pathlib import Path
import json

def validate():
    docs_dir = Path("content/docs")

    # 1. Check all .mdx files have .zh-CN.mdx counterparts
    en_files = [f for f in docs_dir.glob("*.mdx")
                if not f.name.endswith(".zh-CN.mdx")]

    missing = []
    for en_file in en_files:
        zh_file = en_file.parent / f"{en_file.stem}.zh-CN.mdx"
        if not zh_file.exists():
            missing.append(en_file.name)

    if missing:
        print(f"❌ Missing {len(missing)} Chinese translations:")
        for f in missing:
            print(f"  - {f}")
        return False
    else:
        print(f"✅ All {len(en_files)} files translated")

    # 2. Validate meta.zh-CN.json
    meta_zh = docs_dir / "meta.zh-CN.json"
    with open(meta_zh, 'r', encoding='utf-8') as f:
        meta_data = json.load(f)

    if len(meta_data.get('pages', [])) < 27:
        print(f"⚠️ meta.zh-CN.json incomplete: {len(meta_data['pages'])} pages")
        return False

    print("✅ meta.zh-CN.json complete")
    return True

if __name__ == "__main__":
    success = validate()
    exit(0 if success else 1)
```

---

## 📖 Reference Resources

### Existing Translations
- `content/oxyapi/*.zh-CN.mdx` - API docs translation reference
- `content/examples/*.zh-CN.mdx` - Example docs translation reference

### Translation Scripts
- `scripts/translate_oxyapi.py` - OxyAPI translation script (template)
- `scripts/validate_oxyapi_translation.py` - Validation script (template)

### Strategy Documents
- `scripts/OXYAPI_TRANSLATION_STRATEGY.md` - OxyAPI strategy
- `scripts/TRANSLATION_SUMMARY.md` - Translation summary

### Project Config
- `lib/i18n.ts` - i18n configuration
- `content/docs/meta.json` - English navigation config

---

## ✅ Success Criteria

### Must Achieve
- [ ] 27 .zh-CN.mdx files created
- [ ] meta.zh-CN.json complete with all 27 pages
- [ ] All frontmatter correctly translated
- [ ] Code blocks remain in English
- [ ] Local build succeeds (`pnpm build`)
- [ ] Language switching works

### Quality Standards
- [ ] Terminology consistent (per terminology table)
- [ ] Sentences natural and fluent
- [ ] No grammar errors
- [ ] Technical accuracy maintained
- [ ] Format integrity preserved

### Validation Standards
- [ ] Automated validation script passes
- [ ] No leftover English (except proper nouns)
- [ ] All internal links valid
- [ ] Style consistent with existing translations

---

## 📌 Important Notes

### Key Principles
1. **Don't modify** original English files
2. **Don't translate** Python code in examples
3. **Keep** all link paths unchanged
4. **Ensure** UTF-8 encoding
5. **Preserve** Markdown formatting

### AI Coding Instructions

When executing this strategy, AI Coding should:

1. **Work sequentially** through steps 1-5
2. **Report progress** after each phase
3. **Auto-fix** issues when possible
4. **Flag** issues that need human review
5. **Provide summary** when complete

### Error Handling

If errors occur:
- Reference `content/oxyapi/*.zh-CN.mdx` for patterns
- Check terminology table for consistency
- Run validation scripts
- Report specific error to human for review

---

## 🎯 Success Metrics

### Quantitative
- Translation completion: **100%** (27/27)
- Terminology consistency: **>95%**
- Build success rate: **100%**
- Link validity: **100%**

### Qualitative
- Natural and fluent translation
- Technically accurate
- Good user experience
- Consistent style

---

## 🤖 AI Coding Execution Command

To execute this strategy, AI Coding should follow this sequence:

```bash
# Phase 1: Update Configuration
1. Update content/docs/meta.zh-CN.json with complete version

# Phase 2: Create Translation Infrastructure
2. Create scripts/translate_docs.py
3. Create scripts/validate_docs_translation.py

# Phase 3: Execute Translation
4. Run translation script: python scripts/translate_docs.py

# Phase 4: Quality Enhancement
5. Review and enhance each .zh-CN.mdx file
6. Ensure terminology consistency
7. Improve sentence fluency

# Phase 5: Validation
8. Run validation: python scripts/validate_docs_translation.py
9. Generate completion report

# Phase 6: Human Handoff
10. Report completion status
11. List any issues requiring human review
12. Provide testing instructions
```

---

**Document Version**: v2.0 (English, AI-Optimized)
**Created**: 2025-11-06
**Project**: oxygent-doc-website
**Target**: content/docs/
**Executor**: AI Coding Tool (Automated)

**Ready for AI Coding Execution!** 🚀
