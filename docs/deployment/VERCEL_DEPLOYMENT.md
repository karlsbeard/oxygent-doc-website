# Vercel 部署指南

## 🎯 为什么选择 Vercel？

✅ **完美支持 Next.js**：Vercel 是 Next.js 的开发商，提供最佳集成
✅ **零配置部署**：连接 GitHub 仓库即可自动部署
✅ **全球 CDN**：自动部署到全球边缘网络，访问速度快
✅ **免费额度充足**：100GB/月 带宽，完全够用
✅ **完美 i18n 支持**：自动处理多语言路由
✅ **自动优化**：图片优化、代码分割、智能缓存

## 🚀 快速部署（5分钟完成）

### 步骤 1：连接 Vercel

1. 访问 [vercel.com](https://vercel.com)
2. 点击 **"Sign Up"** 或 **"Login"**
3. 选择 **"Continue with GitHub"** 使用 GitHub 账号登录
4. 授权 Vercel 访问你的 GitHub 仓库

### 步骤 2：导入项目

1. 登录后点击 **"Add New..."** → **"Project"**
2. 在项目列表中找到 `oxygent-doc-website`
   - 如果没看到，点击 **"Adjust GitHub App Permissions"** 添加仓库访问权限
3. 点击仓库右侧的 **"Import"** 按钮

### 步骤 3：配置项目（使用默认设置）

Vercel 会自动检测项目配置，你只需确认：

```
Framework Preset: Next.js ✅ (自动检测)
Root Directory: ./ ✅
Build Command: pnpm build ✅ (自动检测)
Output Directory: .next ✅
Install Command: pnpm install ✅ (自动检测)
```

**不需要添加任何环境变量！** 点击 **"Deploy"** 即可。

### 步骤 4：等待部署完成

- ⏱️ 首次部署约 2-3 分钟
- 🎉 部署成功后会显示预览 URL

### 步骤 5：访问网站

部署完成后，你会获得：
- **生产 URL**：`https://oxygent-doc-website.vercel.app`
- **自动 HTTPS**：SSL 证书自动配置
- **全球 CDN**：所有静态资源自动分发

## 🔄 自动部署流程

配置完成后，每次推送代码到 GitHub 都会自动触发部署：

```bash
git add .
git commit -m "update: documentation"
git push origin master
```

Vercel 会自动：
1. 检测到新的 commit
2. 拉取最新代码
3. 运行 `pnpm build`
4. 部署到全球 CDN
5. 发送部署通知（邮件）

## 📊 部署状态监控

### Vercel 仪表板

访问 [vercel.com/dashboard](https://vercel.com/dashboard) 查看：

- **部署历史**：每次部署的状态和日志
- **性能分析**：页面加载速度、Core Web Vitals
- **访问统计**：流量、带宽使用情况
- **预览部署**：每个 PR 的独立预览 URL

### 部署状态

- ✅ **Ready**：部署成功
- 🔄 **Building**：正在构建
- ❌ **Error**：构建失败（点击查看日志）

## 🌐 自定义域名（可选）

### 绑定自定义域名

1. 在 Vercel 项目设置中点击 **"Domains"**
2. 输入你的域名（如 `docs.oxygent.ai`）
3. 根据提示配置 DNS 记录：

```dns
类型: CNAME
名称: docs
值: cname.vercel-dns.com
```

4. 等待 DNS 生效（通常 5-10 分钟）
5. Vercel 自动配置 SSL 证书

## 🔧 高级配置

### 环境变量（如需要）

在 Vercel 项目设置 → **"Environment Variables"** 中添加：

```env
# 示例：自定义 basePath（通常不需要）
NEXT_PUBLIC_BASE_PATH=

# 示例：Google Analytics ID
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

### 构建缓存

Vercel 自动缓存 `node_modules` 和构建产物，加快后续部署速度。

### 预览部署

每个 Pull Request 都会自动创建预览部署：
- 独立 URL：`https://oxygent-doc-website-git-<branch>-<user>.vercel.app`
- 在 PR 评论中自动显示预览链接
- 合并到 master 后自动部署到生产环境

## 📈 性能优化（Vercel 自动处理）

Vercel 自动应用以下优化：

✅ **图片优化**：自动 WebP/AVIF 转换，响应式图片
✅ **代码分割**：按需加载 JavaScript
✅ **边缘缓存**：静态资源缓存在全球节点
✅ **Brotli 压缩**：自动压缩文本资源
✅ **HTTP/2 推送**：预加载关键资源

## 🌏 部署区域

**免费计划（Hobby）**：
- ✅ 自动部署到全球边缘网络
- ✅ Vercel 智能选择最优节点
- ✅ 覆盖全球主要地区（包括亚太）
- ℹ️ 不支持自定义区域配置

**Pro/Enterprise 计划**：
- 可自定义部署区域
- 支持多区域配置
- 更多性能优化选项

💡 **对于免费用户**：Vercel 会自动将你的应用部署到全球 CDN，无需手动配置区域。

## 💰 成本估算

### 免费额度（Hobby 计划）

```
带宽：100 GB/月
构建时间：6000 分钟/月
部署数量：无限制
团队成员：1 人
```

### 预估使用量

```
单页大小：~2 MB
月访问量：1000 次
总带宽：2000 MB ≈ 2 GB

使用率：2 GB / 100 GB = 2% ✅
```

**结论**：完全在免费额度内！

### 升级选项

如果超出免费额度：
- **Pro 计划**：$20/月（1TB 带宽）
- **企业计划**：按需定价

## 🐛 故障排查

### 构建失败

查看构建日志：
1. Vercel 仪表板 → 你的项目
2. 点击失败的部署
3. 查看 **"Build Logs"**

常见问题：
- ❌ **依赖安装失败**：检查 `package.json`
- ❌ **类型错误**：运行 `pnpm build` 本地测试
- ❌ **环境变量缺失**：在 Vercel 设置中添加

### 搜索功能不工作

✅ **已修复**：当前配置使用 `static` 搜索模式，完美支持 Vercel

### 路由问题

✅ **已修复**：`hideLocale: 'always'` 在 Vercel 上完美工作

## 📚 相关资源

- [Vercel 文档](https://vercel.com/docs)
- [Next.js 部署](https://nextjs.org/docs/deployment)
- [Vercel CLI](https://vercel.com/docs/cli)

## 🔄 切换回其他部署方式

### Docker 部署

Docker 配置仍然保留，可以随时切换：

```bash
# 构建 Docker 镜像
pnpm docker:build

# 启动容器
pnpm docker:up

# 访问 http://localhost:3000
```

### 本地测试

```bash
# 开发模式
pnpm dev

# 生产构建测试
pnpm build
pnpm start
```

## ✅ 部署检查清单

- [x] 创建 `vercel.json` 配置
- [x] 清理 GitHub Pages 相关文件
- [x] 简化 `next.config.mjs`
- [x] 测试本地构建成功
- [ ] 连接 Vercel 账号
- [ ] 导入 GitHub 仓库
- [ ] 部署成功
- [ ] 测试搜索功能
- [ ] 测试多语言切换
- [ ] 测试左侧菜单导航

## 🎉 完成！

现在你的文档站已经配置完成，准备部署到 Vercel。

**下一步**：访问 [vercel.com](https://vercel.com) 开始部署！
