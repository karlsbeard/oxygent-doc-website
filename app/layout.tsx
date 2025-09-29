import type { ReactNode } from 'react'
import { Inter } from 'next/font/google'
import '@/app/global.css'

const inter = Inter({
  subsets: ['latin'],
})

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <html className={inter.className} suppressHydrationWarning>
      <body className="flex min-h-screen flex-col">
        {children}
      </body>
    </html>
  )
}
