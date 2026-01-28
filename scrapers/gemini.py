from bs4 import BeautifulSoup
from .base import BaseScraper
from loguru import logger

class GeminiScraper(BaseScraper):
    async def scrape_share_link(self, url):
        # AI Studio 加载较慢，我们多等一会儿
        html = await self.fetch_html(url, wait_selector="div[role='article']")
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        extracted_data = []

        # Google AI Studio 的分享页通常把对话放在 role='article' 的 div 里
        # 或者寻找包含 'user-query' 和 'model-response' 特征的容器
        messages = soup.find_all('div', role='article')

        for msg in messages:
            # 1. 尝试判定角色
            # 这里的逻辑：查看容器内部是否包含特定的图标或文本提示
            text_content = msg.get_text(separator="\n").strip()
            
            # 简单的启发式判定：Gemini 的分享页通常 User 在上，Model 在下
            # 或者寻找具体的 CSS 特征。
            # 注意：Google 喜欢把 Markdown 渲染在 class 包含 'markdown' 的 div 里
            md_div = msg.find(class_=lambda x: x and 'markdown' in x.lower())
            content = md_div.get_text(separator="\n").strip() if md_div else text_content

            # 角色判定补丁：AI Studio 分享页通常可以通过容器的层级关系识别
            # 这里我们通过内容预判，稍后在 Analyser 中让 Gemini 二次修正
            role = "Assistant" if len(content) > 100 else "User" # 初始假设，Analyser 会纠正
            
            if content:
                extracted_data.append({"role": role, "content": content})

        # 如果还是抓不到，采用“全文抓取”兜底方案
        if not extracted_data:
            logger.warning("Gemini 结构化抓取失败，改用全文兜底")
            return [{"role": "System_Raw", "content": soup.get_text()}]
            
        return extracted_data