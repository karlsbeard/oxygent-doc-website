import { createTokenizer } from '@orama/tokenizers/mandarin'
import { createFromSource } from 'fumadocs-core/search/server'
import { source } from '@/lib/source'

// Static mode for GitHub Pages
// staticGET 在开发模式下动态生成索引，生产构建时生成静态文件
export const revalidate = false

export const { staticGET: GET } = createFromSource(source, {
  localeMap: {
    'zh-CN': {
      components: {
        tokenizer: createTokenizer(),
      },
      search: {
        threshold: 0,
        tolerance: 0,
      },
    },
    'en-US': {
      language: 'english',
    },
  },
})
