from crawler import links_finder, links_util
from scraper import scrape_and_save
from rag import build_db
import params 

def get_links(url, allowed_domains = [], depth = 1):
    # Returns file with links saved
    return links_finder.run_crawl_process(url, allowed_domains=allowed_domains, max_depth=depth)
    

def filter_links():
    # Do later
    return

def parse_links_dict(links_file):
    list_of_links, link_titles , unique_links = links_util.prase_links(links_file)
    
    return list_of_links, link_titles , unique_links 


def scrape_page():
    # Scape pages
    # Save pages db
    
    return


def rag_pages():
    return


def run_career_app(url):
    unfiltered_links = get_links(url)
    list_of_links, link_titles , unique_links  = parse_links_dict(unfiltered_links)
    scrape_pages = scraper_pages(list_of_links)
    # print(scrape_pages)
    
    print("Done")
    return

    