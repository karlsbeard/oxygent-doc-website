# 部署指南 (Deployment Guide)

本文档提供 OxyGent 文档网站的完整部署方案，包括 GitHub Pages 和其他部署选项。

## 📋 目录

- [GitHub Pages 部署](#github-pages-部署)
- [本地测试部署](#本地测试部署)
- [其他部署选项](#其他部署选项)
- [常见问题](#常见问题)

---

## 🚀 GitHub Pages 部署

### 前提条件

- ✅ GitHub 账户和仓库访问权限
- ✅ Node.js >= 22
- ✅ pnpm >= 9

### 自动部署（推荐）

项目已配置 GitHub Actions 自动部署，每次推送到 `master` 分支时自动触发。

#### 步骤 1: 启用 GitHub Pages

1. 进入 GitHub 仓库: `https://github.com/karlsbeard/oxygent-doc-website`
2. 点击 **Settings** → **Pages**
3. 在 **Source** 下选择 **GitHub Actions**

![GitHub Pages Settings](https://docs.github.com/assets/cb-47267/mw-1440/images/help/pages/publishing-source-drop-down.webp)

#### 步骤 2: 推送代码触发部署

```bash
git add .
git commit -m "feat: enable GitHub Pages deployment"
git push origin master
```

#### 步骤 3: 查看部署状态

1. 进入仓库的 **Actions** 标签页
2. 查看 "Deploy to GitHub Pages" workflow 运行状态
3. 部署成功后，访问: **https://karlsbeard.github.io/oxygent-doc-website/**

### 手动部署

如果需要手动触发部署：

1. 进入 GitHub 仓库的 **Actions** 标签页
2. 选择 "Deploy to GitHub Pages" workflow
3. 点击 **Run workflow** → **Run workflow**

---

## 🧪 本地测试部署

在推送到 GitHub 之前，建议先在本地测试构建：

### 方法 1: 标准构建

```bash
# 安装依赖
pnpm install

# 构建静态站点
pnpm build

# 预览构建结果（使用 serve 或其他静态服务器）
npx serve out
```

访问: `http://localhost:3000/oxygent-doc-website/`

### 方法 2: 使用 GitHub Pages 专用脚本

```bash
# 使用与 GitHub Actions 相同的配置构建
pnpm build:github-pages

# 预览
npx serve out
```

### 本地开发模式

开发时无需设置 basePath，直接运行：

```bash
pnpm dev
```

访问: `http://localhost:3000/`

---

## 🌐 其他部署选项

### Docker 部署

如果需要使用 Docker 部署（非静态导出），需要修改配置：

#### 1. 修改 `next.config.mjs`

```javascript
const config = {
  reactStrictMode: true,
  // 注释或删除以下行
  // output: 'export',

  // 根据需要保留或删除 basePath
  // basePath: basePath,
  // assetPrefix: basePath,

  images: {
    unoptimized: false, // 可以启用图片优化
  },
}
```

#### 2. 使用 Docker Compose

创建 `docker-compose.yml`:

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
```

创建 `Dockerfile`:

```dockerfile
FROM node:22-alpine AS base

FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json pnpm-lock.yaml* source.config.ts ./
RUN corepack enable pnpm && pnpm i --frozen-lockfile

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN corepack enable pnpm && pnpm run build

FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

构建和运行：

```bash
docker-compose up --build
```

### Vercel 部署

Vercel 是 Next.js 的官方推荐平台：

1. 安装 Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. 登录并部署:
   ```bash
   vercel login
   vercel
   ```

3. 或者通过 Vercel Dashboard 导入 GitHub 仓库

**注意**: Vercel 部署时需要移除或注释 `output: 'export'` 配置。

### Netlify 部署

1. 在 Netlify Dashboard 中导入 GitHub 仓库
2. 配置构建设置:
   - **Build command**: `pnpm build`
   - **Publish directory**: `out`
   - **环境变量**: `NEXT_PUBLIC_BASE_PATH` 设为空字符串

### Cloudflare Pages

使用 [OpenNext](https://opennext.js.org/cloudflare) 适配器：

```bash
npm install -D @opennext/cloudflare
```

**注意**: Fumadocs 不支持 Edge Runtime，需要使用 Node.js Runtime。

---

## ❓ 常见问题

### Q1: 部署后样式丢失或资源 404

**原因**: basePath 配置不正确

**解决方案**:
- 确认 `next.config.mjs` 中的 `basePath` 与实际部署路径匹配
- GitHub Pages: `/oxygent-doc-website`
- 自定义域名: 设为空字符串 `''`

### Q2: GitHub Actions 构建失败

**常见原因**:
1. Node.js 版本不匹配（需要 >= 22）
2. pnpm 版本不匹配（需要 >= 9）
3. 依赖安装失败

**解决方案**:
```bash
# 本地测试构建
pnpm install --frozen-lockfile
pnpm build
```

查看 Actions 日志获取详细错误信息。

### Q3: 如何切换到自定义域名？

1. 在 GitHub Pages 设置中配置自定义域名
2. 修改 `next.config.mjs`:
   ```javascript
   const basePath = process.env.NEXT_PUBLIC_BASE_PATH || ''
   ```
3. 修改 `.github/workflows/deploy.yml`:
   ```yaml
   env:
     NEXT_PUBLIC_BASE_PATH: ''
   ```
4. 推送更改并重新部署

### Q4: 能否同时支持多个部署环境？

可以！使用环境变量区分：

```javascript
// next.config.mjs
const basePath = process.env.NEXT_PUBLIC_BASE_PATH ||
  (process.env.NODE_ENV === 'production' ? '/oxygent-doc-website' : '')
```

### Q5: 构建后 `.next` 目录很大，如何优化？

静态导出 (`output: 'export'`) 只会生成 `out` 目录，`.next` 是中间产物，不会部署。

如果需要优化构建速度：
- 使用 pnpm 缓存（已在 GitHub Actions 中配置）
- 考虑使用 Turbopack（开发模式已启用）

---

## 📚 参考资料

- [Next.js 部署文档](https://nextjs.org/docs/app/getting-started/deploying)
- [Next.js 静态导出](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [Fumadocs 部署指南](https://fumadocs.vercel.app/docs/ui/deploying)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

---

## 📞 支持

如有问题，请：
1. 查看 GitHub Actions 运行日志
2. 检查浏览器控制台错误
3. 在项目仓库提交 Issue

**当前部署配置**:
- 📦 仓库: `karlsbeard/oxygent-doc-website`
- 🌐 URL: https://karlsbeard.github.io/oxygent-doc-website/
- 🔧 框架: Next.js 15 + Fumadocs
- 🚀 部署方式: GitHub Actions (自动)
