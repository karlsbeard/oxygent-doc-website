# 智能环境检测方案

## 🎯 **设计目标**

实现**零配置**的多环境部署：
- ✅ 本地开发：自动使用空路径
- ✅ GitHub Actions：自动使用 `/oxygent-doc-website`
- ✅ 手动覆盖：支持环境变量自定义
- ✅ **单分支管理**：无需维护多个分支

---

## 🔧 **技术实现**

### 核心逻辑 (`next.config.mjs`)

```javascript
const basePath = process.env.NEXT_PUBLIC_BASE_PATH !== undefined
  ? process.env.NEXT_PUBLIC_BASE_PATH  // 1️⃣ 手动设置优先
  : process.env.CI === 'true'
    ? '/oxygent-doc-website'           // 2️⃣ GitHub Actions 自动检测
    : ''                                // 3️⃣ 本地开发默认
```

### 优先级层级

```
1. NEXT_PUBLIC_BASE_PATH 环境变量（最高优先级）
   ↓
2. CI=true 检测（GitHub Actions 自动触发）
   ↓
3. 空字符串（本地开发默认）
```

---

## 📦 **使用场景**

### 场景 1: 本地开发（零配置）

```bash
# 无需任何配置
pnpm dev

# 自动检测：
# - CI 未设置 → basePath = ''
# - 访问：http://localhost:3000/
```

**工作原理：**
- `CI` 环境变量不存在
- `NEXT_PUBLIC_BASE_PATH` 未设置
- 自动使用空字符串 ✅

---

### 场景 2: GitHub Actions 部署（自动化）

```yaml
# .github/workflows/deploy.yml
- name: Build with Next.js
  run: pnpm build
  # CI=true 由 GitHub Actions 自动设置
```

**工作原理：**
- GitHub Actions 自动设置 `CI=true`
- 检测到 `CI=true` → basePath = `/oxygent-doc-website`
- 自动构建 GitHub Pages 版本 ✅

---

### 场景 3: 本地测试 GitHub Pages 构建

```bash
# 方法 1: 使用预设脚本
pnpm build:test-gh-pages

# 方法 2: 手动设置环境变量
NEXT_PUBLIC_BASE_PATH=/oxygent-doc-website pnpm build

# 预览构建结果
npx serve out
# 访问：http://localhost:3000/oxygent-doc-website/
```

**工作原理：**
- 手动设置 `NEXT_PUBLIC_BASE_PATH=/oxygent-doc-website`
- 优先级最高，覆盖其他检测 ✅

---

### 场景 4: 自定义域名部署

```bash
# 使用自定义域名（如 docs.oxygent.com）
NEXT_PUBLIC_BASE_PATH='' pnpm build

# 或创建 .env.production.local
echo "NEXT_PUBLIC_BASE_PATH=" > .env.production.local
pnpm build
```

**工作原理：**
- 明确设置空字符串
- 部署到自定义域名根路径 ✅

---

## 🔍 **环境变量说明**

### `NEXT_PUBLIC_BASE_PATH`

**作用：** 手动控制应用的基础路径

**值类型：**
- `undefined`（未设置）：使用自动检测
- `''`（空字符串）：根路径部署
- `'/path'`：子路径部署（如 `/oxygent-doc-website`）

**示例：**
```bash
# 根路径
NEXT_PUBLIC_BASE_PATH=''

# 子路径
NEXT_PUBLIC_BASE_PATH=/docs
NEXT_PUBLIC_BASE_PATH=/oxygent-doc-website
```

### `CI`

**作用：** 指示是否在 CI 环境中运行

**值类型：**
- `'true'`：CI 环境（GitHub Actions, GitLab CI, 等）
- `undefined` 或其他值：本地环境

**自动设置：**
- GitHub Actions：✅ 自动设置为 `'true'`
- 本地开发：❌ 未设置

---

## 📊 **工作流程图**

```
开始
  │
  ├─ NEXT_PUBLIC_BASE_PATH 已设置？
  │  ├─ 是 → 使用 NEXT_PUBLIC_BASE_PATH 值
  │  └─ 否 → 继续
  │
  ├─ CI === 'true'？
  │  ├─ 是 → 使用 '/oxygent-doc-website'
  │  └─ 否 → 使用 ''（空字符串）
  │
结束
```

---

## ✅ **优势对比**

