from bs4 import BeautifulSoup
from .base import BaseScraper
from loguru import logger

class DeepSeekScraper(BaseScraper):
    async def scrape_share_link(self, url):
        # DeepSeek 的对话通常包含在 .ds-markdown 类中
        html = await self.fetch_html(url, wait_selector=".ds-markdown")
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # 寻找所有的消息区块
        # 注意：DeepSeek 的结构通常是交替出现的对话块
        # 2026年最新结构可能是 f-chat-message 或者 ds-markdown 容器
        messages = soup.find_all(class_="ds-markdown")
        
        extracted_data = []
        for i, msg in enumerate(messages):
            role = "User" if i % 2 == 0 else "Assistant"
            text = msg.get_text(separator="\n").strip()
            extracted_data.append({"role": role, "content": text})
            
        return extracted_data