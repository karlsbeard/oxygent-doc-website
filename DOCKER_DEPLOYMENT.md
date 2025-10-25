# Docker 部署指南

完整的 OxyGent 文档网站 Docker 部署方案。

## 📋 目录

- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [部署方式对比](#部署方式对比)
- [常见问题](#常见问题)

---

## 🚀 快速开始

### 方式 1: 使用 Docker Compose（推荐）

```bash
# 1. 构建镜像
pnpm docker:build

# 2. 启动容器
pnpm docker:up

# 3. 访问应用
open http://localhost:3000

# 4. 查看日志
pnpm docker:logs

# 5. 停止容器
pnpm docker:down
```

### 方式 2: 使用 Docker CLI

```bash
# 1. 构建镜像
docker build -t oxygent-docs:latest .

# 2. 运行容器
docker run -d \
  --name oxygent-docs \
  -p 3000:3000 \
  oxygent-docs:latest

# 3. 访问应用
open http://localhost:3000

# 4. 查看日志
docker logs -f oxygent-docs

# 5. 停止容器
docker stop oxygent-docs
docker rm oxygent-docs
```

---

## ⚙️ 配置说明

### 环境变量

Docker 部署支持以下环境变量：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `NODE_ENV` | `production` | Node.js 运行环境 |
| `PORT` | `3000` | 应用监听端口 |
| `NEXT_PUBLIC_BASE_PATH` | `''`（空） | 应用基础路径 |
| `DOCKER_OUTPUT` | `true` | 使用 standalone 输出模式 |

#### 自定义 basePath

如果需要部署到子路径（如 `/docs`），设置环境变量：

**docker-compose.yml:**
```yaml
services:
  web:
    environment:
      - NEXT_PUBLIC_BASE_PATH=/docs
```

**Docker CLI:**
```bash
docker run -d \
  -p 3000:3000 \
  -e NEXT_PUBLIC_BASE_PATH=/docs \
  oxygent-docs:latest
```

---

## 🏗️ 构建过程

### 多阶段构建说明

Dockerfile 使用 **多阶段构建** 优化镜像大小：

#### Stage 1: deps（依赖安装）
```dockerfile
FROM node:22-alpine AS deps
RUN corepack enable pnpm
COPY package.json pnpm-lock.yaml source.config.ts ./
RUN pnpm install --frozen-lockfile
```

**作用：** 安装所有依赖，包括 `source.config.ts`（Fumadocs MDX 必需）

#### Stage 2: builder（应用构建）
```dockerfile
FROM base AS builder
ENV DOCKER_OUTPUT=true
RUN pnpm run build
```

**作用：** 使用 `standalone` 模式构建应用，生成自包含的 `server.js`

#### Stage 3: runner（生产运行）
```dockerfile
FROM base AS runner
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
CMD ["node", "server.js"]
```

**作用：** 仅复制必要文件到最终镜像，大幅减小镜像体积

---

## 📦 部署方式对比

### GitHub Pages vs Docker

| 维度 | GitHub Pages | Docker |
|------|-------------|--------|
| **部署模式** | 静态文件（`output: 'export'`） | Node.js 服务器（`output: 'standalone'`） |
| **成本** | 🆓 完全免费 | 💰 需要服务器 |
| **性能** | ⚡⚡⚡ 极快（全球 CDN） | ⚡⚡ 快（取决于服务器） |
| **动态功能** | ❌ 不支持 | ✅ 支持 API 路由、SSR |
| **扩展性** | ⭐ 有限 | ⭐⭐⭐ 高 |
| **维护成本** | ⭐ 低 | ⭐⭐ 中等 |
| **适用场景** | 纯文档站点 | 需要后端功能的应用 |

**推荐：**
- ✅ **文档站点** → GitHub Pages（当前项目最佳选择）
- ✅ **动态应用** → Docker 部署

---

## 🔧 高级配置

### 自定义端口

#### docker-compose.yml
```yaml
services:
  web:
    ports:
      - "8080:3000"  # 主机端口:容器端口
    environment:
      - PORT=3000
```

#### Docker CLI
```bash
docker run -d -p 8080:3000 oxygent-docs:latest
```

访问：`http://localhost:8080`

### 使用自定义域名

#### 方式 1: Nginx 反向代理

```nginx
server {
    listen 80;
    server_name docs.example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 方式 2: Traefik (Docker)

```yaml
version: '3.8'

services:
  web:
    image: oxygent-docs:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.docs.rule=Host(`docs.example.com`)"
      - "traefik.http.services.docs.loadbalancer.server.port=3000"
    networks:
      - web

networks:
  web:
    external: true
```

### 持久化日志

```yaml
services:
  web:
    volumes:
      - ./logs:/app/logs
```

### 资源限制

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

---

## 🐳 生产部署最佳实践

### 1. 使用特定版本标签

```bash
# 不推荐
docker build -t oxygent-docs:latest .

# 推荐
docker build -t oxygent-docs:1.0.0 .
docker tag oxygent-docs:1.0.0 oxygent-docs:latest
```

### 2. 健康检查

```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 3. 自动重启

```yaml
services:
  web:
    restart: unless-stopped
```

### 4. 日志管理

```yaml
services:
  web:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## ❓ 常见问题

### Q1: Docker 构建失败，找不到 `source.config.ts`？

**原因：** Fumadocs MDX 需要 `source.config.ts` 文件在构建时可用。

**解决方案：** Dockerfile 已经包含此文件复制，确保文件存在：
```bash
ls source.config.ts
```

### Q2: 容器启动后无法访问？

**排查步骤：**
```bash
# 1. 检查容器状态
docker ps

# 2. 查看容器日志
docker logs oxygent-docs

# 3. 检查端口映射
docker port oxygent-docs

# 4. 测试容器内部
docker exec -it oxygent-docs sh
wget -O- http://localhost:3000
```

### Q3: 镜像体积过大？

**当前优化：**
- ✅ 多阶段构建
- ✅ Alpine Linux 基础镜像
- ✅ `.dockerignore` 排除不必要文件

**预期大小：** ~150-200 MB（取决于依赖）

**进一步优化：**
```dockerfile
# 使用 distroless 镜像（高级）
FROM gcr.io/distroless/nodejs22-debian11
COPY --from=builder /app/.next/standalone ./
CMD ["server.js"]
```

### Q4: 如何更新应用？

```bash
# 1. 停止旧容器
pnpm docker:down

# 2. 重新构建镜像
pnpm docker:build

# 3. 启动新容器
pnpm docker:up
```

### Q5: Docker vs GitHub Pages，如何选择？

| 场景 | 推荐方案 |
|------|----------|
| 纯文档站点，无后端需求 | ✅ GitHub Pages |
| 需要 API 路由、服务端渲染 | ✅ Docker |
| 需要私有化部署 | ✅ Docker |
| 需要全球 CDN 加速 | ✅ GitHub Pages |
| 预算有限 | ✅ GitHub Pages（免费） |

---

## 📚 相关命令速查

### Docker Compose

```bash
# 构建镜像
pnpm docker:build
# or
docker-compose build

# 启动容器（后台）
pnpm docker:up
# or
docker-compose up -d

# 停止并删除容器
pnpm docker:down
# or
docker-compose down

# 查看日志
pnpm docker:logs
# or
docker-compose logs -f

# 重启服务
pnpm docker:restart
# or
docker-compose restart

# 进入容器
docker-compose exec web sh
```

### Docker CLI

```bash
# 构建镜像
docker build -t oxygent-docs:latest .

# 运行容器
docker run -d -p 3000:3000 --name oxygent-docs oxygent-docs:latest

# 停止容器
docker stop oxygent-docs

# 删除容器
docker rm oxygent-docs

# 删除镜像
docker rmi oxygent-docs:latest

# 查看日志
docker logs -f oxygent-docs

# 进入容器
docker exec -it oxygent-docs sh
```

---

## 🔗 相关资源

- [Next.js Docker 官方文档](https://nextjs.org/docs/app/building-your-application/deploying/docker)
- [Fumadocs 部署指南](https://fumadocs.vercel.app/docs/ui/deploying)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [Docker 多阶段构建](https://docs.docker.com/build/building/multi-stage/)

---

**创建日期**: 2025-10-25
**部署模式**: Docker Standalone
**状态**: ✅ 已配置并测试
