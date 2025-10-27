# llms.txt 和 llms-full.txt 配置说明

## 概述

本项目已配置 `llms.txt` 和 `llms-full.txt` 文件,遵循 [llmstxt.org](https://llmstxt.org/) 规范,为 LLM(大语言模型)提供结构化的文档索引和内容。

## 访问端点

### 开发环境
- **llms.txt** (简洁版): `http://localhost:3000/llms.txt`
- **llms-full.txt** (完整版): `http://localhost:3000/llms-full.txt`

### 生产环境
- **llms.txt**: `https://your-domain.com/llms.txt`
- **llms-full.txt**: `https://your-domain.com/llms-full.txt`

## 功能说明

### llms.txt (简洁版)
- 提供网站概览和描述
- 列出所有文档页面的标题和 URL
- 列出所有示例的标题和 URL
- 包含语言支持信息
- 适合快速索引和发现

### llms-full.txt (完整版)
- 包含所有 llms.txt 的内容
- **完整的文档内容**(从 MDX 文件中提取)
- **完整的示例内容**(从 MDX 文件中提取)
- 自动移除 frontmatter,保留纯内容
- 包含元数据信息
- 适合 LLM 训练、上下文学习和深度分析

## 技术实现

### 文件结构
```
app/
├── llms-txt/
│   └── route.ts          # llms.txt 路由处理
├── llms-full-txt/
│   └── route.ts          # llms-full.txt 路由处理
middleware.ts             # URL 重写中间件
```

### 核心特性

1. **动态生成**: 内容实时从文档源生成,始终保持最新
2. **URL 重写**: 通过 middleware 将 `.txt` 路径重写到实际路由
3. **内容提取**: 直接读取 MDX 源文件,提供真实的文档内容
4. **缓存优化**:
   - llms.txt: 1小时缓存
   - llms-full.txt: 30分钟缓存
5. **国际化支持**: 自动包含所有语言版本的文档

### 实现原理

#### Middleware (middleware.ts)
```typescript
// 将 /llms.txt 重写为 /llms-txt
// 将 /llms-full.txt 重写为 /llms-full-txt
```

#### 路由处理
- 使用 fumadocs 的 source API 获取页面列表
- 使用 Node.js fs API 读取原始 MDX 文件内容
- 自动移除 frontmatter,保留纯 Markdown 内容
- 设置正确的 Content-Type 和缓存头

## 环境变量配置

在 `.env.local` 或生产环境中设置:

```bash
# 生产环境 URL (可选,默认为 localhost:3000)
NEXT_PUBLIC_BASE_URL=https://your-domain.com
```

## 符合规范

本实现遵循 llmstxt.org 规范:
- ✅ 纯文本格式
- ✅ 结构化内容
- ✅ 清晰的目录结构
- ✅ 完整的 URL 链接
- ✅ 元数据信息
- ✅ 可被 LLM 轻松解析

## 测试

### 本地测试
```bash
# 启动开发服务器
pnpm dev

# 测试简洁版
curl http://localhost:3000/llms.txt

# 测试完整版
curl http://localhost:3000/llms-full.txt
```

### 生产测试
```bash
# 构建
pnpm build

# 启动生产服务器
pnpm start

# 测试端点
curl https://your-domain.com/llms.txt
curl https://your-domain.com/llms-full.txt
```

## 维护说明

### 自动更新
- 文档内容更新后自动生效(动态生成)
- 无需手动维护文件

### 缓存清除
如需立即看到更新:
1. 等待缓存过期(llms.txt: 1小时, llms-full.txt: 30分钟)
2. 或清除 CDN 缓存(如果使用 CDN)
3. 或重启服务器

### 自定义
需要修改内容格式或结构时:
- 编辑 `app/llms-txt/route.ts` (简洁版)
- 编辑 `app/llms-full-txt/route.ts` (完整版)

## 性能考虑

### llms.txt
- 轻量级,快速响应
- 适合频繁访问
- 1小时缓存

### llms-full.txt
- 包含完整内容,响应可能较大
- 读取多个文件系统文件
- 30分钟缓存
- 建议通过 CDN 分发

## 用途

### 对 LLM 的价值
1. **快速索引**: llms.txt 提供文档结构概览
2. **深度学习**: llms-full.txt 提供完整训练数据
3. **上下文理解**: 帮助 LLM 理解项目文档结构
4. **准确回答**: 提供最新的文档内容供参考

### 对开发者的价值
1. **SEO 优化**: 结构化内容有助于搜索引擎理解
2. **API 文档**: 可作为文档 API 端点使用
3. **自动化**: 支持自动化工具和脚本访问
4. **兼容性**: 纯文本格式,通用性强

## 相关链接

- [llmstxt.org 规范](https://llmstxt.org/)
- [Fumadocs 文档](https://fumadocs.dev/)
- [Next.js 文档](https://nextjs.org/docs)

---

生成时间: 2025-10-27
版本: 1.0.0
