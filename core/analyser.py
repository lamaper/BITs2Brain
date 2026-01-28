import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class CTFAnalyser:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-3-flash-preview",
            temperature=0.1,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def _build_prompt(self) -> str:
        return """
        你是一个 CTF 领域的专家和高级知识库管理员。你的任务是分析一段用户与 AI 关于 CTF 题目的对话记录。

        ### 你的目标：
        1. **识别题目信息**：题目名字、类别（Web/Pwn/Reverse/Crypto/Misc）、涉及的技术栈。
        2. **梳理逻辑**：核心思路、关键步骤。
        3. **知识剥离（最重要）**：
           - 对话中是否提到了通用的、可复用的技巧？（例如：IDA Pro 快捷键、特定的 Python 库用法、特殊的 Linux 命令）。
           - 将这些“通用技巧”与“具体题目逻辑”分开，单独归类。
        注意：输入的对话记录可能包含 AI 的‘深度思考（Thinking Process）’，请将其视为 AI 回复的一部分。如果发现原本应该是‘User’的字段里包含了 AI 的自我解析（例如‘我想一下...’），请在分析时自动将其纠正为 AI 的思考，并重点提取真正的用户提问。
        ### 必须返回的 JSON 格式（不要包含任何解释文字）：
        {{
            "metadata": {{
                "title": "题目名称或对话核心主题",
                "category": "Web/Pwn/Reverse/Crypto/Misc",
                "tags": ["标签1", "标签2"]
            }},
            "analysis": {{
                "key_points": ["考点1", "考点2"],
                "solution_summary": "解题核心逻辑总结",
                "vulnerability_type": "漏洞类型(如 CVE 编号, SSRF, Heap Overflow)"
            }},
            "general_knowledge": [
                {{
                    "topic": "知识点标题(如：IDA Pro 搜索字符串技巧)",
                    "content": "具体的知识描述或操作步骤",
                    "tags": ["工具名", "分类"]
                }}
            ]
        }}

        ### 原始对话内容：
        {chat_content}
        """

    async def analyse_file(self, file_path):
        if not os.path.exists(file_path): return None

        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        chat_content = "\n".join([f"{m['role']}: {m['content']}" for m in raw_data])
        
        prompt = PromptTemplate.from_template(self._build_prompt())
        chain = prompt | self.llm

        logger.info("[*] 正在利用 Gemini 分析对话并提取知识点...")
        
        try:
            response = await chain.ainvoke({"chat_content": chat_content})
            
            # --- 关键修复：兼容处理列表类型的 content ---
            content = response.content
            if isinstance(content, list):
                # 如果是列表，把里面所有的文本块拼起来
                content = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
            
            # 提取 JSON 并清洗 Markdown 标签
            clean_text = content.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            logger.error(f"[X] 分析失败: {e}")
            return None