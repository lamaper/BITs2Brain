# 🧠 BITs2Brain (B2B)

**基于 LLM 驱动的 CTF 战队自动化知识复盘与归档平台**

> 让 AI 替你整理 Writeups，把散落在聊天记录里的 Flag 逻辑和 IDA 技巧一网打尽。

---

## 🌟 核心功能

- **多平台收割**：自动爬取并解析 DeepSeek、Tencent 元宝、Gemini (Google AI Studio) 的分享链接。
- **语义级剥离**：利用 Gemini 1.5 Pro 的超长上下文能力，自动识别并提取对话中的：
  - **题目档案**：名称、分类、核心解题思路。
  - **通用技巧**：独立提取 IDA Pro 操作、特定脚本用法、常用命令等可复用知识。
- **结构化归档**：自动生成美观的 Markdown 文件，并按 CTF 类别（Web/Pwn/Reverse...）自动建档。
- **智能去噪**：自动识别并剔除 AI 的“深度思考”碎碎念，只留干货。

---

## 🛠️ 技术栈

- **爬虫层**: Playwright (Headless Chrome) + BeautifulSoup4
- **大脑层**: Gemini 1.5 Pro (Google AI Studio API)
- **存储层**: 结构化 Markdown 文件系统 (未来支持向量数据库)
- **后端**: Python 3.12 + LangChain

---

## 🚀 快速开始

### 1. 克隆与安装
```bash
git clone [https://github.com/your-repo/BITs2Brain.git](https://github.com/your-repo/BITs2Brain.git)
cd BITs2Brain
chmod +x setup.sh
./setup.sh
```

2. 配置密钥

编辑项目根目录下的 .env 文件：
```env
GOOGLE_API_KEY=你的Gemini密钥
```
3. 一键运行
```Bash
source venv/bin/activate
python main.py
```
## 📂 项目结构
```Plaintext
.
├── core/               # 核心逻辑 (分析器、归档器)
├── scrapers/           # 各平台爬虫 (DeepSeek, Gemini等)
├── knowledge_base/     # 自动生成的 Markdown 知识库
├── main.py             # 全流水线运行入口
└── requirements.txt    # 依赖清单
```

## 📝 TODO

    [ ] 接入向量数据库 (ChromaDB) 实现语义查重与合并

    [ ] 支持上传题目附件与截图自动分析

    [ ] 战队 Wiki 页面前端展示


---
