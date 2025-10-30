import { loader } from 'fumadocs-core/source'
import { docs, examples, oxyapi } from '@/.source'
import { i18n } from './i18n'

// See https://fumadocs.vercel.app/docs/headless/source-api for more info
export const docSource = loader({
  // it assigns a URL to your pages
  baseUrl: '/docs',
  source: docs.toFumadocsSource(),
  i18n,
})

export const examplesSource = loader({
  baseUrl: '/examples',
  source: examples.toFumadocsSource(),
  i18n,
})

export const oxyapiSource = loader({
  baseUrl: '/oxyapi',
  source: oxyapi.toFumadocsSource(),
  i18n,
})
