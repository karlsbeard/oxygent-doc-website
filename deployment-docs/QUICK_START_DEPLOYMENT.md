# 🚀 GitHub Pages 部署快速开始

## 📝 当前状态

✅ **所有配置已完成！** 你的项目现在可以自动部署到 GitHub Pages。

## 🎯 下一步操作

### 步骤 1: 在 GitHub 上启用 GitHub Pages

1. 打开你的 GitHub 仓库: `https://github.com/karlsbeard/oxygent-doc-website`

2. 点击 **Settings** (设置)

3. 在左侧菜单找到 **Pages**

4. 在 **Build and deployment** 部分:
   - **Source**: 选择 `GitHub Actions` (而不是 Deploy from a branch)

5. 保存设置

### 步骤 2: 推送代码

```bash
# 添加所有更改
git add .

# 提交更改
git commit -m "feat: configure GitHub Pages deployment

- Add GitHub Actions workflow for automatic deployment
- Configure Next.js for static export
- Add .nojekyll file for GitHub Pages
- Add deployment documentation"

# 推送到 main 分支
git push origin main
```

### 步骤 3: 查看部署进度

1. 推送后，自动触发 GitHub Actions workflow

2. 在仓库页面点击 **Actions** 标签

3. 你会看到 "Deploy to GitHub Pages" workflow 正在运行

4. 等待 workflow 完成（通常 3-5 分钟）

### 步骤 4: 访问你的网站

部署成功后，你的网站将在以下地址可用：

**选项 A: 自定义域名 (如果已配置)**

- `https://your-custom-domain.com`

**选项 B: GitHub Pages 默认域名**

- `https://karlsbeard.github.io/oxygent-doc-website/`

> ⚠️ **重要**: 如果使用选项 B（子路径部署），需要额外配置！

## ⚙️ 子路径部署配置 (如果需要)

如果你的网站部署在 `https://karlsbeard.github.io/oxygent-doc-website/`（而不是根域名），需要：

### 1. 修改 `next.config.mjs`

取消注释以下行：

```javascript
basePath: basePath,
assetPrefix: basePath,
```

完整配置应该是：

```javascript
const config = {
  reactStrictMode: true,
  output: 'export',

  basePath, // ← 取消注释
  assetPrefix: basePath, // ← 取消注释

  images: {
    unoptimized: true,
  },
  trailingSlash: true,
}
```

### 2. 修改 `.github/workflows/deploy.yml`

在 "Build with Next.js" 步骤的 env 部分设置：

```yaml
- name: Build with Next.js
  run: pnpm build
  env:
    NEXT_PUBLIC_BASE_PATH: /oxygent-doc-website # ← 设置你的仓库名
```

### 3. 提交并推送更改

```bash
git add .
git commit -m "feat: configure basePath for GitHub Pages"
git push origin main
```

## 🔍 验证部署

部署成功后检查：

- ✅ 网站可以访问
- ✅ 样式加载正常
- ✅ 图片显示正常
- ✅ 链接跳转正常
- ✅ 搜索功能正常（如果有）

## 📊 已创建的文件

```
oxygent-doc-website/
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions workflow
├── public/
│   └── .nojekyll                   # 告诉 GitHub Pages 不要使用 Jekyll
├── next.config.mjs                 # Next.js 配置（已添加静态导出）
├── DEPLOYMENT.md                   # 详细部署文档
├── QUICK_START_DEPLOYMENT.md       # 本文件
└── check-deployment.sh             # 配置检查脚本
```

## 🛠️ 有用的命令

```bash
# 本地构建测试
pnpm build

# 本地运行生产版本
pnpm start

# 运行配置检查
./check-deployment.sh

# 手动触发部署（如果需要）
# 在 GitHub Actions 页面点击 "Run workflow"
```

## 🔄 更新流程

每次更新内容后：

```bash
# 1. 修改文档内容
# 2. 本地测试（可选）
pnpm dev

# 3. 提交更改
git add .
git commit -m "docs: update content"

# 4. 推送（自动触发部署）
git push origin main

# 5. 等待部署完成（3-5 分钟）
# 6. 访问网站查看更新
```

## ❓ 常见问题

### Q: 部署需要多长时间？

A: 通常 3-5 分钟。可以在 Actions 标签页查看进度。

### Q: 如何手动触发部署？

A: 进入 Actions → Deploy to GitHub Pages → Run workflow

### Q: 页面显示 404

A: 检查：

1. GitHub Pages 是否设置为 "GitHub Actions"
2. basePath 是否配置正确
3. 部署是否成功完成

### Q: 样式加载失败

A: 检查：

1. basePath 和 assetPrefix 是否配置正确
2. 浏览器控制台的错误信息
3. 是否使用了相对路径

### Q: 本地 Node.js 版本不够？

A: 本地版本不影响部署，GitHub Actions 使用 Node.js 22

## 📚 相关文档

- [DEPLOYMENT.md](./DEPLOYMENT.md) - 详细部署指南
- [Fumadocs 文档](https://fumadocs.vercel.app)
- [Next.js Static Exports](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
- [GitHub Pages 文档](https://docs.github.com/en/pages)

## 🎉 完成

配置已全部完成。现在只需：

1. 在 GitHub 设置中启用 GitHub Pages (Source: GitHub Actions)
2. 推送代码
3. 等待部署完成
4. 访问你的网站！

---

**配置时间**: 2025-10-24
**仓库**: karlsbeard/oxygent-doc-website
**状态**: ✅ 就绪
