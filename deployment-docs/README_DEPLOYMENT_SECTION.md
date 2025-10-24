# README 部署章节建议

将以下内容添加到你的 README.md 文件中：

---

## 🚀 部署

本项目配置了自动部署到 GitHub Pages。

### 快速部署

1. **启用 GitHub Pages**
   - 进入 [仓库设置](https://github.com/karlsbeard/oxygent-doc-website/settings/pages)
   - Source: 选择 `GitHub Actions`

2. **推送代码**
   ```bash
   git push origin main
   ```

3. **访问网站**
   - 🌐 https://karlsbeard.github.io/oxygent-doc-website/

### 本地构建

```bash
# 安装依赖
pnpm install

# 开发模式
pnpm dev

# 生产构建
pnpm build

# 运行生产版本
pnpm start
```

### 配置检查

运行配置检查脚本：

```bash
./check-deployment.sh
```

### 文档

- 📖 [快速开始指南](./QUICK_START_DEPLOYMENT.md)
- 📚 [详细部署文档](./DEPLOYMENT.md)
- 📊 [配置总结](./DEPLOYMENT_SUMMARY.md)

---

## 或者，简洁版本：

---

## 🚀 部署

本项目自动部署到 GitHub Pages。

**网站地址**: https://karlsbeard.github.io/oxygent-doc-website/

每次推送到 `main` 分支都会自动触发部署。查看 [部署文档](./DEPLOYMENT.md) 了解详情。

---
