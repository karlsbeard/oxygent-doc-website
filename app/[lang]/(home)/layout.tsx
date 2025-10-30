import type { LinkItemType } from 'fumadocs-ui/layouts/links'
import type { ReactNode } from 'react'
import { HomeLayout } from 'fumadocs-ui/layouts/home'
import {
  NavbarMenu,
  NavbarMenuTrigger,
} from 'fumadocs-ui/layouts/home/navbar'
import Link from 'next/link'
import { baseOptions } from '@/app/layout.config'
import { customTranslations } from '@/lib/i18n'

interface IProps {
  params: Promise<{ lang: string }>
  children: ReactNode
}

export default async function Layout({ params, children }: IProps) {
  const { lang } = await params

  // Ensure lang exists in customTranslations, fallback to default
  const currentLang = customTranslations[lang] ? lang : 'en-US'

  // const documentationLinks = [{
  //   text: '快速开始',
  //   url: `/${lang}/docs`,
  //   icon: <BookTextIcon />,
  //   iconClassName: 'bg-gradient-to-br from-blue-500 to-blue-600',
  // }, {
  //   text: '核心概念',
  //   url: `/${lang}/docs/test`,
  //   icon: <LayersIcon />,
  //   iconClassName: 'bg-gradient-to-br from-green-500 to-green-600',
  // }, {
  //   text: '开发指南',
  //   url: `/${lang}/docs/guide`,
  //   icon: <CookingPotIcon />,
  //   iconClassName: 'bg-gradient-to-br from-purple-500 to-purple-600',
  // }]

  const oxyapiLinks = [{
    text: '🔧 开发工具',
    url: `/${lang}/oxyapi`,
  }]

  const links: LinkItemType[] = [
    {
      type: 'custom',
      on: 'nav',
      children: (
        <NavbarMenu>
          <NavbarMenuTrigger asChild>
            <Link href={`/${lang}/docs`}>
              {customTranslations[currentLang]['documentation.title']}
            </Link>
          </NavbarMenuTrigger>
          {/* <NavbarMenuContent className="text-sm">
            {documentationLinks.map(link => (
              <NavbarMenuLink
                key={link.url}
                className="border-none"
                href={link.url}
              >
                <div className="flex flex-col">
                  <div
                    className={`
                      mb-2 flex size-6 items-center justify-center rounded text-white
                      [&>*]:size-4
                      ${link.iconClassName}
                    `}
                  >
                    {link.icon}
                  </div>
                  <div className="font-medium">{link.text}</div>
                </div>
              </NavbarMenuLink>
            ))}
          </NavbarMenuContent> */}
        </NavbarMenu>
      ),
    },
    {
      text: customTranslations[currentLang]['oxyapi.title'],
      url: `/${lang}/oxyapi`,
    },
    {
      text: customTranslations[currentLang]['examples.title'],
      url: `/${lang}/examples`,
    },
  ]

  return (
    <HomeLayout
      className="min-h-screen"
      {...baseOptions(lang)}
      links={links}
    >
      {children}
    </HomeLayout>
  )
}
