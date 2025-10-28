# OxyGent Documentation Migration Plan

## Overview
Migrate OxyGent documentation from `OxyGent/docs_building/docs_en/` to `content/docs/` following fumadocs conventions.

## Source Structure Analysis

### Source Directory: `OxyGent/docs_building/docs_en/`
```
├── README.md (main project intro)
├── OxyGent/
│   ├── Introduction.md
│   ├── QuickStart.md
│   ├── Configuration.md
│   └── Visualization.md
├── Context/
│   ├── OxyRequest.md
│   ├── OxyResponse.md
│   └── OxyState.md
├── Oxy/
│   ├── Agents/ (6 files + 1 subdirectory)
│   ├── Flows/ (3 files)
│   ├── LLMs/ (2 files)
│   └── Tools/ (4 files)
├── Extensions/ (2 files)
├── Examples/ (Python files + README)
├── API Reference/ (extensive API docs)
├── FAQ.md
└── MAS.md
```

### Images Found:
1. `OxyGent/docs_building/images/` (5 images)
2. `OxyGent/docs_building/docs_en/Oxy/Agents/SSEOxyAgentFloder/SSEOxyAgentUsingExampleFigure.png`

## Target Structure: `content/docs/`

### File Naming Convention
- Use kebab-case for all files
- Prefix with section name for clarity
- Use .mdx extension
- Add frontmatter with title, description

### Detailed File Mapping

#### 1. Core Documentation (Getting Started)
| Source | Target | Priority |
|--------|--------|----------|
| `README.md` | `index.mdx` | High |
| `OxyGent/Introduction.md` | `introduction.mdx` | High |
| `OxyGent/QuickStart.md` | `quick-start.mdx` | High |
| `OxyGent/Configuration.md` | `configuration.mdx` | High |
| `OxyGent/Visualization.md` | `visualization.mdx` | Medium |

#### 2. Context Documentation
| Source | Target | Priority |
|--------|--------|----------|
| `Context/OxyRequest.md` | `context-oxy-request.mdx` | Medium |
| `Context/OxyResponse.md` | `context-oxy-response.mdx` | Medium |
| `Context/OxyState.md` | `context-oxy-state.mdx` | Medium |

#### 3. Oxy Agents
| Source | Target | Priority |
|--------|--------|----------|
| `Oxy/Agents/ChatAgent.md` | `agents-chat.mdx` | High |
| `Oxy/Agents/ParallelAgent.md` | `agents-parallel.mdx` | High |
| `Oxy/Agents/RagAgent.md` | `agents-rag.mdx` | Medium |
| `Oxy/Agents/ReActAgent.md` | `agents-react.mdx` | High |
| `Oxy/Agents/SSEOxyGent.md` | `agents-sse-oxygent.mdx` | Medium |
| `Oxy/Agents/SSEOxyAgentFloder/SSEOxyAgent.md` | `agents-sse-agent.mdx` | Medium |

#### 4. Oxy Flows
| Source | Target | Priority |
|--------|--------|----------|
| `Oxy/Flows/ParallelFlow.md` | `flows-parallel.mdx` | High |
| `Oxy/Flows/PlanAndSolve.md` | `flows-plan-and-solve.mdx` | High |
| `Oxy/Flows/Reflexion.md` | `flows-reflexion.mdx` | Medium |

#### 5. Oxy LLMs
| Source | Target | Priority |
|--------|--------|----------|
| `Oxy/LLMs/HttpLLM.md` | `llms-http.mdx` | High |
| `Oxy/LLMs/OpenAILLM.md` | `llms-openai.mdx` | High |

#### 6. Oxy Tools
| Source | Target | Priority |
|--------|--------|----------|
| `Oxy/Tools/FunctionHub.md` | `tools-function-hub.mdx` | High |
| `Oxy/Tools/LocalMCPClient.md` | `tools-local-mcp.mdx` | High |
| `Oxy/Tools/SSEMCPClient.md` | `tools-sse-mcp.mdx` | Medium |
| `Oxy/Tools/StreamableMCPClient.md` | `tools-streamable-mcp.mdx` | Medium |

#### 7. Extensions
| Source | Target | Priority |
|--------|--------|----------|
| `Extensions/integrate_oxygent_into_web_server.md` | `extensions-web-server.mdx` | Medium |
| `Extensions/web_api.md` | `extensions-web-api.mdx` | Medium |

#### 8. FAQ & MAS
| Source | Target | Priority |
|--------|--------|----------|
| `FAQ.md` | `faq.mdx` | High |
| `MAS.md` | `mas.mdx` | High |

#### 9. API Reference (Selective - High Priority Only)
| Source | Target | Priority |
|--------|--------|----------|
| `API Reference/README.md` | `api-reference.mdx` | Medium |
| `API Reference/agent/base_agent.md` | `api-base-agent.mdx` | Low |
| `API Reference/agent/chat_agent.md` | `api-chat-agent.mdx` | Low |
| ... (other API files as needed) | ... | Low |

