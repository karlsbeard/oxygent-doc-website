# 部署文档 / Deployment Documentation

本目录包含项目的各种部署方案和配置说明。

## 📚 文档列表

### 推荐部署方案

- **[VERCEL_STEP_BY_STEP_GUIDE.md](./VERCEL_STEP_BY_STEP_GUIDE.md)** - 🎯 Vercel 图文详细教程（新手推荐）
  - 📖 手把手图文教程
  - ⏱️ 5分钟快速部署
  - ❓ 10+ 常见问题解答
  - 🔄 自动部署流程说明

- **[VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md)** - Vercel 部署指南（快速参考）
  - ✅ 零配置部署
  - ✅ 全球 CDN 加速
  - ✅ 自动优化
  - ✅ 免费额度充足

### 替代部署方案

- **[DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md)** - Docker 容器化部署
  - 完整的 Docker 配置
  - 适合自托管服务器
  - 支持 standalone 模式

- **[GITHUB_PAGES_FIX.md](./GITHUB_PAGES_FIX.md)** - GitHub Pages 部署说明
  - ⚠️ 已弃用（不支持服务端路由）
  - 仅作参考

### 技术文档

- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - 通用部署概述
- **[ENVIRONMENT_DETECTION.md](./ENVIRONMENT_DETECTION.md)** - 环境检测机制说明

## 🚀 快速开始

### 推荐：Vercel 部署（5分钟）

1. 访问 [vercel.com](https://vercel.com)
2. 导入 GitHub 仓库
3. 点击 Deploy
4. 完成！

详细步骤请查看 [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md)

### Docker 部署

```bash
# 构建镜像
pnpm docker:build

# 启动容器
pnpm docker:up

# 访问 http://localhost:3000
```

详细配置请查看 [DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md)

## 📊 部署方案对比

| 方案 | 复杂度 | 成本 | 性能 | 推荐度 |
|------|--------|------|------|--------|
| Vercel | ⭐ 极简 | 免费 | ⭐⭐⭐⭐⭐ | ✅ 强烈推荐 |
| Docker | ⭐⭐⭐ 中等 | 服务器成本 | ⭐⭐⭐⭐ | 🟡 按需使用 |
| GitHub Pages | ⭐⭐ 简单 | 免费 | ⭐⭐ | ❌ 已弃用 |

## 💡 注意事项

- 本项目使用 `hideLocale: 'always'` 配置，需要服务端路由支持
- Vercel 是最佳选择，完美支持 Next.js 所有特性
- Docker 部署适合有特殊需求或自托管场景
- 不推荐使用 GitHub Pages（静态导出不支持动态路由）
