import process from 'node:process'
import { createMDX } from 'fumadocs-mdx/next'

const withMDX = createMDX()

// 获取 basePath，用于 GitHub Pages 部署
// GitHub Pages URL: https://karlsbeard.github.io/oxygent-doc-website/
// 如果部署在自定义域名（如 https://oxygent.com），则设置 NEXT_PUBLIC_BASE_PATH=''
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || '/oxygent-doc-website'

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,

  // 静态导出，用于 GitHub Pages 部署
  output: 'export',

  // GitHub Pages 部署路径配置
  basePath,
  assetPrefix: basePath,

  // 禁用图片优化，因为静态导出不支持
  images: {
    unoptimized: true,
  },

  // 为 GitHub Pages 添加尾部斜杠
  trailingSlash: true,
}

export default withMDX(config)
