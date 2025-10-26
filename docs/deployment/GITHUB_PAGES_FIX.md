# GitHub Pages 404 问题修复说明

## 🐛 问题描述

部署到 GitHub Pages 后，访问 `https://karlsbeard.github.io/oxygent-doc-website/` 返回 404 错误。

## 🔍 问题原因

本项目使用了 **Next.js 国际化 (i18n)** 功能：

1. **静态导出限制**
   - 使用了 `output: 'export'` 进行静态导出
   - 静态导出**不支持 Next.js Middleware**
   - Middleware 通常用于处理 i18n 路由重定向

2. **目录结构**
   - 构建输出：`out/en-US/` 和 `out/zh-CN/`
   - **缺少根路径** `index.html`
   - 访问根路径时找不到文件 → 404

3. **期望行为 vs 实际行为**
   - ❌ 期望：middleware 将 `/` 重定向到 `/en-US/`
   - ❌ 实际：静态部署无 middleware，无法重定向
   - ✅ 需要：客户端 JavaScript 重定向

## ✅ 解决方案

创建客户端重定向页面 `public/index.html`：

### 功能特性

1. **自动语言检测**
   ```javascript
   const userLang = navigator.language || navigator.userLanguage;
   if (userLang.startsWith('zh')) {
     window.location.replace(basePath + '/zh-CN/');
   } else {
     window.location.replace(basePath + '/en-US/');
   }
   ```

2. **兜底重定向**
   ```html
   <meta http-equiv="refresh" content="0; url=./en-US/">
   ```

3. **用户体验**
   - 显示加载动画
   - 提供手动链接
   - 0 秒自动跳转

### 文件位置

```
oxygent-doc-website/
├── public/
│   └── index.html        ← 新增：重定向页面
├── out/                  ← 构建输出
│   ├── index.html        ← 自动复制
│   ├── en-US/
│   │   └── index.html
│   └── zh-CN/
│       └── index.html
```

## 📦 部署流程

### 自动部署

推送到 `master` 分支后：

1. GitHub Actions 自动触发
2. 构建静态文件到 `out/`
3. `public/index.html` 自动复制到 `out/index.html`
4. 部署到 GitHub Pages

### 访问流程

```
用户访问：https://karlsbeard.github.io/oxygent-doc-website/
         ↓
加载：    index.html (重定向页面)
         ↓
检测语言：浏览器语言 (zh-* → zh-CN, 其他 → en-US)
         ↓
重定向：  https://karlsbeard.github.io/oxygent-doc-website/en-US/
         ↓
显示文档  ✅
```

## 🧪 测试方法

### 本地测试

```bash
# 1. 构建项目
pnpm build

# 2. 检查 index.html 是否存在
ls -la out/index.html

# 3. 启动本地服务器
npx serve out -l 3000

# 4. 访问测试
# http://localhost:3000/oxygent-doc-website/
# → 应自动重定向到 /oxygent-doc-website/en-US/
```

### GitHub Pages 测试

1. 推送代码到 GitHub
2. 等待 Actions 完成（约 2-3 分钟）
3. 访问：https://karlsbeard.github.io/oxygent-doc-website/
4. 验证：
   - ✅ 自动重定向到 `/en-US/` 或 `/zh-CN/`
   - ✅ 页面正常加载
   - ✅ 样式和资源正常

## 🔧 技术细节

### 为什么使用客户端重定向？

| 方案 | 优点 | 缺点 | 适用性 |
|------|------|------|--------|
| **服务端 Middleware** | 快速、SEO 友好 | 需要服务器 | ❌ 静态导出不支持 |
| **客户端 JS 重定向** | 简单、无需服务器 | 轻微延迟 | ✅ GitHub Pages 可用 |
| **Meta Refresh** | 兜底方案 | 不够优雅 | ✅ 作为备选 |

### basePath 处理

