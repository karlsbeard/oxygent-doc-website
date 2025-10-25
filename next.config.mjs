import process from 'node:process'
import { createMDX } from 'fumadocs-mdx/next'

const withMDX = createMDX()

/**
 * 智能 basePath 配置
 *
 * 自动检测部署环境：
 * 1. GitHub Actions (CI=true) → 自动使用 /oxygent-doc-website
 * 2. 本地开发 → 自动使用空字符串
 * 3. 手动覆盖 → NEXT_PUBLIC_BASE_PATH 环境变量优先
 *
 * 使用示例：
 * - 本地开发：pnpm dev (自动检测)
 * - 本地测试 GitHub Pages：NEXT_PUBLIC_BASE_PATH=/oxygent-doc-website pnpm build
 * - GitHub Actions：自动使用正确路径
 * - 自定义域名：NEXT_PUBLIC_BASE_PATH='' pnpm build
 */
const basePath = process.env.NEXT_PUBLIC_BASE_PATH !== undefined
  ? process.env.NEXT_PUBLIC_BASE_PATH // 手动设置优先
  : process.env.CI === 'true'
    ? '/oxygent-doc-website' // GitHub Actions 自动检测
    : '' // 本地开发默认

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,

  // 输出配置
  // Docker 部署: output = 'standalone'（生成 server.js）
  // GitHub Pages: output = 'export'（生成静态文件）
  // 开发模式: 默认（无需配置）
  ...(process.env.DOCKER_OUTPUT === 'true'
    ? {
        output: 'standalone', // Docker 使用 standalone 模式
      }
    : process.env.NODE_ENV === 'production'
      ? {
          output: 'export', // GitHub Pages 使用静态导出
        }
      : {}),

  // 部署路径配置（仅在设置了 basePath 时应用）
  ...(basePath && {
    basePath,
    assetPrefix: basePath,
  }),

  // 图片优化配置
  images: {
    unoptimized: true, // 静态导出不支持优化
  },

  // URL 配置
  trailingSlash: true,
}

export default withMDX(config)
