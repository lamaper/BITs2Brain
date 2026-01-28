import os
import json
from datetime import datetime
from loguru import logger

class CTFArchiver:
    def __init__(self, base_path="knowledge_base"):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def _format_to_markdown(self, data):
        """将结构化 JSON 转换为美观的 Markdown"""
        metadata = data.get('metadata', {})
        analysis = data.get('analysis', {})
        general = data.get('general_knowledge', [])

        md = f"# {metadata.get('title', '未命名题目')}\n\n"
        md += f"- **类别**: {metadata.get('category', 'Misc')}\n"
        md += f"- **标签**: {', '.join(metadata.get('tags', []))}\n"
        md += f"- **归档时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

        md += "## 🚩 题目分析\n"
        md += f"> **核心思路**: {analysis.get('solution_summary', '无')}\n\n"
        md += "### 考点点拨\n"
        for point in analysis.get('key_points', []):
            md += f"- {point}\n"
        md += "\n"

        if general:
            md += "## 💡 提取的通用知识点\n"
            for item in general:
                md += f"### 📌 {item.get('topic')}\n"
                md += f"{item.get('content')}\n"
                if item.get('tags'):
                    md += f"\n*Tags: {', '.join(item.get('tags'))}*\n"
                md += "\n---\n"
        
        return md

    def archive_data(self, data):
        """核心方法：直接接收字典数据并保存为 Markdown"""
        if not data:
            logger.error("没有数据可供归档")
            return None

        metadata = data.get('metadata', {})
        category = metadata.get('category', 'Misc')
        title = metadata.get('title', 'untitled').replace("/", "-").replace("\\", "-")
        
        # 1. 创建分类目录
        category_path = os.path.join(self.base_path, category)
        os.makedirs(category_path, exist_ok=True)

        # 2. 生成 Markdown
        md_content = self._format_to_markdown(data)
        
        # 3. 写入文件
        file_path = os.path.join(category_path, f"{title}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        return file_path

    def archive_file(self, json_path):
        """兼容方法：从 JSON 文件读取并归档"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return self.archive_data(data)