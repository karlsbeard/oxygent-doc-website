# 脚本工具

本目录包含用于文档翻译和维护的 Python 脚本。

## 📝 脚本列表

### 翻译相关

- **translate_script.py** - 批量翻译主脚本
  - 翻译 19 个 .zh-CN.mdx 文件
  - 处理标题、描述和说明文本

- **translate_remaining.py** - 处理遗漏的翻译
  - 修复特定文件的翻译问题
  - 处理 8 个文件

- **check_chinese.py** - 质量检查脚本
  - 检查未翻译的英文内容
  - 生成检查报告

- **final_translate.py** - 生成统计报告
  - 统计翻译数量
  - 生成完成报告

- **clean_all_chinese.py** - 最终质量验证
  - 全面检查翻译质量
  - 生成验证报告

## 🚀 使用方法

### 翻译工作流

```bash
# 1. 批量翻译
python scripts/translate_script.py

# 2. 处理遗漏
python scripts/translate_remaining.py

# 3. 质量检查
python scripts/check_chinese.py

# 4. 生成报告
python scripts/final_translate.py

# 5. 最终验证
python scripts/clean_all_chinese.py
```

### 单独运行

```bash
# 进入脚本目录
cd scripts

# 运行特定脚本
python translate_script.py
```

## 📊 翻译统计

- **处理文件数**: 24 个
- **代码块数**: 23 个
- **中文注释数**: 56 条
- **翻译覆盖率**: 100%

## ⚙️ 翻译原则

1. **代码保持英文**: 所有 Python 代码保持英文
2. **注释使用中文**: 代码注释全部中文化
3. **说明文档中文化**: 标题、描述、正文全部中文

## 📝 注意事项

- 脚本使用 Python 3.10+
- 需要确保文件路径正确
- 运行前备份重要文件
- 所有脚本已被 ESLint 忽略

## 🔗 相关文档

- [翻译报告](../docs/reports/TRANSLATION_REPORT.md)
- [索引更新报告](../docs/reports/INDEX_UPDATE_REPORT.md)

---

**脚本位置**: `/scripts/`
**最后更新**: 2025-10-24
