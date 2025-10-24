# 部署文档

本目录包含 OxyGent 文档网站的完整部署指南和配置说明。

## 📚 文档列表

### 快速开始

- **[QUICK_START_DEPLOYMENT.md](./QUICK_START_DEPLOYMENT.md)** - 快速开始指南
  - 3 步完成部署
  - 适合首次部署

### 详细文档

- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - 完整部署指南
  - 详细配置说明
  - 故障排查
  - 最佳实践

- **[DEPLOYMENT_SUMMARY.md](./DEPLOYMENT_SUMMARY.md)** - 配置总结
  - 配置检查清单
  - 文件说明
  - 部署流程图

- **[WORKFLOW_EXPLAINED.md](./WORKFLOW_EXPLAINED.md)** - Workflow 详解
  - GITHUB_TOKEN 说明
  - github-pages 环境解释
  - 常见问题解答

### 辅助工具

- **[check-deployment.sh](./check-deployment.sh)** - 部署配置检查脚本
  - 自动验证配置
  - 显示详细结果

- **[README_DEPLOYMENT_SECTION.md](./README_DEPLOYMENT_SECTION.md)** - README 更新建议
  - 可复制到主 README

## 🚀 快速部署

```bash
# 1. 查看快速开始指南
cat QUICK_START_DEPLOYMENT.md

# 2. 运行配置检查
./check-deployment.sh

# 3. 推送代码
git push origin main
```

## 📖 建议阅读顺序

1. **首次部署**: QUICK_START_DEPLOYMENT.md
2. **详细了解**: DEPLOYMENT.md
3. **问题排查**: WORKFLOW_EXPLAINED.md
4. **验证配置**: 运行 check-deployment.sh

## 🔗 相关链接

- [GitHub Actions](https://github.com/karlsbeard/oxygent-doc-website/actions)
- [GitHub Pages 设置](https://github.com/karlsbeard/oxygent-doc-website/settings/pages)
- [部署历史](https://github.com/karlsbeard/oxygent-doc-website/deployments)

## ⚠️ 重要提示

- 所有 Markdown 文件 (*.md) 已被 ESLint 忽略
- Shell 脚本需要执行权限：`chmod +x check-deployment.sh`
- 文档中的示例配置可直接使用

---

**文档位置**: `/deployment-docs/`
**最后更新**: 2025-10-24
