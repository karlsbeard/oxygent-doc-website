'use client'

import { ArrowRightIcon } from '@radix-ui/react-icons'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { customTranslations } from '@/lib/i18n'

export default function HomePage() {
  const params = useParams()
  const lang = params?.lang as string || 'en-US'
  const currentLang = customTranslations[lang] ? lang : 'en-US'
  const t = customTranslations[currentLang]

  return (
    <main className="flex flex-1 flex-col">
      {/* Hero Section */}
      <section
        className={`
          relative overflow-hidden bg-gradient-to-b from-blue-50 to-white
          dark:from-gray-900 dark:to-gray-800
        `}
      >
        <div
          className={`
            mx-auto max-w-4xl px-6 py-24 text-center
            sm:py-32
          `}
        >
          <h1
            className={`
              mb-6 text-4xl font-bold tracking-tight text-gray-900
              sm:text-6xl
              dark:text-white
            `}
          >
            {t['home.hero.title']}
          </h1>

          <p
            className={`
              mb-8 text-xl text-gray-600
              sm:text-2xl
              dark:text-gray-300
            `}
          >
            {t['home.hero.description']}
          </p>

          <div
            className={`
              flex flex-col items-center justify-center gap-4
              sm:flex-row sm:gap-6
            `}
          >
            <Link
              href={`/${lang}/docs/quick-start`}
              className={`
                inline-flex items-center rounded-lg bg-blue-600 px-6 py-3 text-lg font-semibold text-white shadow-sm
                hover:bg-blue-700
                focus:ring-2 focus:ring-blue-500 focus:outline-none
              `}
            >
              {t['home.hero.getStarted']}
              <ArrowRightIcon className="ml-2 h-5 w-5" />
            </Link>

            <Link
              href={`/${lang}/docs`}
              className={`
                inline-flex items-center rounded-lg border border-gray-300 bg-white px-6 py-3 text-lg font-semibold
                text-gray-700 shadow-sm
                hover:bg-gray-50
                dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700
              `}
            >
              {t['home.hero.viewDocs']}
            </Link>
          </div>
        </div>
      </section>

      {/* Quick Links Section */}
      <section
        className={`
          py-16
          sm:py-24
        `}
      >
        <div className="mx-auto max-w-6xl px-6">
          <div
            className={`
              grid gap-8
              md:grid-cols-2
              lg:grid-cols-3
            `}
          >
            {/* Documentation */}
            <Link
              href={`/${lang}/docs`}
              className={`
                group rounded-lg border border-gray-200 p-6
                hover:border-blue-300 hover:shadow-md
                dark:border-gray-700 dark:hover:border-blue-600
              `}
            >
              <h3
                className={`
                  mb-2 text-lg font-semibold text-gray-900
                  group-hover:text-blue-600
                  dark:text-white dark:group-hover:text-blue-400
                `}
              >
                📚
                {' '}
                {t['documentation.title']}
              </h3>
              <p
                className={`
                  text-gray-600
                  dark:text-gray-300
                `}
              >
                {t['documentation.description']}
              </p>
            </Link>

            {/* API Reference */}
            <Link
              href={`/${lang}/oxyapi`}
              className={`
                group rounded-lg border border-gray-200 p-6
                hover:border-blue-300 hover:shadow-md
                dark:border-gray-700 dark:hover:border-blue-600
              `}
            >
              <h3
                className={`
                  mb-2 text-lg font-semibold text-gray-900
                  group-hover:text-blue-600
                  dark:text-white dark:group-hover:text-blue-400
                `}
              >
                🔧
                {' '}
                {t['oxyapi.title']}
              </h3>
              <p
                className={`
                  text-gray-600
                  dark:text-gray-300
                `}
              >
                {t['oxyapi.description']}
              </p>
            </Link>

            {/* Examples */}
            <Link
              href={`/${lang}/examples`}
              className={`
                group rounded-lg border border-gray-200 p-6
                hover:border-blue-300 hover:shadow-md
                dark:border-gray-700 dark:hover:border-blue-600
              `}
            >
              <h3
                className={`
                  mb-2 text-lg font-semibold text-gray-900
                  group-hover:text-blue-600
                  dark:text-white dark:group-hover:text-blue-400
                `}
              >
                💡
                {' '}
                {t['examples.title']}
              </h3>
              <p
                className={`
                  text-gray-600
                  dark:text-gray-300
                `}
              >
                {t['examples.description']}
              </p>
            </Link>
          </div>
        </div>
      </section>
    </main>
  )
}
