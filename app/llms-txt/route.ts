import process from 'node:process'
import { NextResponse } from 'next/server'
import { docSource, examplesSource } from '@/lib/source'

/**
 * llms.txt - Compact version for LLM discovery
 * Provides a structured overview of the documentation site
 * Spec: https://llmstxt.org/
 *
 * Access via: /llms-txt (will be rewritten to /llms.txt via middleware)
 */
export async function GET() {
  const docs = docSource.getPages()
  const examples = examplesSource.getPages()

  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'

  const content = `# Oxygent Documentation

> Oxygent is a powerful AI agent framework for building intelligent applications

## Overview

This documentation provides comprehensive guides and examples for using Oxygent framework.

## Main Sections

### Documentation
${docs.map(doc => `- ${doc.data.title}: ${baseUrl}/docs/${doc.slugs.join('/')}`).join('\n')}

### Examples
${examples.map(example => `- ${example.data.title}: ${baseUrl}/examples/${example.slugs.join('/')}`).join('\n')}

## Additional Resources

- Full Documentation: ${baseUrl}/llms-full.txt
- API Documentation: ${baseUrl}/api-docs
- Ecosystem: ${baseUrl}/ecosystem

## Languages

This documentation is available in:
- English (en)
- Chinese Simplified (zh-CN)

## Getting Started

To get started with Oxygent, visit: ${baseUrl}/docs/quick-start

---
Generated: ${new Date().toISOString()}
`

  return new NextResponse(content, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, s-maxage=3600',
    },
  })
}
