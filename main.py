import asyncio
import json
from scrapers.deepseek import DeepSeekScraper
from core.analyser import CTFAnalyser
from loguru import logger

async def main():
    test_url = "https://chat.deepseek.com/share/njz71ovecfzgd3112k" 
    
    # 1. 抓取环节
    scraper = DeepSeekScraper()
    raw_data = await scraper.scrape_share_link(test_url)
    
    if not raw_data:
        logger.error("抓取失败，请检查网络或链接。")
        return

    # 保存原始数据
    with open("raw_dialogue.json", "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
    logger.success("第一步：原始对话已抓取。")

    # 2. 分析环节
    analyser = CTFAnalyser()
    structured_result = await analyser.analyse_file("raw_dialogue.json")
    
    if structured_result:
        with open("structured_knowledge.json", "w", encoding="utf-8") as f:
            json.dump(structured_result, f, ensure_ascii=False, indent=4)
        logger.success("第二步：AI 知识提取完成！结果已存入 structured_knowledge.json")
        print("\n=== AI 提取的知识概览 ===")
        print(f"题目: {structured_result['metadata']['title']}")
        print(f"通用知识点数量: {len(structured_result['general_knowledge'])}")
    else:
        logger.error("AI 分析失败。")

if __name__ == "__main__":
    asyncio.run(main())