import asyncio
import json
from scrapers.deepseek import DeepSeekScraper
from loguru import logger

async def main():
    # 替换为你实际拿到的 DeepSeek 分享链接
    test_url = "https://chat.deepseek.com/share/njz71ovecfzgd3112k" 
    
    scraper = DeepSeekScraper()
    logger.info("开始提取 DeepSeek 对话...")
    
    result = await scraper.scrape_share_link(test_url)
    
    if result:
        logger.success(f"成功提取到 {len(result)} 条对话！")
        
        # 简单展示结果
        for entry in result:
            print(f"\n【{entry['role']}】:\n{entry['content'][:100]}...") # 只显示前100字
            
        # 保存为本地文件，方便后续喂给 AI 处理层
        output_file = "raw_dialogue.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info(f"原始数据已保存至: {output_file}")
    else:
        logger.error("抓取结果为空，请检查链接或网络状态。")

if __name__ == "__main__":
    asyncio.run(main())