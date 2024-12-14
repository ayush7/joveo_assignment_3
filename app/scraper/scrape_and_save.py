from scraper import markdown_scraper, save_scraped_page


def scrape_and_save_page(url, save_scraped_page_dir="scraped_pages", database_file_name = ""):
    scraped_markdown = markdown_scraper.markdown_scrape(url)
    saved_db, saved_path = save_scraped_page.save_markdown(url, 
                                                           scraped_markdown, 
                                                           directory=save_scraped_page_dir, 
                                                           database_file_name=database_file_name
                                                           )
    
    return saved_db, saved_path