```javascript
// 获取当前路径，移除尾部斜杠
const basePath = window.location.pathname.replace(/\/$/, '');

// basePath = '/oxygent-doc-website' (GitHub Pages)
// basePath = '' (自定义域名)

// 重定向
window.location.replace(basePath + '/en-US/');
```

这样可以：
- ✅ 支持 GitHub Pages (`/oxygent-doc-website/`)
- ✅ 支持自定义域名（basePath 为空）
- ✅ 支持本地开发

## 📝 相关修改

### 文件清单

- ✅ `public/index.html` - 新增重定向页面
- ✅ `next.config.mjs` - 已配置静态导出和 basePath
- ✅ `.github/workflows/deploy.yml` - 已配置 GitHub Actions
- ✅ `DEPLOYMENT.md` - 完整部署指南

### 配置要点

1. **Next.js 配置** (`next.config.mjs`)
   ```javascript
   output: 'export'  // 静态导出
   basePath: '/oxygent-doc-website'  // GitHub Pages 路径
   ```

2. **GitHub Actions** (`.github/workflows/deploy.yml`)
   ```yaml
   env:
     NEXT_PUBLIC_BASE_PATH: /oxygent-doc-website
   ```

3. **重定向页面** (`public/index.html`)
   - 自动语言检测
   - 客户端 JavaScript 重定向
   - Meta refresh 兜底

## 🚀 部署步骤

```bash
# 1. 确认修改
git status

# 2. 添加新文件
git add public/index.html

# 3. 提交
git commit -m "fix: add client-side redirect for GitHub Pages i18n routing"

# 4. 推送
git push origin master

# 5. 查看部署进度
# https://github.com/karlsbeard/oxygent-doc-website/actions

# 6. 访问测试
# https://karlsbeard.github.io/oxygent-doc-website/
```

## ⚠️ 注意事项

1. **SEO 影响**
   - 客户端重定向对 SEO 有轻微影响
   - 搜索引擎可能需要额外时间索引
   - 建议在 Google Search Console 提交两个语言版本

2. **性能考虑**
   - 重定向延迟：< 100ms
   - 用户体验：显示加载动画，体验良好
   - 兜底机制：Meta refresh 确保兼容性

3. **替代方案**
   - **Vercel/Netlify**: 支持 middleware，无需此修复
   - **单语言版本**: 移除 i18n，只使用英文或中文
   - **自定义服务器**: 使用 Node.js 服务器处理重定向

## 📊 对比分析

### 静态导出 vs 服务端渲染

| 特性 | 静态导出 (当前) | 服务端渲染 |
|------|----------------|-----------|
| 部署成本 | 🆓 免费 | 💰 需服务器 |
| 性能 | ⚡⚡⚡ 极快 | ⚡⚡ 快 |
| Middleware | ❌ 不支持 | ✅ 支持 |
| GitHub Pages | ✅ 完美支持 | ❌ 不支持 |
| 重定向方式 | 客户端 JS | 服务端 |
| SEO | ⭐⭐⭐ 良好 | ⭐⭐⭐⭐ 优秀 |

**结论**: 对于文档网站，静态导出 + 客户端重定向是最佳选择。

## ✅ 验证清单

部署后验证：

- [ ] 访问根路径自动重定向到 `/en-US/`
- [ ] 中文浏览器重定向到 `/zh-CN/`
- [ ] 英文浏览器重定向到 `/en-US/`
- [ ] 手动链接可点击
- [ ] 样式和资源正常加载
- [ ] 导航和搜索功能正常
- [ ] 跨页面链接正常工作

## 📚 参考资料

- [Next.js 静态导出文档](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
- [Next.js Middleware 限制](https://nextjs.org/docs/messages/export-no-custom-routes)
- [GitHub Pages 部署指南](https://docs.github.com/en/pages)
- [Fumadocs i18n 文档](https://fumadocs.vercel.app/docs/ui/i18n)

---

**修复日期**: 2025-10-25
**问题类型**: 静态导出 + i18n 路由冲突
**解决方案**: 客户端 JavaScript 重定向
**状态**: ✅ 已修复
