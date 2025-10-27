import type { ReactNode } from 'react'
import { DocsLayout } from 'fumadocs-ui/layouts/docs'
import { baseOptions } from '@/app/layout.config'
import { examplesSource } from '@/lib/source'

interface IProps {
  params: Promise<{ lang: string }>
  children: ReactNode
}

export default async function Layout({ params, children }: IProps) {
  const { lang } = await params

  return (
    <DocsLayout
      {...baseOptions(lang)}
      tree={examplesSource.pageTree[lang]}
      sidebar={{
        defaultOpenLevel: 0,
        banner: (
          <div className="rounded-lg bg-gradient-to-r from-blue-500/10 to-purple-500/10 p-4">
            <div className="text-foreground text-sm font-semibold">
              💡 Examples
            </div>
            <div className="text-muted-foreground mt-1 text-xs">
              Explore OxyGent code examples
            </div>
          </div>
        ),
      }}
    >
      {children}
    </DocsLayout>
  )
}