Note: API Reference files will be migrated selectively based on importance.

## Image Migration Plan

### Source Images
1. `OxyGent/docs_building/images/`:
   - `Intinalization Process.png`
   - `chat_with_agent interact process.png`
   - `prod_data_oxygent_github_images_banner.jpg`
   - `quickstart_chat.png`
   - `quickstart_chat_flow_chat.png`

2. `OxyGent/docs_building/docs_en/Oxy/Agents/SSEOxyAgentFloder/`:
   - `SSEOxyAgentUsingExampleFigure.png`

### Target Location
All images will be migrated to: `public/images/oxygent/`

### Image Path Updates
- Old: `../../images/quickstart_chat.png`
- New: `/images/oxygent/quickstart_chat.png`

## meta.json Structure

```json
{
  "pages": [
    "index",
    "---Getting Started---",
    "introduction",
    "quick-start",
    "configuration",
    "visualization",
    "---Core Concepts---",
    {
      "title": "Context",
      "pages": [
        "context-oxy-request",
        "context-oxy-response",
        "context-oxy-state"
      ]
    },
    "---Oxy Framework---",
    {
      "title": "Agents",
      "pages": [
        "agents-chat",
        "agents-react",
        "agents-parallel",
        "agents-rag",
        "agents-sse-oxygent",
        "agents-sse-agent"
      ]
    },
    {
      "title": "Flows",
      "pages": [
        "flows-parallel",
        "flows-plan-and-solve",
        "flows-reflexion"
      ]
    },
    {
      "title": "LLMs",
      "pages": [
        "llms-http",
        "llms-openai"
      ]
    },
    {
      "title": "Tools",
      "pages": [
        "tools-function-hub",
        "tools-local-mcp",
        "tools-sse-mcp",
        "tools-streamable-mcp"
      ]
    },
    "---Advanced---",
    {
      "title": "Extensions",
      "pages": [
        "extensions-web-server",
        "extensions-web-api"
      ]
    },
    "mas",
    "---Help---",
    "faq"
  ]
}
```

## Frontmatter Template

```yaml
---
title: Document Title
description: Brief description of the document content
icon: IconName (optional)
---
```

## Image Reference Updates

### Pattern to Replace:
1. `../../images/` → `/images/oxygent/`
2. Relative paths → Absolute paths from public directory
3. External images (storage.jd.com) → Keep as-is or download if needed

## Conversion Process

### For Each Markdown File:
1. **Read** source `.md` file
2. **Extract** title from first heading or filename
3. **Add** frontmatter with title and description
4. **Update** image paths
5. **Update** internal links
6. **Convert** to `.mdx` format
7. **Write** to target location

### Image Path Conversion:
```javascript
// Pattern matching
../../images/filename.png → /images/oxygent/filename.png
./SSEOxyAgentFloder/filename.png → /images/oxygent/filename.png
```

## Execution Phases

### Phase 1: Preparation (Current)
- [x] Analyze source structure
- [x] Create file mapping
- [x] Design meta.json structure
- [ ] Create backup of existing docs
- [ ] Clean existing content/docs

### Phase 2: Image Migration
- [ ] Create `public/images/oxygent/` directory
- [ ] Copy all images to target location
- [ ] Verify image integrity

### Phase 3: Core Documentation Migration
- [ ] Migrate Getting Started docs (index, introduction, quick-start)
- [ ] Migrate configuration and visualization
- [ ] Verify frontmatter and formatting

### Phase 4: Component Documentation Migration
- [ ] Migrate Context docs
- [ ] Migrate Agents docs
- [ ] Migrate Flows docs
- [ ] Migrate LLMs docs
- [ ] Migrate Tools docs

### Phase 5: Advanced Documentation Migration
- [ ] Migrate Extensions docs
- [ ] Migrate MAS and FAQ docs
- [ ] Selectively migrate API Reference docs

### Phase 6: Integration & Validation
- [ ] Create comprehensive meta.json
- [ ] Update all internal links
- [ ] Validate all image references
- [ ] Test with dev server
- [ ] Fix any rendering issues

## Quality Checklist

### For Each Migrated File:
- [ ] Frontmatter present with title and description
- [ ] All images display correctly
- [ ] All internal links work
- [ ] Code blocks have proper syntax highlighting
- [ ] Formatting preserved from original
- [ ] No broken external links

### Overall:
- [ ] All high-priority files migrated
- [ ] meta.json complete and correct
- [ ] Navigation structure logical
- [ ] No duplicate content
- [ ] Examples directory maintained separately
- [ ] Dev server runs without errors

## Notes
- Examples stay in `content/examples/` (already migrated)
- API Reference docs are low priority - migrate selectively
- Preserve Apache License headers if present
- Keep external image URLs (storage.jd.com) unless broken
