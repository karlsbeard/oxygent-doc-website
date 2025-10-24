# GitHub Actions Workflow 详解

本文档详细解释 `.github/workflows/deploy.yml` 的每个部分。

## 🔑 关于 GITHUB_TOKEN

### ❓ 常见疑问

**Q: 我需要手动创建 GITHUB_TOKEN 吗？**

**A: ❌ 不需要！它是自动提供的。**

### ✅ 工作原理

```yaml
permissions:
  contents: read      # 读取仓库内容
  pages: write        # 写入 GitHub Pages
  id-token: write     # 写入 ID token
```

**说明：**

1. **自动创建**
   - GitHub Actions 在每次运行时自动创建 `GITHUB_TOKEN`
   - 它是一个临时 token，只在当前 workflow 运行期间有效
   - workflow 结束后自动过期

2. **权限控制**
   - `permissions` 字段指定 token 的权限范围
   - 遵循最小权限原则（Principle of Least Privilege）
   - 只授予必需的权限

3. **使用方式**
   - Actions 中的其他步骤会自动使用这个 token
   - 例如：`actions/deploy-pages@v4` 会用它来部署
   - 你不需要显式传递或引用它

### 🔒 安全性

- ✅ 自动管理，无需手动创建
- ✅ 临时有效，降低泄露风险
- ✅ 权限受限，不能访问其他资源
- ✅ 不会出现在日志中

### 📝 你需要做什么？

**什么都不需要！** 只需：

1. 确保 workflow 文件包含 `permissions` 字段 ✅ (已包含)
2. 在 GitHub 仓库设置中启用 GitHub Pages

**不需要：**
- ❌ 在 Settings → Secrets 中创建 GITHUB_TOKEN
- ❌ 在 workflow 中显式引用 GITHUB_TOKEN
- ❌ 设置任何环境变量

## 🌍 关于 `github-pages` 环境

### ❓ IDE 警告说明

你可能看到这个警告：

```
⚠️ Value 'github-pages' is not valid
```

**这是误报，可以安全忽略！**

### ✅ 为什么使用 `github-pages`？

```yaml
environment:
  name: github-pages                                    # ← 必须是这个名称
  url: ${{ steps.deployment.outputs.page_url }}
```

**原因：**

1. **GitHub 保留名称**
   - `github-pages` 是 GitHub 的内置环境名称
   - 用于 GitHub Pages 部署
   - **必须使用这个确切的名称**

2. **自动创建**
   - 当你启用 GitHub Pages (Source: GitHub Actions) 时
   - GitHub 会自动创建 `github-pages` 环境
   - 你会在仓库的 Environments 页面看到它

3. **官方标准**
   - 这是 GitHub 官方文档推荐的配置
   - 所有使用 GitHub Pages 的 Actions 都应该用这个名称
   - 参考：[GitHub Docs - Deploying with GitHub Actions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow)

### 🔍 验证方法

部署成功后：

1. 访问：`https://github.com/karlsbeard/oxygent-doc-website/deployments`
2. 你会看到 "github-pages" 环境
3. 点击可以查看部署历史和详情

### 🛠️ 环境的作用

```yaml
environment:
  name: github-pages                                    # 环境名称
  url: ${{ steps.deployment.outputs.page_url }}        # 部署后的 URL
```

**功能：**

1. **部署追踪**
   - GitHub 会追踪每次部署
   - 可以查看历史部署记录
   - 可以回滚到之前的版本

2. **保护规则**（可选）
   - 可以设置部署前的审批流程
   - 可以限制谁能部署到这个环境
   - 可以设置环境变量

3. **部署 URL**
   - 自动获取部署后的 URL
   - 在 Actions 日志中显示
   - 方便快速访问

## 📊 Workflow 完整流程

### 1. 触发条件

```yaml
on:
  push:
    branches: [main, master]    # 推送到这些分支时触发
  workflow_dispatch:             # 允许手动触发
```

