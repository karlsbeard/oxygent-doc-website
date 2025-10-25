# syntax=docker.io/docker/dockerfile:1

# OxyGent Documentation - Docker Build
# 基于 Next.js 官方 Dockerfile 并针对 Fumadocs MDX 优化

FROM node:22-alpine AS base

# ========================================
# Stage 1: 安装依赖
# ========================================
FROM base AS deps

# 安装 libc6-compat 以兼容某些 Node.js 原生模块
RUN apk add --no-cache libc6-compat

WORKDIR /app

# 启用 corepack 以使用 pnpm
RUN corepack enable pnpm

# 复制依赖配置文件
# 重要：source.config.ts 是 Fumadocs MDX 必需的配置文件
COPY package.json pnpm-lock.yaml source.config.ts ./

# 安装生产依赖
RUN pnpm install --frozen-lockfile --prod=false

# ========================================
# Stage 2: 构建应用
# ========================================
FROM base AS builder

WORKDIR /app

# 启用 corepack
RUN corepack enable pnpm

# 从 deps 阶段复制 node_modules
COPY --from=deps /app/node_modules ./node_modules

# 复制所有源代码
COPY . .

# 设置环境变量
# DOCKER_OUTPUT=true: 使用 standalone 输出模式
# NEXT_TELEMETRY_DISABLED: 禁用 Next.js 遥测（可选）
ENV DOCKER_OUTPUT=true
ENV NEXT_TELEMETRY_DISABLED=1

# 构建应用
RUN pnpm run build

# ========================================
# Stage 3: 生产运行时
# ========================================
FROM base AS runner

WORKDIR /app

# 设置生产环境
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# 创建非 root 用户
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# 复制公共资源
COPY --from=builder /app/public ./public

# 复制 standalone 构建输出
# Next.js standalone 模式会生成一个自包含的应用
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# 切换到非 root 用户
USER nextjs

# 暴露端口
EXPOSE 3000

# 设置端口和主机
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# 启动应用
# standalone 模式生成的 server.js 是应用的入口点
CMD ["node", "server.js"]
