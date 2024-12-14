"""
Scrapes websites in markdown format. Using crawl4ai. 
Doesn't work for all website, specially those with good robot protection.

Ideally would have used firecrawl but API has rate limits on free tier. Don't wanna add 1 minute sleep after every scrape. 
"""

import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode 

headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache"
}

async def markdown_scrape(url):
    async with AsyncWebCrawler(
                            # user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                            # headers=headers
                            ) as crawler:
        result = await crawler.arun(
            url=url,
            # cache_mode=CacheMode.BYPASS,
            magic=True,
            # delay_before_return_html=2.0,    
            # excluded_tags=['form', 'header', 'footer'],
            # keep_data_attributes=False,
            # include_links_on_markdown=False,
            # simulate_user=True,        # Enables human-like behavior
            # override_navigator=True 
        )
    scrape_success = result.success
    print(result.success)
    # print(type(result))
    return result.markdown, scrape_success



# Testing Modules
async def runf():
    r, scrape_success = await markdown_scrape("https://www.firecrawl.dev/")
    # print(r)
    return r, scrape_success
    
if __name__=='__main__':
    r = asyncio.run( runf())
# async def test()
# url = "https://www.joveo.com"
# loop = asyncio.get_event_loop()
# result = loop.run_until_complete(markdown_scrape(url))
# print(result)