### 2. 权限配置

```yaml
permissions:
  contents: read      # 读取代码
  pages: write        # 写入 Pages
  id-token: write     # 身份验证
```

**自动应用到 GITHUB_TOKEN** ✅

### 3. 并发控制

```yaml
concurrency:
  group: "pages"
  cancel-in-progress: false
```

**作用：**
- 同时只运行一个部署
- 不取消正在进行的部署
- 避免部署冲突

### 4. 构建任务 (build)

```yaml
build:
  runs-on: ubuntu-latest
  steps:
    - Checkout 代码
    - 安装 Node.js 22
    - 安装 pnpm 9
    - 缓存依赖
    - 安装依赖
    - 配置 Pages
    - 构建项目
    - 上传产物
```

**使用 GITHUB_TOKEN：** ✅ (自动)
- actions/checkout@v4
- actions/configure-pages@v4
- actions/upload-pages-artifact@v3

### 5. 部署任务 (deploy)

```yaml
deploy:
  environment:
    name: github-pages          # ← GitHub 标准环境
    url: ${{ steps.deployment.outputs.page_url }}
  runs-on: ubuntu-latest
  needs: build
  steps:
    - Deploy to GitHub Pages
```

**使用 GITHUB_TOKEN：** ✅ (自动)
- actions/deploy-pages@v4

**部署到环境：** `github-pages` ✅ (GitHub 标准)

## 🎯 总结

### ✅ 正确配置检查清单

- [x] `permissions` 字段已配置
- [x] `environment.name` 设置为 `github-pages`
- [x] 使用官方 Actions (checkout, configure-pages, upload-pages-artifact, deploy-pages)
- [x] 不需要手动创建 GITHUB_TOKEN
- [x] 不需要手动创建 github-pages 环境

### ❌ 不需要做的事

- [ ] ❌ 在 Secrets 中创建 GITHUB_TOKEN
- [ ] ❌ 在 Environments 中手动创建 github-pages
- [ ] ❌ 修改 environment name
- [ ] ❌ 显式传递 GITHUB_TOKEN

### 🔧 你只需要做

1. ✅ 在 GitHub 仓库设置中启用 GitHub Pages (Source: GitHub Actions)
2. ✅ 推送代码到 main 分支
3. ✅ 等待自动部署完成

## 📚 参考资料

### 官方文档

- [GitHub Actions Permissions](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)
- [Deploying to GitHub Pages](https://docs.github.com/en/actions/deployment/deploying-to-github-pages)
- [Using Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)

### 相关 Actions

- [actions/checkout](https://github.com/actions/checkout)
- [actions/configure-pages](https://github.com/actions/configure-pages)
- [actions/upload-pages-artifact](https://github.com/actions/upload-pages-artifact)
- [actions/deploy-pages](https://github.com/actions/deploy-pages)

## ❓ 常见问题

### Q1: 为什么 IDE 警告 github-pages 无效？

**A:** IDE linter 不认识 GitHub 的保留环境名称，这是误报。`github-pages` 是正确的。

### Q2: 我需要创建 GITHUB_TOKEN 吗？

**A:** 不需要。它由 GitHub Actions 自动创建和管理。

### Q3: 如果部署失败怎么办？

**A:** 检查：
1. GitHub Pages 是否启用 (Source: GitHub Actions)
2. Actions 日志中的错误信息
3. permissions 配置是否正确

### Q4: 可以更改 environment name 吗？

**A:** 不建议。使用 `github-pages` 是 GitHub 的标准做法。

### Q5: GITHUB_TOKEN 有什么限制？

**A:**
- 只在当前 workflow 运行期间有效
- 权限由 permissions 字段限制
- 不能访问其他仓库（除非明确配置）

---

**最后更新**: 2025-10-24
**配置状态**: ✅ 完全正确
**建议操作**: 忽略 IDE 警告，直接部署
