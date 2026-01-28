# from bs4 import BeautifulSoup
# from .base import BaseScraper
# from loguru import logger

# class DeepSeekScraper(BaseScraper):
#     async def scrape_share_link(self, url):
#         html = await self.fetch_html(url)
#         if not html:
#             return None
        
#         soup = BeautifulSoup(html, 'html.parser')
#         extracted_data = []

#         # 寻找所有消息容器
#         all_messages = soup.find_all('div', class_=lambda x: x and 'message' in x.lower())

#         for msg in all_messages:
#             # 关键修复：将 class 列表转为字符串再处理
#             class_names = msg.get('class', [])
#             class_str = " ".join(class_names).lower()
            
#             role = "Unknown"
#             content = ""
            
#             if 'user' in class_str:
#                 role = "User"
#                 content_node = msg.find(class_="ds-markdown")
#                 content = content_node.get_text(separator="\n").strip() if content_node else msg.get_text().strip()
            
#             elif 'assistant' in class_str:
#                 role = "Assistant"
#                 # 分离深度思考和最终答案
#                 thought_node = msg.find(class_=lambda x: x and 'thought' in x.lower())
#                 answer_node = msg.find(class_="ds-markdown")
                
#                 parts = []
#                 if thought_node:
#                     parts.append(f"[Thought]\n{thought_node.get_text(separator='\n').strip()}\n[/Thought]")
#                 if answer_node:
#                     parts.append(answer_node.get_text(separator="\n").strip())
                
#                 content = "\n\n".join(parts)

#             if content and role != "Unknown":
#                 extracted_data.append({"role": role, "content": content})
            
#         return extracted_data

from bs4 import BeautifulSoup
from .base import BaseScraper
from loguru import logger

class DeepSeekScraper(BaseScraper):
    async def scrape_share_link(self, url):
        html = await self.fetch_html(url)
        if not html: return None
        
        # 调试：把抓到的 HTML 存下来看看
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # 放弃复杂的类名判断，改用更通用的逻辑
        # 只要是包含长文本的 div 且不在 header/footer 里，我们先全拿出来
        # 然后让 Gemini 去分辨谁是 User，谁是 Assistant
        
        raw_text = soup.get_text(separator="\n")
        
        # 如果你发现 raw_text 里确实有对话内容
        # 我们可以构造一个简单的列表回传，把识别任务全交给分析器
        if "DeepSeek" in raw_text or "IDA" in raw_text:
            return [{"role": "System_Raw", "content": raw_text}]
        
        return None