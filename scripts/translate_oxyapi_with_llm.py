#!/usr/bin/env python3
"""
使用大模型翻译 oxyapi 文档中的英文内容
保持代码块不变，只翻译英文段落
"""

import os
import re
import sys
from pathlib import Path

# 尝试导入 OpenAI
try:
    from openai import OpenAI
except ImportError:
    print("❌ 错误: 未安装 openai 库")
    print("   请运行: pip install openai")
    sys.exit(1)

# 初始化 OpenAI 客户端（延迟初始化）
client = None

def extract_code_blocks(content):
    """提取代码块，返回内容和代码块映射"""
    code_blocks = []
    placeholder_pattern = "<<<CODE_BLOCK_{}>>>"
    
    # 匹配代码块 ```...```
    def replace_code_block(match):
        idx = len(code_blocks)
        code_blocks.append(match.group(0))
        return placeholder_pattern.format(idx)
    
    # 替换代码块为占位符
    content_without_code = re.sub(
        r'```[\s\S]*?```',
        replace_code_block,
        content,
        flags=re.MULTILINE
    )
    
    return content_without_code, code_blocks

def restore_code_blocks(content, code_blocks):
    """恢复代码块"""
    for idx, code_block in enumerate(code_blocks):
        placeholder = f"<<<CODE_BLOCK_{idx}>>>"
        content = content.replace(placeholder, code_block)
    return content

def split_into_chunks(content, max_chars=8000):
    """将内容分割成块，按段落分割"""
    # 按双换行符分割段落
    paragraphs = re.split(r'\n\n+', content)
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for para in paragraphs:
        para_length = len(para)
        
        if current_length + para_length > max_chars and current_chunk:
            # 当前块已满，保存并开始新块
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_length = para_length
        else:
            current_chunk.append(para)
            current_length += para_length + 2  # +2 for \n\n
    
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks

def translate_chunk(chunk, file_name):
    """使用大模型翻译一个文本块"""
    prompt = f"""你是一个专业的技术文档翻译专家。请将下面的英文内容翻译成简体中文。

翻译要求：
1. 这是 OxyGent 框架的 API 参考文档（文件名：{file_name}）
2. 保持技术术语的准确性（如 Agent、Tool、MCP、SSE 等可以不翻译）
3. 保持 Markdown 格式不变
4. 保持表格格式不变
5. 保持占位符格式不变（如 <<<CODE_BLOCK_0>>>）
6. 如果遇到已经是中文的内容，保持不变
7. 翻译要自然流畅，符合中文技术文档的表达习惯
8. frontmatter（---之间的内容）不要翻译
9. 保持专业术语的一致性

请直接返回翻译后的内容，不要添加任何解释。

原文：
{chunk}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一个专业的技术文档翻译专家，擅长将英文技术文档翻译成简体中文。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        translated = response.choices[0].message.content.strip()
        return translated
    
    except Exception as e:
        print(f"❌ 翻译出错: {e}")
        return chunk  # 出错时返回原文

def translate_file(file_path):
    """翻译单个文件"""
    print(f"\n{'='*80}")
    print(f"📄 处理文件: {file_path.name}")
    print(f"{'='*80}")
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        main_content = frontmatter_match.group(2)
    else:
        frontmatter = None
        main_content = content
    
    # 提取代码块
    print("📦 提取代码块...")
    content_without_code, code_blocks = extract_code_blocks(main_content)
    print(f"   找到 {len(code_blocks)} 个代码块")
    
    # 分割成块
    print("✂️  分割内容...")
    chunks = split_into_chunks(content_without_code)
    print(f"   分割成 {len(chunks)} 个块")
    
    # 翻译每个块
    translated_chunks = []
    for i, chunk in enumerate(chunks, 1):
        print(f"🌐 翻译块 {i}/{len(chunks)}...")
        translated = translate_chunk(chunk, file_path.name)
        translated_chunks.append(translated)
        print(f"   ✅ 完成 ({len(translated)} 字符)")
    
    # 合并翻译结果
    print("🔗 合并翻译结果...")
    translated_content = '\n\n'.join(translated_chunks)
    
    # 恢复代码块
    print("📦 恢复代码块...")
    final_content = restore_code_blocks(translated_content, code_blocks)
    
    # 恢复 frontmatter
    if frontmatter:
        final_content = f"---\n{frontmatter}\n---\n{final_content}"
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"✅ 文件翻译完成: {file_path.name}")
    print(f"   原始大小: {len(content)} 字符")
    print(f"   翻译后: {len(final_content)} 字符")

def get_api_key():
    """获取 API Key"""
    # 1. 从环境变量获取
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    # 2. 从 .env 文件获取
    env_file = Path.home() / ".openai_api_key"
    if env_file.exists():
        with open(env_file, 'r') as f:
            api_key = f.read().strip()
            if api_key:
                return api_key
    
    # 3. 从项目根目录的 .env 文件获取
    project_env = Path(__file__).parent.parent / ".env"
    if project_env.exists():
        with open(project_env, 'r') as f:
            for line in f:
                if line.startswith("OPENAI_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if api_key:
                        return api_key
    
    return None

def main():
    """主函数"""
    global client
    
    # 要翻译的文件列表
    files_to_translate = [
        "content/oxyapi/tools-function-hub-api.zh-CN.mdx",
        "content/oxyapi/tools-mcp-stdio-api.zh-CN.mdx",
        "content/oxyapi/tools-mcp-sse-api.zh-CN.mdx",
        "content/oxyapi/tools-mcp-streamable-api.zh-CN.mdx",
    ]
    
    base_dir = Path(__file__).parent.parent
    
    print("🚀 开始翻译 OxyAPI 文档")
    print(f"📂 基础目录: {base_dir}")
    
    # 获取 API Key
    api_key = get_api_key()
    if not api_key:
        print("❌ 错误: 未找到 OPENAI_API_KEY")
        print("   请使用以下任一方式设置:")
        print("   1. 环境变量: export OPENAI_API_KEY='your-api-key'")
        print("   2. 创建文件: ~/.openai_api_key")
        print("   3. 在项目根目录创建 .env 文件，添加 OPENAI_API_KEY=your-api-key")
        return
    
    # 初始化客户端
    print("🔑 初始化 OpenAI 客户端...")
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        print(f"❌ 初始化客户端失败: {e}")
        return
    
    # 翻译每个文件
    for file_rel_path in files_to_translate:
        file_path = base_dir / file_rel_path
        
        if not file_path.exists():
            print(f"⚠️  文件不存在: {file_path}")
            continue
        
        try:
            translate_file(file_path)
        except Exception as e:
            print(f"❌ 处理文件出错 {file_path.name}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("🎉 所有文件翻译完成！")
    print("="*80)

if __name__ == "__main__":
    main()

