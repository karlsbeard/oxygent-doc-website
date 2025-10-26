'use client'

import type { SharedProps } from 'fumadocs-ui/components/dialog/search'
import { create } from '@orama/orama'
import { useDocsSearch } from 'fumadocs-core/search/client'
import {
  SearchDialog,
  SearchDialogClose,
  SearchDialogContent,
  SearchDialogHeader,
  SearchDialogIcon,
  SearchDialogInput,
  SearchDialogList,
  SearchDialogOverlay,
} from 'fumadocs-ui/components/dialog/search'
import { useI18n } from 'fumadocs-ui/contexts/i18n'

// 初始化 Orama 实例（服务端已配置 tokenizer，客户端只需基础配置）
function initOrama() {
  return create({
    schema: { _: 'string' },
  })
}

export default function CustomSearchDialog(props: SharedProps) {
  const { locale } = useI18n()

  const { search, setSearch, query } = useDocsSearch({
    type: 'static',
    initOrama: initOrama as any,
    locale,
  })

  return (
    <SearchDialog
      search={search}
      onSearchChange={setSearch}
      isLoading={query.isLoading}
      {...props}
    >
      <SearchDialogOverlay />
      <SearchDialogContent>
        <SearchDialogHeader>
          <SearchDialogIcon />
          <SearchDialogInput />
          <SearchDialogClose />
        </SearchDialogHeader>
        <SearchDialogList items={query.data !== 'empty' ? query.data : null} />
      </SearchDialogContent>
    </SearchDialog>
  )
}
