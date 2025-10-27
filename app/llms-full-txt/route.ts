import fs from 'node:fs/promises'
import path from 'node:path'
import process from 'node:process'
import { NextResponse } from 'next/server'
import { docSource, examplesSource } from '@/lib/source'

/**
 * llms-full.txt - Complete version with full content
 * Provides full documentation content for LLM training and context
 * Spec: https://llmstxt.org/
 *
 * Access via: /llms-full-txt (will be rewritten to /llms-full.txt via middleware)
 */
export async function GET() {
  const docs = docSource.getPages()
  const examples = examplesSource.getPages()

  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'

  let content = `# Oxygent Documentation - Full Content

> Oxygent is a powerful AI agent framework for building intelligent applications

## Table of Contents

### Documentation
${docs.map((doc: any, idx: number) => `${idx + 1}. ${doc.data.title} - ${baseUrl}/docs/${doc.slugs.join('/')}`).join('\n')}

### Examples
${examples.map((example: any, idx: number) => `${idx + 1}. ${example.data.title} - ${baseUrl}/examples/${example.slugs.join('/')}`).join('\n')}

---

`

  // Add full documentation content
  content += '## Full Documentation Content\n\n'

  for (const doc of docs) {
    const url = `${baseUrl}/docs/${doc.slugs.join('/')}`

    content += `### ${doc.data.title}\n\n`
    content += `URL: ${url}\n`

    if (doc.data.description) {
      content += `Description: ${doc.data.description}\n`
    }

    content += '\n'

    // Try to read the actual MDX file content
    try {
      const filePath = path.join(process.cwd(), 'content/docs', `${doc.file.path}`)
      const fileContent = await fs.readFile(filePath, 'utf-8')

      // Remove frontmatter
      const contentWithoutFrontmatter = fileContent.replace(/^---[\s\S]*?---\n/, '')
      content += `${contentWithoutFrontmatter}\n\n`
    } catch {
      // Fallback to description if file reading fails
      if (doc.data.description) {
        content += `${doc.data.description}\n\n`
      }
    }

    content += '---\n\n'
  }

  // Add examples content
  content += '## Examples\n\n'

  for (const example of examples) {
    const url = `${baseUrl}/examples/${example.slugs.join('/')}`

    content += `### ${example.data.title}\n\n`
    content += `URL: ${url}\n`

    if (example.data.description) {
      content += `Description: ${example.data.description}\n`
    }

    content += '\n'

    // Try to read the actual MDX file content
    try {
      const filePath = path.join(process.cwd(), 'content/examples', `${example.file.path}`)
      const fileContent = await fs.readFile(filePath, 'utf-8')

      // Remove frontmatter
      const contentWithoutFrontmatter = fileContent.replace(/^---[\s\S]*?---\n/, '')
      content += `${contentWithoutFrontmatter}\n\n`
    } catch {
      // Fallback to description if file reading fails
      if (example.data.description) {
        content += `${example.data.description}\n\n`
      }
    }

    content += '---\n\n'
  }

  // Add metadata
  content += `
## Metadata

- Generated: ${new Date().toISOString()}
- Total Documentation Pages: ${docs.length}
- Total Examples: ${examples.length}
- Languages: English (en), Chinese Simplified (zh-CN)
- Framework: Oxygent AI Agent Framework
- Documentation Engine: Fumadocs

## Additional Information

For the latest updates and changes, please visit the main website.
For API documentation, visit: ${baseUrl}/api-docs
For ecosystem information, visit: ${baseUrl}/ecosystem

---
End of document
`

  return new NextResponse(content, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=1800, s-maxage=1800', // 30 minutes cache
    },
  })
}
