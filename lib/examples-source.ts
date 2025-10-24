import { loader } from 'fumadocs-core/source'
import { examples } from '@/.source'
import { i18n } from './i18n'

// Examples source configuration
export const examplesSource = loader({
  baseUrl: '/examples',
  source: examples.toFumadocsSource(),
  i18n,
})
