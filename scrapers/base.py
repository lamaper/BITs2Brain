import asyncio
# 关键：必须显式从 async_api 导入 async_playwright
from playwright.async_api import async_playwright
from playwright_stealth import Stealth 
from loguru import logger

class BaseScraper:
    async def get_browser_context(self, playwright):
        # 启动 Chromium，并添加一些基础反爬参数
        browser = await playwright.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        # 创建一个更真实的浏览器上下文
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        return browser, context

    async def fetch_html(self, url, wait_selector=None):
        # 使用 async with 确保 playwright 实例正确开启和关闭
        async with async_playwright() as p:
            browser, context = await self.get_browser_context(p)
            page = await context.new_page()
            
            # 2026 最新版调用方式：创建 Stealth 实例并应用
            stealth = Stealth()
            await stealth.apply_stealth_async(page)
            
            logger.info(f"[*] 正在尝试抓取链接: {url}")
            try:
                # 增加超时容错
                await page.goto(url, wait_until="networkidle", timeout=60000)
                
                if wait_selector:
                    try:
                        # 等待内容渲染
                        await page.wait_for_selector(wait_selector, timeout=15000)
                    except Exception:
                        logger.warning(f"[!] 选择器 {wait_selector} 超时，将尝试直接提取当前内容")
                
                # 模拟真人阅读，等待 JS 彻底跑完
                await asyncio.sleep(2)
                content = await page.content()
                await browser.close()
                return content
            except Exception as e:
                logger.error(f"[X] 抓取过程中发生错误: {e}")
                await browser.close()
                return None