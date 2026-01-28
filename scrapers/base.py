import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth 
from loguru import logger

class BaseScraper:
    async def get_browser_context(self, playwright):
        # 启动 Chromium，禁用自动化特征
        browser = await playwright.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        return browser, context

    async def fetch_html(self, url, wait_selector=None):
        async with async_playwright() as p:
            browser, context = await self.get_browser_context(p)
            page = await context.new_page()
            
            # 应用最新的 Stealth 配置
            stealth = Stealth()
            await stealth.apply_stealth_async(page)
            
            logger.info(f"[*] 正在尝试抓取: {url}")
            try:
                # 增加到 60s 超时以应对慢速网络
                await page.goto(url, wait_until="networkidle", timeout=60000)
                
                if wait_selector:
                    try:
                        await page.wait_for_selector(wait_selector, timeout=15000)
                    except Exception:
                        logger.warning(f"[!] 等待选择器 {wait_selector} 超时")
                
                await asyncio.sleep(2)
                content = await page.content()
                await browser.close()
                return content
            except Exception as e:
                logger.error(f"[X] 抓取失败: {e}")
                await browser.close()
                return None