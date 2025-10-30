import { createTokenizer } from '@orama/tokenizers/mandarin'
import { createFromSource } from 'fumadocs-core/search/server'
import { docSource, examplesSource, oxyapiSource } from '@/lib/source'

function mergeSources(sources: any[]) {
  return sources.reduce((acc, source) => {
    return {
      ...acc,
      ...source,
    }
  }, {})
}

export const { GET } = createFromSource(mergeSources([docSource, examplesSource, oxyapiSource]), {
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
