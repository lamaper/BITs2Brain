#!/bin/bash

# BITs2Brain 快速安装脚本
# 适用环境: Ubuntu/Debian/WSL

echo "🚀 开始安装 BITs2Brain - CTF 知识库自动化流水线..."

# 1. 检查 Python 环境
if ! command -v python3 &> /dev/null
then
    echo "❌ 错误: 未找到 python3，请先安装 Python 3.10+。"
    exit
fi

# 2. 创建虚拟环境
echo "[*] 正在创建虚拟环境 (venv)..."
python3 -m venv venv
source venv/bin/activate

# 3. 升级 pip 并安装依赖
echo "[*] 正在安装 Python 依赖库 (这可能需要 1-2 分钟)..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. 安装 Playwright 浏览器内核
echo "[*] 正在安装 Playwright 浏览器内核..."
playwright install chromium

# 5. 初始化 .env 文件
if [ ! -f .env ]; then
    echo "[*] 正在创建 .env 模板，请稍后记得填写 API Key。"
    echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
    echo "OPENAI_API_KEY=your_deepseek_api_key_here" >> .env
    echo "OPENAI_API_BASE=https://api.deepseek.com" >> .env
fi

echo "------------------------------------------------"
echo "✅ 安装成功！"
echo "使用说明:"
echo "1. 执行 'source venv/bin/activate' 激活环境"
echo "2. 编辑 '.env' 文件填入你的 API Key"
echo "3. 执行 'python main.py' 开始抓取和归档"
echo "------------------------------------------------"