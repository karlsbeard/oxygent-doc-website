import { createTokenizer } from '@orama/tokenizers/mandarin'
import { createFromSource } from 'fumadocs-core/search/server'
import { source } from '@/lib/source'

export const { GET } = createFromSource(source, {
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
