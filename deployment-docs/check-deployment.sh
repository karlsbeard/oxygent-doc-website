#!/bin/bash

# GitHub Pages 部署配置检查脚本

echo "======================================"
echo "GitHub Pages 部署配置检查"
echo "======================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查计数
PASS=0
FAIL=0
WARN=0

# 检查函数
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗${NC} $2"
        ((FAIL++))
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗${NC} $2"
        ((FAIL++))
        return 1
    fi
}

check_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $3"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗${NC} $3"
        ((FAIL++))
        return 1
    fi
}

echo "1️⃣  检查必需文件..."
echo "-----------------------------------"
check_file "package.json" "package.json 存在"
check_file "next.config.mjs" "next.config.mjs 存在"
check_file ".github/workflows/deploy.yml" "GitHub Actions workflow 存在"
check_file "public/.nojekyll" ".nojekyll 文件存在"
echo ""

echo "2️⃣  检查 Next.js 配置..."
echo "-----------------------------------"
check_content "next.config.mjs" "output: 'export'" "静态导出已配置"
check_content "next.config.mjs" "unoptimized: true" "图片优化已禁用"
echo ""

echo "3️⃣  检查包管理器..."
echo "-----------------------------------"
if [ -f "pnpm-lock.yaml" ]; then
    echo -e "${GREEN}✓${NC} 使用 pnpm（推荐）"
    ((PASS++))

    # 检查 pnpm 是否安装
    if command -v pnpm &> /dev/null; then
        echo -e "${GREEN}✓${NC} pnpm 已安装"
        ((PASS++))
    else
        echo -e "${YELLOW}⚠${NC} pnpm 未安装，请运行: npm install -g pnpm"
        ((WARN++))
    fi
else
    echo -e "${YELLOW}⚠${NC} 未找到 pnpm-lock.yaml，建议使用 pnpm"
    ((WARN++))
fi
echo ""

echo "4️⃣  检查 Node.js 版本..."
echo "-----------------------------------"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -ge 22 ]; then
        echo -e "${GREEN}✓${NC} Node.js 版本符合要求 (v$(node -v | cut -d'v' -f2))"
        ((PASS++))
    else
        echo -e "${RED}✗${NC} Node.js 版本过低 (需要 >= 22，当前: v$(node -v | cut -d'v' -f2))"
        ((FAIL++))
    fi
else
    echo -e "${RED}✗${NC} Node.js 未安装"
    ((FAIL++))
fi
echo ""

echo "5️⃣  检查 Git 配置..."
echo "-----------------------------------"
if [ -d ".git" ]; then
    echo -e "${GREEN}✓${NC} Git 仓库已初始化"
    ((PASS++))

    # 检查是否有远程仓库
    if git remote -v | grep -q "github.com"; then
        echo -e "${GREEN}✓${NC} GitHub 远程仓库已配置"
        ((PASS++))

        # 显示远程仓库地址
        REMOTE_URL=$(git remote get-url origin 2>/dev/null)
        if [ -n "$REMOTE_URL" ]; then
            echo -e "   远程仓库: ${YELLOW}$REMOTE_URL${NC}"
        fi
    else
        echo -e "${RED}✗${NC} 未配置 GitHub 远程仓库"
        ((FAIL++))
    fi
else
    echo -e "${RED}✗${NC} Git 仓库未初始化"
    ((FAIL++))
fi
echo ""

echo "6️⃣  检查构建配置..."
echo "-----------------------------------"
check_content "package.json" '"build": "next build"' "构建脚本已配置"

# 检查是否有 out 目录（之前的构建）
if [ -d "out" ]; then
    echo -e "${YELLOW}⚠${NC} 检测到 out 目录（之前的构建），建议添加到 .gitignore"
    ((WARN++))
fi
echo ""

echo "======================================"
echo "检查结果汇总"
echo "======================================"
echo -e "${GREEN}通过${NC}: $PASS"
echo -e "${RED}失败${NC}: $FAIL"
echo -e "${YELLOW}警告${NC}: $WARN"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✅ 配置检查通过！可以开始部署。${NC}"
    echo ""
    echo "📝 下一步："
    echo "1. 确保代码已推送到 GitHub"
    echo "2. 在 GitHub 仓库设置中启用 GitHub Pages (Source: GitHub Actions)"
    echo "3. 推送代码或手动触发 workflow"
    echo ""
    echo "运行以下命令推送代码："
    echo "  git add ."
    echo "  git commit -m \"Configure GitHub Pages deployment\""
    echo "  git push origin main"
    exit 0
else
    echo -e "${RED}❌ 配置检查发现问题，请修复后再部署。${NC}"
    echo ""
    echo "📝 修复建议："
    echo "- 检查上述标记为 ✗ 的项目"
    echo "- 参考 DEPLOYMENT.md 文档"
    echo "- 确保所有必需文件都已创建"
    exit 1
fi
