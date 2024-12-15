"""
Main file used for Scraper Module
"""

from scraper import markdown_scraper, save_scraped_page
import re 

def remove_links_from_markdown(markdown_content):
    """Removes links from markdown text. """
    link_pattern = r'\[([^\]]+)\]\([^\)]+\)'
    return re.sub(link_pattern, r'\1', markdown_content)



async def scrape_and_save_page(url, page_title = "",save_scraped_page_dir=".cache/scraped_data", database_file_name = "scrape_db.json", remove_links=True, category="others"):
    
    try:
        scraped_markdown, scrape_success = await markdown_scraper.markdown_scrape(url)
    except Exception as e:
        print(f"Exception in scraping {e} : Bad Url : {url}")
    saved_db = None
    saved_path = None 
    if scrape_success:
        if remove_links:
            clean_md = remove_links_from_markdown(scraped_markdown)
        
        try:
            saved_db, saved_path = save_scraped_page.save_markdown(url, 
                                                           clean_md, 
                                                           directory=save_scraped_page_dir, 
                                                           database_file_name=database_file_name,
                                                           category=category, page_title=page_title)
        except Exception as e:
            print(f"Exception in saving page : {e} for {url}")
    
    return saved_db, saved_path, scrape_success