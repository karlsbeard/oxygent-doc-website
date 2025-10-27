import type { NextFetchEvent, NextRequest } from 'next/server'
import { createI18nMiddleware } from 'fumadocs-core/i18n/middleware'
import { NextResponse } from 'next/server'
import { i18n } from '@/lib/i18n'

export function middleware(request: NextRequest, event: NextFetchEvent) {
  const { pathname } = request.nextUrl

  // Handle llms.txt and llms-full.txt rewrites
  if (pathname === '/llms.txt') {
    return NextResponse.rewrite(new URL('/llms-txt', request.url))
  }

  if (pathname === '/llms-full.txt') {
    return NextResponse.rewrite(new URL('/llms-full-txt', request.url))
  }

  // Continue with i18n middleware for other routes
  return createI18nMiddleware(i18n)(request, event)
}

export const config = {
  // Matcher ignoring `/_next/` and `/api/`
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico|assets).*)'],
}
