import type { MDXComponents } from 'mdx/types'
import { createGenerator } from 'fumadocs-typescript'
import { AutoTypeTable } from 'fumadocs-typescript/ui'
import { Step, Steps } from 'fumadocs-ui/components/steps'
import { Tab, Tabs } from 'fumadocs-ui/components/tabs'
import defaultMdxComponents from 'fumadocs-ui/mdx'

const generator = createGenerator()

// use this function to get MDX components, you will need it for rendering MDX
export function getMDXComponents(components?: MDXComponents): MDXComponents {
  return {
    ...defaultMdxComponents,
    ...components,
    Tabs,
    Tab,
    Steps,
    Step,
    AutoTypeTable: props => (
      <AutoTypeTable
        class="hidden"
        {...props}
        generator={generator}
      />
    ),
  }
}
