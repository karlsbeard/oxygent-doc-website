# llms.txt 快速开始指南

## ✅ 已完成配置

你的项目现在已经支持 `llms.txt` 和 `llms-full.txt`!

## 📍 访问地址

### 开发环境
```bash
http://localhost:3000/llms.txt         # 简洁版 - 文档索引
http://localhost:3000/llms-full.txt    # 完整版 - 全部内容
```

### 生产环境
```bash
https://your-domain.com/llms.txt
https://your-domain.com/llms-full.txt
```

## 🧪 快速测试

```bash
# 1. 启动开发服务器
pnpm dev

# 2. 在新终端测试简洁版
curl http://localhost:3000/llms.txt

# 3. 测试完整版
curl http://localhost:3000/llms-full.txt
```

## 📁 创建的文件

```
app/
├── llms-txt/route.ts           ← llms.txt 简洁版路由
├── llms-full-txt/route.ts      ← llms-full.txt 完整版路由
middleware.ts                   ← URL 重写(已更新)
docs/LLMS-TXT-SETUP.md         ← 详细文档
```

## 🎯 主要功能

### llms.txt (简洁版)
- ✅ 网站概览
- ✅ 文档列表 + URL
- ✅ 示例列表 + URL
- ✅ 语言支持信息
- ✅ 1小时缓存

### llms-full.txt (完整版)
- ✅ 所有 llms.txt 的内容
- ✅ **完整的文档内容**(从 MDX 提取)
- ✅ **完整的示例内容**(从 MDX 提取)
- ✅ 自动去除 frontmatter
- ✅ 元数据信息
- ✅ 30分钟缓存

## 🔧 技术实现

### 核心原理
1. **动态生成**: 实时从 fumadocs source API 获取数据
2. **内容提取**: 直接读取 MDX 源文件
3. **URL 重写**: middleware 将 `/llms.txt` 重写为 `/llms-txt`
4. **自动更新**: 文档更新后自动生效

### 架构
```
请求: /llms.txt
    ↓
middleware.ts (URL 重写)
    ↓
app/llms-txt/route.ts (处理请求)
    ↓
返回: text/plain 响应
```

## 🌐 环境变量(可选)

在 `.env.local` 中设置:

```bash
# 生产环境 URL
NEXT_PUBLIC_BASE_URL=https://your-domain.com
```

## 📊 遵循规范

✅ [llmstxt.org](https://llmstxt.org/) 规范
- 纯文本格式
- 结构化内容
- 完整 URL 链接
- 元数据信息

## 🚀 部署注意事项

### Vercel / Netlify
- ✅ 自动支持,无需额外配置
- ✅ 缓存自动处理

### Docker
- ✅ 已支持(参考 `next.config.mjs`)
- ✅ 确保文件系统可访问 `content/` 目录

### 其他平台
- ✅ 确保 Node.js 运行时支持
- ✅ 确保可以读取文件系统

## 💡 使用场景

### 对 LLM
- 📚 快速了解文档结构
- 🧠 训练数据提取
- 🔍 上下文学习
- 💬 准确回答用户问题

### 对开发者
- 🤖 自动化工具集成
- 📡 API 端点使用
- 🔎 SEO 优化
- 📄 文档导出

## ❓ 常见问题

### Q: 内容什么时候更新?
A: 实时更新!每次请求都从最新的 MDX 文件生成。

### Q: 如何自定义内容?
A: 编辑 `app/llms-txt/route.ts` 或 `app/llms-full-txt/route.ts`

### Q: 支持哪些语言?
A: 自动包含项目中所有语言版本(en, zh-CN 等)

### Q: 会影响性能吗?
A: 不会。有缓存机制,且响应速度很快。

## 📖 详细文档

查看 `docs/LLMS-TXT-SETUP.md` 了解更多详细信息。

## ✨ 完成!

你的项目现在已经完全支持 llms.txt 规范。LLM 可以轻松发现和理解你的文档内容!

---

**设置时间**: 2025-10-27
**版本**: 1.0.0
**符合规范**: llmstxt.org
