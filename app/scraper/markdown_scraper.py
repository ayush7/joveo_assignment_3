import asyncio
from crawl4ai import AsyncWebCrawler

async def markdown_scrape(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            magic=True,
            excluded_tags=['form', 'header', 'footer'],
            keep_data_attributes=False,
            include_links_on_markdown=False
        )
    return result.markdown_v2

