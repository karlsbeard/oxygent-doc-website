// import process from 'node:process'
import { createMDX } from 'fumadocs-mdx/next'

const withMDX = createMDX()

// 获取 basePath，用于 GitHub Pages 部署
// 如果你的仓库名是 oxygent-doc-website，并且部署在 https://username.github.io/oxygent-doc-website/
// 则需要设置 basePath: '/oxygent-doc-website'
// 如果部署在根域名（如 https://oxygent.com），则保持为空字符串
// 变量名以 _ 开头表示有意未使用（取消注释下面的 basePath 配置时会用到）
// const _basePath = process.env.NEXT_PUBLIC_BASE_PATH || ''

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,

  // 静态导出，用于 GitHub Pages
  output: 'export',

  // 如果需要 basePath，取消下面的注释（需要重命名 _basePath 为 basePath）
  // basePath: _basePath,
  // assetPrefix: _basePath,

  // 禁用图片优化，因为 GitHub Pages 不支持
  images: {
    unoptimized: true,
  },

  // 可选：为 GitHub Pages 添加尾部斜杠
  trailingSlash: true,
}

export default withMDX(config)
