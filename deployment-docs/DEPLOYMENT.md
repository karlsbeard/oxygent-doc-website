# GitHub Pages 部署指南

本文档描述如何将 OxyGent 文档网站部署到 GitHub Pages。

## 📋 前置要求

- GitHub 仓库已创建
- 项目使用 pnpm 作为包管理器
- Node.js >= 22

## 🚀 自动部署配置

已配置好自动部署 workflow，每次推送到 `main` 或 `master` 分支时会自动触发部署。

### 1. GitHub 仓库设置

在 GitHub 仓库中启用 GitHub Pages：

1. 进入仓库的 **Settings** 页面
2. 在左侧菜单中选择 **Pages**
3. 在 **Build and deployment** 部分：
   - **Source**: 选择 `GitHub Actions`

### 2. 配置文件说明

#### `.github/workflows/deploy.yml`

GitHub Actions 工作流文件，负责自动构建和部署。

**触发条件：**

- 推送到 `main` 或 `master` 分支
- 手动触发（在 Actions 标签页）

**工作流程：**

1. 检出代码
2. 安装 Node.js 22 和 pnpm 9
3. 缓存 pnpm 依赖
4. 安装依赖
5. 构建 Next.js 应用（静态导出）
6. 上传构建产物
7. 部署到 GitHub Pages

#### `next.config.mjs`

Next.js 配置文件，包含 GitHub Pages 部署所需的设置。

**关键配置：**

- `output: 'export'` - 启用静态导出
- `images.unoptimized: true` - 禁用图片优化
- `trailingSlash: true` - 添加尾部斜杠（可选）

### 3. 部署场景

#### 场景 A：部署到自定义域名或根路径

例如：`https://oxygent.com` 或 `https://username.github.io`

**配置：**
无需额外配置，保持默认即可。

#### 场景 B：部署到仓库子路径

例如：`https://username.github.io/oxygent-doc-website`

**配置步骤：**

1. 在 `next.config.mjs` 中取消注释以下行：

```javascript
basePath: basePath,
assetPrefix: basePath,
```

2. 在 `.github/workflows/deploy.yml` 中设置环境变量：

```yaml
env:
  NEXT_PUBLIC_BASE_PATH: /oxygent-doc-website
```

### 4. 本地测试

在部署前，你可以在本地测试构建：

```bash
# 安装依赖
pnpm install

# 构建项目
pnpm build

# 启动生产服务器（用于测试）
pnpm start
```

构建成功后，会在项目根目录生成 `out` 目录，这就是将被部署的静态文件。

### 5. 手动触发部署

如果需要手动触发部署：

1. 进入仓库的 **Actions** 标签页
2. 选择 **Deploy to GitHub Pages** workflow
3. 点击 **Run workflow**
4. 选择分支并点击绿色的 **Run workflow** 按钮

## 🔍 故障排查

### 问题 1: 404 错误

**原因：** basePath 配置不正确

**解决方案：**

- 如果部署在子路径，确保正确配置了 `basePath`
- 检查 GitHub Pages 设置中的 URL

### 问题 2: 样式或资源加载失败

**原因：** assetPrefix 配置不正确

**解决方案：**

- 确保 `assetPrefix` 与 `basePath` 一致
- 检查浏览器控制台的错误信息

### 问题 3: 图片显示不正常

**原因：** 图片优化未禁用

**解决方案：**

- 确保 `images.unoptimized: true` 已设置
- 使用相对路径引用图片

### 问题 4: 部署失败

**原因：** GitHub Pages 权限未设置

**解决方案：**

1. 检查 workflow 文件的 permissions 设置
2. 确保 GitHub Pages 源设置为 "GitHub Actions"
3. 查看 Actions 标签页的错误日志

## 📝 其他注意事项

### 环境变量

如果你的应用需要环境变量，可以在 GitHub 仓库设置中配置：

1. 进入 **Settings** > **Secrets and variables** > **Actions**
2. 添加所需的 secrets 或 variables
3. 在 workflow 文件中引用：

```yaml
env:
  MY_SECRET: ${{ secrets.MY_SECRET }}
```

### 自定义域名

如果要使用自定义域名：

1. 在 GitHub Pages 设置中配置 Custom domain
2. 在 DNS 提供商处添加 CNAME 记录
3. 等待 DNS 传播（可能需要几分钟到几小时）

### 构建优化

为了加快构建速度，workflow 已配置：

- pnpm store 缓存
- 依赖锁定文件（`pnpm-lock.yaml`）

## 🔗 相关链接

- [Next.js Static Exports](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Fumadocs Documentation](https://fumadocs.vercel.app)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## ✅ 部署检查清单

在首次部署前，请确认：

- [ ] GitHub 仓库已创建
- [ ] GitHub Pages 设置为 "GitHub Actions"
- [ ] `.github/workflows/deploy.yml` 文件已创建
- [ ] `next.config.mjs` 已配置静态导出
- [ ] `public/.nojekyll` 文件已创建
- [ ] basePath 配置正确（如果需要）
- [ ] 代码已推送到 main/master 分支
- [ ] Actions workflow 运行成功
- [ ] 网站可以访问

---

**初次部署时间**: 2025-10-24
**配置状态**: ✅ 已完成
