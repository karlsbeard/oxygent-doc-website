# 项目结构

OxyGent 文档网站的文件组织结构。

## 📁 目录结构

```
oxygent-doc-website/
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions 自动部署配置
│
├── .husky/                         # Git hooks
│   └── pre-commit                  # 提交前检查（已适配 Node 版本）
│
├── app/                            # Next.js 应用主目录
│   └── [lang]/                     # 多语言支持
│
├── content/                        # 文档内容
│   └── examples/                   # 示例文档
│       ├── *.mdx                   # 英文示例
│       ├── *.zh-CN.mdx            # 中文示例
│       ├── index.mdx              # 英文索引
│       └── index.zh-CN.mdx        # 中文索引
│
├── deployment-docs/                # 📚 部署文档（新增）
│   ├── README.md                   # 文档导航
│   ├── DEPLOYMENT.md               # 完整部署指南
│   ├── DEPLOYMENT_SUMMARY.md       # 配置总结
│   ├── QUICK_START_DEPLOYMENT.md   # 快速开始
│   ├── WORKFLOW_EXPLAINED.md       # Workflow 详解
│   ├── README_DEPLOYMENT_SECTION.md # README 更新建议
│   └── check-deployment.sh         # 配置检查脚本
│
├── scripts/                        # 🛠️ 脚本工具（新增）
│   ├── README.md                   # 脚本说明
│   ├── translate_script.py         # 批量翻译
│   ├── translate_remaining.py      # 处理遗漏
│   ├── check_chinese.py            # 质量检查
│   ├── final_translate.py          # 生成报告
│   └── clean_all_chinese.py        # 最终验证
│
├── docs/                           # 📝 文档和报告
│   └── reports/                    # 工作报告
│       ├── TRANSLATION_REPORT.md   # 翻译报告
│       └── INDEX_UPDATE_REPORT.md  # 索引更新报告
│
├── public/                         # 静态资源
│   └── .nojekyll                   # GitHub Pages 配置
│
├── .eslintignore                   # ESLint 忽略规则（新增）
├── eslint.config.mjs               # ESLint 配置（已更新）
├── next.config.mjs                 # Next.js 配置（已更新）
├── package.json                    # 项目配置
└── PROJECT_STRUCTURE.md            # 本文件
```

## 📋 文件分类

### 核心配置文件

| 文件 | 说明 | 修改状态 |
|------|------|---------|
| `next.config.mjs` | Next.js 配置，包含静态导出设置 | ✅ 已更新 |
| `eslint.config.mjs` | ESLint 配置，添加了忽略规则 | ✅ 已更新 |
| `.eslintignore` | ESLint 忽略文件 | ✅ 新增 |
| `package.json` | 项目依赖和脚本 | 无需修改 |

### 部署相关

| 目录/文件 | 说明 |
|----------|------|
| `.github/workflows/deploy.yml` | 自动部署 workflow |
| `deployment-docs/` | 完整的部署文档集合 |
| `public/.nojekyll` | GitHub Pages 配置 |

### 工具脚本

| 目录/文件 | 说明 |
|----------|------|
| `scripts/` | Python 翻译和维护脚本 |
| `deployment-docs/check-deployment.sh` | 部署配置检查 |

### 文档内容

| 目录 | 说明 |
|------|------|
| `content/examples/` | 示例文档（中英文） |
| `docs/reports/` | 工作报告 |

## 🎯 文件整理说明

### 之前的问题
- ❌ 根目录杂乱，多个 Python 脚本
- ❌ 部署文档散落在根目录
- ❌ ESLint 错误阻止提交

### 整理后的改进
- ✅ **deployment-docs/**: 所有部署相关文档
- ✅ **scripts/**: 所有 Python 脚本
- ✅ **docs/reports/**: 工作报告
- ✅ 根目录保持干净整洁
- ✅ ESLint 配置已优化

## 📝 ESLint 配置说明

### 忽略的文件类型
```javascript
ignores: [
  '**/*.md',           // 所有 Markdown 文件
  '**/*.sh',           // Shell 脚本
  '**/*.py',           // Python 脚本
  '.github/**/*.yml',  // GitHub workflows
  'public/**',         // 公共资源
  'scripts/**',        // 脚本目录
  'deployment-docs/**' // 部署文档
]
```

### Git Hook 优化
- `.husky/pre-commit` 已更新
- Node < 22 时自动跳过 lint
- GitHub Actions 使用 Node 22 进行检查

## 🚀 快速导航

### 开发相关
- 📖 [示例文档](./content/examples/)
- 🛠️ [脚本工具](./scripts/)
- ⚙️ [Next.js 配置](./next.config.mjs)

### 部署相关
- 🚀 [快速部署](./deployment-docs/QUICK_START_DEPLOYMENT.md)
- 📚 [完整指南](./deployment-docs/DEPLOYMENT.md)
- 🔍 [配置检查](./deployment-docs/check-deployment.sh)

### 报告文档
- 📊 [翻译报告](./docs/reports/TRANSLATION_REPORT.md)
- 📝 [索引更新](./docs/reports/INDEX_UPDATE_REPORT.md)

## ⚠️ 重要提示

### Node 版本
- **本地开发**: Node 20+ (部分功能受限)
- **GitHub Actions**: Node 22 (完整功能)
- **ESLint**: 需要 Node 22 才能运行

### Git 提交
- Node < 22 时会跳过本地 lint
- 不影响提交，GitHub Actions 会检查
- 建议升级到 Node 22 以获得最佳体验

### 文件修改
- 修改部署文档请在 `deployment-docs/` 中操作
- 添加脚本请放到 `scripts/` 目录
- 生成的报告放到 `docs/reports/`

## 📚 相关文档

- [部署文档导航](./deployment-docs/README.md)
- [脚本工具说明](./scripts/README.md)
- [GitHub Actions](https://github.com/karlsbeard/oxygent-doc-website/actions)

---

**最后更新**: 2025-10-24
**项目状态**: ✅ 已整理
**结构版本**: v1.0
