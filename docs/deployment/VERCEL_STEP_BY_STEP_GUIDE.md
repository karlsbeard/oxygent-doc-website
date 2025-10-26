# Vercel 部署详细图文教程

> 本教程将手把手教你如何将 GitHub 仓库部署到 Vercel，整个过程不超过 5 分钟！

## 📋 目录

- [前置准备](#前置准备)
- [第一步：创建 Vercel 账号](#第一步创建-vercel-账号)
- [第二步：连接 GitHub](#第二步连接-github)
- [第三步：导入项目](#第三步导入项目)
- [第四步：配置项目](#第四步配置项目)
- [第五步：开始部署](#第五步开始部署)
- [第六步：查看部署结果](#第六步查看部署结果)
- [自动部署机制](#自动部署机制)
- [常见问题](#常见问题)

---

## 前置准备

✅ **你需要准备：**

1. 一个 GitHub 账号
2. 项目代码已推送到 GitHub 仓库
3. 项目包含 `package.json` 文件

✅ **本项目已配置好：**

- ✅ `vercel.json` 配置文件
- ✅ `next.config.mjs` 优化配置
- ✅ 搜索功能（Orama）
- ✅ 多语言支持（i18n）

---

## 第一步：创建 Vercel 账号

### 1.1 访问 Vercel 官网

打开浏览器，访问 👉 [https://vercel.com](https://vercel.com)

### 1.2 注册账号

点击页面右上角的 **"Sign Up"** 按钮

**推荐方式：使用 GitHub 账号注册**

```
🔘 Continue with GitHub （推荐）
🔘 Continue with GitLab
🔘 Continue with Bitbucket
🔘 Continue with Email
```

**为什么推荐 GitHub？**

- ✅ 一键授权，无需单独注册
- ✅ 自动关联 GitHub 仓库
- ✅ 支持自动部署
- ✅ PR 预览功能

### 1.3 授权 GitHub

点击 **"Continue with GitHub"** 后，会跳转到 GitHub 授权页面：

```
Vercel by Vercel wants to access your account

This application will be able to:
✓ Read access to code
✓ Read and write access to checks, deployments, and pull requests
```

点击 **"Authorize Vercel"** 授权

---

## 第二步：连接 GitHub

### 2.1 进入 Dashboard

授权完成后，你会自动进入 Vercel Dashboard（控制面板）

页面地址：`https://vercel.com/dashboard`

### 2.2 配置 GitHub 权限

首次使用需要配置 GitHub 仓库访问权限：

**方式一：授予所有仓库访问权限（推荐新手）**

```
✓ All repositories
  授予 Vercel 访问你所有仓库的权限
```

**方式二：只授予特定仓库访问权限（推荐）**

```
✓ Only select repositories
  选择 oxygent-doc-website 仓库
```

点击 **"Install"** 或 **"Save"** 完成配置

---

## 第三步：导入项目

### 3.1 创建新项目

在 Dashboard 页面，点击 **"Add New..."** 按钮，选择 **"Project"**

```
┌─────────────────────────┐
│  Add New...             │
├─────────────────────────┤
│  Project          ← 选这个 │
│  Team                   │
│  Domain                 │
└─────────────────────────┘
```

### 3.2 选择 GitHub 仓库

你会看到 **"Import Git Repository"** 页面，展示你的 GitHub 仓库列表

**找到你的项目：**

```
🔍 Search repositories...

  GitHub
  ├─ your-username/oxygent-doc-website  [Import] ← 点击这里
  ├─ your-username/other-project        [Import]
  └─ ...
```

**找不到仓库？**

- 点击 **"Adjust GitHub App Permissions"**
- 重新配置仓库访问权限

### 3.3 点击 Import

找到 `oxygent-doc-website` 仓库，点击右侧的 **"Import"** 按钮

---

## 第四步：配置项目

### 4.1 自动检测配置

Vercel 会自动检测项目类型和配置：

```
Configure Project

Project Name: oxygent-doc-website
Framework Preset: Next.js ✅ (自动检测)
Root Directory: ./
Build Command: pnpm build ✅ (从 vercel.json 读取)
Output Directory: .next
Install Command: pnpm install ✅ (从 vercel.json 读取)
```

**✨ 重要提示：**

- 所有配置都已在 `vercel.json` 中预设好
- **无需修改任何配置！**
- 直接使用默认值即可

### 4.2 环境变量（可选）

本项目 **不需要** 配置任何环境变量！

如果未来需要添加环境变量（如 Google Analytics）：

```
Environment Variables (可选)

Name:  NEXT_PUBLIC_GA_ID
Value: G-XXXXXXXXXX
```

---

## 第五步：开始部署

### 5.1 点击 Deploy

确认配置无误后，点击页面底部的 **"Deploy"** 按钮

```
┌────────────────────────────────────┐
│                                    │
│         [Deploy]                   │
│                                    │
└────────────────────────────────────┘
```

### 5.2 部署进度

点击后会进入部署页面，显示实时构建日志：

```
Building...

○ Initializing build
● Cloning repository
  ↓ https://github.com/your-username/oxygent-doc-website.git
● Installing dependencies
  ↓ pnpm install
● Building application
  ↓ pnpm build
● Uploading build outputs
○ Deployment ready

⏱️ 预计时间：2-3 分钟
```

**构建日志示例：**

```bash
[12:00:00] Cloning repository...
[12:00:05] Installing dependencies with pnpm...
[12:00:30] Running build command: pnpm build
[12:01:00] ✓ Compiled successfully
[12:01:10] ✓ Linting and checking types
[12:01:20] ✓ Generating static pages (74 pages)
[12:01:25] ✓ Finalizing page optimization
[12:01:30] ✓ Deployment ready!
```

---

## 第六步：查看部署结果

### 6.1 部署成功

构建完成后，你会看到成功页面：

```
🎉 Congratulations!

Your project has been successfully deployed!

Production: https://oxygent-doc-website.vercel.app

✓ Domain: oxygent-doc-website.vercel.app
✓ Status: Ready
✓ Updated: Just now
```

### 6.2 访问你的网站

点击生产环境 URL 或复制链接到浏览器：

```
https://oxygent-doc-website.vercel.app
```

**你会看到：**

- ✅ 中英文文档正常显示
- ✅ 左侧导航菜单工作正常
- ✅ 搜索功能正常（按 Cmd+K 或点击搜索图标）
- ✅ 多语言切换正常

### 6.3 获取部署 URL

每次部署会生成三种 URL：

| URL 类型 | 格式 | 用途 |
|---------|------|------|
| **生产环境** | `https://oxygent-doc-website.vercel.app` | 主站点地址 |
| **预览环境** | `https://oxygent-doc-website-git-branch.vercel.app` | 分支预览 |
| **独立部署** | `https://oxygent-doc-website-hash.vercel.app` | 每次部署唯一 URL |

---

## 自动部署机制

### 🔄 自动化工作流

配置完成后，Vercel 会自动监听你的 GitHub 仓库：

```
┌─────────────────────────────────────────────┐
│                                             │
│  你的本地代码                                 │
│      ↓ git push                              │
│  GitHub 仓库 (master/main)                  │
│      ↓ 自动触发                              │
│  Vercel 构建                                 │
│      ↓ 2-3 分钟                              │
│  生产环境更新 ✅                              │
│                                             │
└─────────────────────────────────────────────┘
```

### 📝 工作流程详解

**1️⃣ 修改代码**

```bash
# 在本地修改代码
vim content/docs/index.mdx

# 查看修改
git status
```

**2️⃣ 提交到 GitHub**

```bash
git add .
git commit -m "docs: update documentation"
git push origin master
```

**3️⃣ Vercel 自动部署**

- GitHub 触发 webhook 通知 Vercel
- Vercel 自动拉取最新代码
- 运行 `pnpm build` 构建项目
- 部署到全球 CDN
- 发送邮件通知部署结果

**4️⃣ 访问新版本**

- 生产环境自动更新
- 用户访问时看到最新内容
- 无需任何手动操作

### 🌿 分支预览功能

**创建功能分支：**

```bash
git checkout -b feature/new-docs
# 修改代码
git push origin feature/new-docs
```

**自动创建预览环境：**

```
预览 URL: https://oxygent-doc-website-git-feature-new-docs.vercel.app
```

**在 Pull Request 中查看：**

- 打开 PR 页面
- Vercel bot 会自动评论预览 URL
- 点击 URL 可以预览修改效果
- 合并到 master 后自动部署到生产环境

---

## 常见问题

### ❓ Q1: 部署失败怎么办？

**查看构建日志：**

1. 进入 Vercel Dashboard
2. 点击失败的部署
3. 查看 **"Build Logs"** 详细日志

**常见错误：**

**错误 1：依赖安装失败**

```bash
Error: Cannot find module 'xxx'
```

**解决：**

- 检查 `package.json` 是否缺少依赖
- 本地运行 `pnpm install` 测试
- 确保 `pnpm-lock.yaml` 已提交

**错误 2：构建失败**

```bash
Error: Build failed
```

**解决：**

- 本地运行 `pnpm build` 测试
- 查看是否有 TypeScript 错误
- 检查 ESLint 错误

**错误 3：找不到文件**

```bash
Error: ENOENT: no such file or directory
```

**解决：**

- 检查文件路径大小写（Vercel 区分大小写）
- 确保文件已提交到 Git
- 检查 `.gitignore` 配置

### ❓ Q2: 搜索功能不工作？

✅ **已修复！** 本项目使用 `static` 搜索模式，完美支持 Vercel。

**验证搜索：**

1. 访问部署后的网站
2. 按 `Cmd+K` 或 `Ctrl+K`
3. 输入搜索关键词
4. 应该能看到搜索结果

**如果还是不工作：**

- 检查 `components/search.tsx` 配置
- 确保 `@orama/orama` 依赖已安装
- 查看浏览器控制台是否有错误

### ❓ Q3: 左侧菜单导航不工作？

✅ **已修复！** 删除了 `public/index.html` 重定向文件。

**验证导航：**

1. 访问 `/zh-CN/docs` 或 `/en-US/docs`
2. 点击左侧菜单任意链接
3. 页面应该正常跳转，不会重定向到首页

### ❓ Q4: 多语言切换不工作？

✅ **已配置！** `hideLocale: 'always'` 在 Vercel 上完美工作。

**验证多语言：**

1. 访问 `/zh-CN/docs` 查看中文版
2. 点击语言切换器
3. 应该能切换到 `/en-US/docs` 英文版

### ❓ Q5: 如何绑定自定义域名？

**步骤：**

1️⃣ **进入域名设置**

- Vercel Dashboard → 项目 → Settings → Domains

2️⃣ **添加域名**

```
Add Domain: docs.yourdomain.com
```

3️⃣ **配置 DNS**
在你的域名服务商添加 CNAME 记录：

```dns
类型: CNAME
名称: docs
值: cname.vercel-dns.com
```

4️⃣ **等待生效**

- DNS 生效时间：5-10 分钟
- Vercel 自动配置 SSL 证书
- 完成后可通过自定义域名访问

### ❓ Q6: 免费额度够用吗？

✅ **完全够用！**

**Vercel 免费计划：**

```
✓ 带宽：100 GB/月
✓ 构建时间：6000 分钟/月
✓ 部署次数：无限制
✓ 团队成员：1 人
```

**本项目预估使用量：**

```
单页大小：~2 MB
月访问量：1000 次
总带宽：2000 MB ≈ 2 GB

使用率：2 GB / 100 GB = 2% ✅
```

**结论：** 完全在免费额度内，无需担心！

### ❓ Q7: 如何查看部署历史？

**步骤：**

1. Vercel Dashboard → 你的项目
2. 点击 **"Deployments"** 标签
3. 查看所有部署记录

**部署状态：**

- ✅ **Ready**: 部署成功
- 🔄 **Building**: 正在构建
- ❌ **Error**: 构建失败
- ⏸️ **Canceled**: 已取消

### ❓ Q8: 如何回滚到之前的版本？

**步骤：**

1. Deployments → 选择历史部署
2. 点击 **"···"** 菜单
3. 选择 **"Promote to Production"**
4. 确认回滚

**注意：** 回滚不会影响 GitHub 代码，只是改变生产环境指向的部署版本。

### ❓ Q9: Node.js 版本问题？

**本项目配置：**

- 在 `package.json` 中指定：

```json
{
  "engines": {
    "node": ">=18.0.0"
  }
}
```

**Vercel 支持的版本：**

- Node.js 18.x（推荐）
- Node.js 20.x
- Node.js 22.x

### ❓ Q10: 如何加速国内访问？

**方案一：使用 CDN（推荐）**

- Vercel 自带全球 CDN
- 香港、新加坡节点覆盖亚太地区
- 无需额外配置

**方案二：绑定国内 CDN**

- 使用阿里云 CDN 或腾讯云 CDN
- 配置回源到 Vercel 域名
- 需要 ICP 备案

**方案三：自建反向代理**

- 在国内服务器部署 Nginx
- 反向代理到 Vercel
- 需要服务器和备案

---

## 🎉 部署成功！下一步？

### 推荐操作

1. **✅ 测试功能**
   - 访问所有页面确认正常
   - 测试搜索功能
   - 测试多语言切换

2. **📊 监控性能**
   - Vercel Dashboard → Analytics
   - 查看访问量和性能指标

3. **🔔 配置通知**
   - Vercel Dashboard → Settings → Notifications
   - 开启部署成功/失败邮件通知

4. **🌐 绑定域名（可选）**
   - 参考 Q5 配置自定义域名

5. **📝 更新文档**
   - 继续完善项目文档
   - 每次 push 自动部署

---

## 📚 相关资源

- [Vercel 官方文档](https://vercel.com/docs)
- [Next.js 部署指南](https://nextjs.org/docs/deployment)
- [Vercel CLI 工具](https://vercel.com/docs/cli)
- [项目部署文档](./VERCEL_DEPLOYMENT.md)

---

## 💬 需要帮助？

如果遇到问题：

1. 查看 [Vercel 官方文档](https://vercel.com/docs)
2. 搜索 [Vercel Discussions](https://github.com/vercel/vercel/discussions)
3. 查看项目的 `docs/deployment/` 目录下的其他文档

祝你部署顺利！🚀
