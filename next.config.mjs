import process from 'node:process'
import { createMDX } from 'fumadocs-mdx/next'

const withMDX = createMDX()

/**
 * Next.js 配置
 *
 * 部署方案：
 * 1. Vercel（推荐）：默认配置，自动优化
 * 2. Docker：设置 DOCKER_OUTPUT=true 使用 standalone 模式
 * 3. 本地开发：默认开发模式
 */

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,

  // Docker 部署专用配置
  // 仅当明确指定 DOCKER_OUTPUT=true 时才使用 standalone 模式
  ...(process.env.DOCKER_OUTPUT === 'true' && {
    output: 'standalone',
  }),

  // 图片优化配置
  // Vercel 自动处理图片优化
  // Docker standalone 模式需要 unoptimized
  images: {
    unoptimized: process.env.DOCKER_OUTPUT === 'true',
  },
}

export default withMDX(config)