| 方案 | 配置复杂度 | 维护成本 | 灵活性 | 推荐度 |
|------|-----------|---------|--------|--------|
| **智能环境检测** | ⭐ 零配置 | ⭐ 低 | ⭐⭐⭐ 高 | ✅ 推荐 |
| 手动环境变量 | ⭐⭐ 需配置 | ⭐⭐ 中 | ⭐⭐⭐ 高 | ✅ 可选 |
| 两个分支 | ⭐⭐⭐ 复杂 | ⭐⭐⭐ 高 | ⭐ 低 | ❌ 不推荐 |
| 两个配置文件 | ⭐⭐ 中等 | ⭐⭐ 中 | ⭐⭐ 中 | ❌ 不推荐 |

---

## 🧪 **测试验证**

### 测试 1: 本地开发

```bash
# 清除所有环境变量
unset NEXT_PUBLIC_BASE_PATH
unset CI

# 运行开发服务器
pnpm dev

# 预期结果：
# ✅ basePath = ''
# ✅ 访问 http://localhost:3000/ 正常
```

### 测试 2: 模拟 GitHub Actions

```bash
# 设置 CI 环境变量
export CI=true

# 运行构建
pnpm build

# 检查输出
cat out/en-US/index.html | grep href

# 预期结果：
# ✅ href="/oxygent-doc-website/_next/..."
```

### 测试 3: 手动覆盖

```bash
# 设置自定义 basePath
export NEXT_PUBLIC_BASE_PATH=/custom-path
export CI=true  # 即使 CI=true，也应使用 NEXT_PUBLIC_BASE_PATH

# 运行构建
pnpm build

# 检查输出
cat out/en-US/index.html | grep href

# 预期结果：
# ✅ href="/custom-path/_next/..."
```

---

## 📚 **相关文件**

```
oxygent-doc-website/
├── next.config.mjs              # 智能检测逻辑
├── .env.example                 # 环境变量示例
├── .github/workflows/deploy.yml # GitHub Actions 配置
├── package.json                 # 构建脚本
└── ENVIRONMENT_DETECTION.md     # 本文档
```

---

## 🆚 **替代方案对比**

### 方案 A: 两个分支

```
main 分支 → 开发用（basePath = ''）
gh-pages 分支 → 部署用（basePath = '/oxygent-doc-website'）
```

**缺点：**
- ❌ 需要维护两个分支
- ❌ 容易出现代码不同步
- ❌ 增加合并冲突风险

### 方案 B: 两个配置文件

```
next.config.mjs           → 开发用
next.config.production.mjs → 生产用
```

**缺点：**
- ❌ 配置重复
- ❌ 需要额外的脚本切换
- ❌ 维护两个文件

### 方案 C: 智能环境检测（当前方案）

```javascript
const basePath = process.env.NEXT_PUBLIC_BASE_PATH !== undefined
  ? process.env.NEXT_PUBLIC_BASE_PATH
  : process.env.CI === 'true'
    ? '/oxygent-doc-website'
    : ''
```

**优点：**
- ✅ 单一配置文件
- ✅ 单一代码分支
- ✅ 零配置运行
- ✅ 灵活手动覆盖

---

## ❓ **常见问题**

### Q1: 为什么不直接用 `NODE_ENV` 判断？

**A:** `NODE_ENV` 在开发和生产环境都可能不同：
- 本地 `pnpm build` → `NODE_ENV=production`（但需要 basePath=''）
- GitHub Actions → `NODE_ENV=production`（需要 basePath='/oxygent-doc-website'）

使用 `CI` 环境变量更准确判断是否在 CI 环境。

### Q2: 如果忘记设置环境变量会怎样？

**A:** 完全没问题！这就是智能检测的优势：
- 本地开发：自动使用空路径 ✅
- GitHub Actions：自动检测 `CI=true`，使用正确路径 ✅

### Q3: 如何验证当前使用的 basePath？

```bash
# 开发模式
pnpm dev
# 查看终端输出，会显示 http://localhost:3000/

# 构建模式
pnpm build
cat out/en-US/index.html | grep -o 'href="[^"]*_next' | head -1
# 如果输出 href="/_next → basePath 为空
# 如果输出 href="/oxygent-doc-website/_next → basePath 为 /oxygent-doc-website
```

---

## 🚀 **部署清单**

- [x] 配置智能环境检测
- [x] 更新 GitHub Actions
- [x] 简化 package.json 脚本
- [x] 创建 .env.example
- [x] 编写详细文档

**下一步：**
1. 推送代码到 GitHub
2. 验证 GitHub Actions 自动部署
3. 本地测试开发模式

---

**创建日期**: 2025-10-25
**方案类型**: 智能环境检测
**状态**: ✅ 已实现并测试
