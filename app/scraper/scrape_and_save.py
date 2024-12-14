"""
Main file used for Scraper Module
"""

from scraper import markdown_scraper, save_scraped_page
import re 

def remove_links(markdown_content):
    """Removes links from markdown text. """
    link_pattern = r'\[([^\]]+)\]\([^\)]+\)'
    return re.sub(link_pattern, r'\1', markdown_content)



async def scrape_and_save_page(url, save_scraped_page_dir=".cache/scraped_data", database_file_name = "scrape_db.json", remove_links=True):
    scraped_markdown = await markdown_scraper.markdown_scrape(url)
    
    if remove_links:
        clean_md = remove_links (scraped_markdown)
    saved_db, saved_path = save_scraped_page.save_markdown(url, 
                                                           clean_md, 
                                                           directory=save_scraped_page_dir, 
                                                           database_file_name=database_file_name
                                                           )
    
    return saved_db, saved_path