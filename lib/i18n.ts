import type { Translations } from 'fumadocs-ui/i18n'
import { defineI18n } from 'fumadocs-core/i18n'

export const i18n = defineI18n({
  defaultLanguage: 'en-US',
  languages: ['en-US', 'zh-CN'],
  hideLocale: 'always',
})

// translations
export const zhCN: (Partial<Translations> & {
  displayName?: string
}) = {
  displayName: '简体中文',
  search: '搜索',
  searchNoResult: '没有找到相关内容',
  toc: '目录',
  tocNoHeadings: '没有可用的目录',
  lastUpdate: '最后更新',
  chooseLanguage: '选择语言',
  nextPage: '下一页',
  previousPage: '上一页',
  chooseTheme: '选择主题',
  editOnGithub: '在 GitHub 上编辑',
}

export const enUS: typeof zhCN = {
  displayName: 'English',
  search: 'Search',
  searchNoResult: 'No results found',
  toc: 'Table of Contents',
  tocNoHeadings: 'No headings available',
  lastUpdate: 'Last updated',
  chooseLanguage: 'Choose language',
  nextPage: 'Next page',
  previousPage: 'Previous page',
  chooseTheme: 'Choose theme',
  editOnGithub: 'Edit on GitHub',
}

export const translations: Record<string, Partial<Translations>> = {
  'zh-CN': zhCN,
  'en-US': enUS,
}

/**
 * Custom translations for specific components
 */
const customZhCN = {
  'documentation.title': '文档',
  'ecosystem.title': '生态',
  'api.title': 'API',
  'examples.title': '在线演示',
  'home.slogan': '智能代理框架，重新定义AI应用开发',
  'home.description': 'OxyGent 是一个高性能的智能代理框架，专为构建强大的AI应用而设计。',
}

const customEnUS: typeof customZhCN = {
  'documentation.title': 'Documentation',
  'ecosystem.title': 'Ecosystem',
  'api.title': 'API',
  'examples.title': 'Examples',
  'home.slogan': 'Intelligent Agent Framework, Redefining AI Application Development',
  'home.description': 'OxyGent is a high-performance intelligent agent framework designed for building powerful AI applications.',
}

export const customTranslations: Record<string, Record<string, string>> = {
  'zh-CN': customZhCN,
  'en-US': customEnUS,
}
