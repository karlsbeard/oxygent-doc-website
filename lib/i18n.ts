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
  'documentation.description': '学习如何使用 OxyGent 构建智能代理应用',
  'oxyapi.title': 'OxyAPI',
  'oxyapi.description': '完整的 API 参考文档和使用指南',
  'examples.title': '在线演示',
  'examples.description': '实际应用示例和最佳实践',
  'home.hero.title': '下一代智能代理框架',
  'home.hero.subtitle': '重新定义AI应用开发',
  'home.hero.description': 'OxyGent 是一个高性能的智能代理框架，专为构建强大的AI应用而设计。支持多代理协作、工具集成和企业级部署。',
  'home.hero.getStarted': '快速开始',
  'home.hero.viewDocs': '查看文档',
  'home.features.title': '核心特性',
  'home.features.subtitle': '为现代AI应用构建而生',
  'home.features.multiAgent.title': '多代理协作',
  'home.features.multiAgent.description': '支持复杂的多代理系统，实现智能协作和任务分配',
  'home.features.toolIntegration.title': '工具集成',
  'home.features.toolIntegration.description': '无缝集成各种工具和API，扩展代理能力',
  'home.features.enterprise.title': '企业级部署',
  'home.features.enterprise.description': '支持大规模部署和高可用性架构',
  'home.features.workflow.title': '智能工作流',
  'home.features.workflow.description': '可视化工作流设计，简化复杂业务逻辑',
  'home.tech.title': '技术亮点',
  'home.tech.performance': '高性能架构',
  'home.tech.scalable': '可扩展设计',
  'home.tech.reliable': '企业级可靠性',
  'home.quickStart.title': '快速开始',
  'home.quickStart.description': '几分钟内构建您的第一个AI代理',
  'home.useCases.title': '企业应用场景',
  'home.useCases.subtitle': '已在多个行业成功应用',
  'home.useCases.automation.title': '业务流程自动化',
  'home.useCases.automation.description': '自动化复杂的业务流程，提高效率',
  'home.useCases.customer.title': '智能客户服务',
  'home.useCases.customer.description': '24/7智能客服，提升用户体验',
  'home.useCases.analysis.title': '数据分析助手',
  'home.useCases.analysis.description': '智能数据分析和洞察生成',
  'home.cta.title': '准备开始了吗？',
  'home.cta.description': '加入数千名开发者，使用OxyGent构建下一代AI应用',
  'home.cta.getStarted': '立即开始',
  'home.cta.github': 'GitHub',
}

const customEnUS: typeof customZhCN = {
  'documentation.title': 'Documentation',
  'documentation.description': 'Learn how to build intelligent agent applications with OxyGent',
  'oxyapi.title': 'OxyAPI',
  'oxyapi.description': 'Complete API reference documentation and usage guide',
  'examples.title': 'Examples',
  'examples.description': 'Real-world examples and best practices',
  'home.hero.title': 'Next-Generation Intelligent Agent Framework',
  'home.hero.subtitle': 'Redefining AI Application Development',
  'home.hero.description': 'OxyGent is a high-performance intelligent agent framework designed for building powerful AI applications. Supporting multi-agent collaboration, tool integration, and enterprise-grade deployment.',
  'home.hero.getStarted': 'Get Started',
  'home.hero.viewDocs': 'View Documentation',
  'home.features.title': 'Core Features',
  'home.features.subtitle': 'Built for modern AI applications',
  'home.features.multiAgent.title': 'Multi-Agent Collaboration',
  'home.features.multiAgent.description': 'Support complex multi-agent systems with intelligent collaboration and task distribution',
  'home.features.toolIntegration.title': 'Tool Integration',
  'home.features.toolIntegration.description': 'Seamlessly integrate various tools and APIs to extend agent capabilities',
  'home.features.enterprise.title': 'Enterprise Deployment',
  'home.features.enterprise.description': 'Support large-scale deployment and high-availability architecture',
  'home.features.workflow.title': 'Intelligent Workflows',
  'home.features.workflow.description': 'Visual workflow design to simplify complex business logic',
  'home.tech.title': 'Technical Highlights',
  'home.tech.performance': 'High-Performance Architecture',
  'home.tech.scalable': 'Scalable Design',
  'home.tech.reliable': 'Enterprise-Grade Reliability',
  'home.quickStart.title': 'Quick Start',
  'home.quickStart.description': 'Build your first AI agent in minutes',
  'home.useCases.title': 'Enterprise Use Cases',
  'home.useCases.subtitle': 'Successfully applied across multiple industries',
  'home.useCases.automation.title': 'Business Process Automation',
  'home.useCases.automation.description': 'Automate complex business processes to improve efficiency',
  'home.useCases.customer.title': 'Intelligent Customer Service',
  'home.useCases.customer.description': '24/7 intelligent customer service to enhance user experience',
  'home.useCases.analysis.title': 'Data Analysis Assistant',
  'home.useCases.analysis.description': 'Intelligent data analysis and insight generation',
  'home.cta.title': 'Ready to Get Started?',
  'home.cta.description': 'Join thousands of developers building next-generation AI applications with OxyGent',
  'home.cta.getStarted': 'Get Started Now',
  'home.cta.github': 'GitHub',
}

export const customTranslations: Record<string, Record<string, string>> = {
  'zh-CN': customZhCN,
  'en-US': customEnUS,
}
