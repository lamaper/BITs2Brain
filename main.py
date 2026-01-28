import asyncio
import json
from scrapers.deepseek import DeepSeekScraper
from scrapers.gemini import GeminiScraper  # 新增
from core.analyser import CTFAnalyser
from core.archiver import CTFArchiver
from loguru import logger

async def process_ctf_link(url: str):
    # 1. 路由分配
    if "deepseek.com" in url:
        scraper = DeepSeekScraper()
    elif "google.com" in url or "aistudio" in url:
        scraper = GeminiScraper()
    else:
        logger.error(f"暂不支持该平台: {url}")
        return

    # 2. 抓取原始数据
    raw_data = await scraper.scrape_share_link(url)
    if not raw_data: 
        logger.error(f"无法从该链接获取内容: {url}")
        return

    # 3. 保存临时文件供分析
    temp_raw = "temp_raw.json"
    with open(temp_raw, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False)
        
    # 4. AI 语义分析
    analyser = CTFAnalyser()
    structured_result = await analyser.analyse_file(temp_raw)
    
    if not structured_result:
        logger.error("AI 分析失败，可能是抓取的内容不包含有效的对话。")
        return

    # 5. 归档 (这里现在匹配了上面新增的 archive_data)
    archiver = CTFArchiver()
    final_path = archiver.archive_data(structured_result)
    
    if final_path:
        logger.success(f"🎉 归档成功: {final_path}")
    else:
        logger.error("归档失败。")

async def main():
    urls = [
        "https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221AVkc4dc5ES2tNMPQW9sEyrFwzICs1cBg%22%5D,%22action%22:%22open%22,%22userId%22:%22105912647283914331320%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing"
    ]
    
    for url in urls:
        await process_ctf_link(url)

if __name__ == "__main__":
    asyncio.run(main())