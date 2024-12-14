from crawler import links_finder
from scraper import markdown_scraper
from rag import build_db


def get_links(url):
    
    return

def filter_links():
    # Do later
    return

def parse_links_dict():
    return 


def scraper_pages():
    # Scape pages
    # Save pages db
    
    return


def rag_pages():
    return


def run_career_app(url):
    unfiltered_links = get_links(url)
    parsed_links = list(parse_links_dict(unfiltered_links))
    scrape_pages = scraper_pages(parsed_links)
    print(scrape_pages)
    
    
    return
    