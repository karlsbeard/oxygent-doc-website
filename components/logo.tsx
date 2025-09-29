'use client'

import type { SVGProps } from 'react'

export function Logo(props: SVGProps<SVGSVGElement>) {
  return (
    <div className="flex items-center gap-2">
      <svg
        width="32"
        height="32"
        viewBox="0 0 32 32"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        {...props}
      >
        <defs>
          <linearGradient id="oxygent-gradient" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse">
            <stop stopColor="#0048FF" />
            <stop offset="0.5" stopColor="#0C81ED" />
            <stop offset="1" stopColor="#00C5A8" />
          </linearGradient>
        </defs>
        <rect width="32" height="32" rx="8" fill="url(#oxygent-gradient)" />
        <path
          d="M8 12C8 10.8954 8.89543 10 10 10H14C15.1046 10 16 10.8954 16 12V20C16 21.1046 15.1046 22 14 22H10C8.89543 22 8 21.1046 8 20V12Z"
          fill="white"
          fillOpacity="0.9"
        />
        <path
          d="M18 8C18 6.89543 18.8954 6 20 6H24C25.1046 6 26 6.89543 26 8V24C26 25.1046 25.1046 26 24 26H20C18.8954 26 18 25.1046 18 24V8Z"
          fill="white"
          fillOpacity="0.7"
        />
      </svg>
      <span className="text-foreground text-xl font-semibold">OxyGent</span>
    </div>
  )
}
