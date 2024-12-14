"""
Main file doing the backend pipeline's heavylifting. 
run.py is just the entrypoint 

"""

from crawler import links_finder, links_util
from scraper import scrape_and_save
from rag import build_db
import params 
import os 
import shutil
import json 
import time 


scrape_status_dict = []

def get_links(url, allowed_domains = [], depth = 1):
    # Returns file with links saved
    return links_finder.run_crawl_process(url, allowed_domains=allowed_domains, max_depth=depth)
    

def filter_links():
    # Do later
    return

def parse_links_dict(links_file):
    list_of_links, link_titles , unique_links = links_util.prase_links(links_file)
    
    return list_of_links, link_titles , unique_links 


async def scrape_pages_func(list_of_links:list):
    # Scrapes and saves pages for further processing 
    # Can use cache and stuff but better design so you don't have to do scraping time and again
    
    
    for link in list_of_links:
        link_status = {"link": link}
        saved_db, saved_path, scrape_success = await scrape_and_save.scrape_and_save_page(link)
        if not scrape_success:
            print(f"Failed to scrape : {link}")
            link_status["scrape_success"] = False
        else:
            print(f"Scrape successful for : {link}")
            link_status["scrape_success"] = True
        
        scrape_status_dict.append(link_status)
         
    
    return

def delete_cache(cache_path = ".cache"):
    shutil.rmtree(cache_path)
    



def rag_pages():
    return


async def run_career_app(url, delete_old_cache = True, delete_persistent_db = False):
    
    ### Deleted old cache, just using it for testing and presentation
    if delete_old_cache :
        delete_cache()
    
    
    
    ### Run crawler - get all the links and shit 
    unfiltered_links = get_links(url)
    list_of_links, link_titles , unique_links  = parse_links_dict(unfiltered_links)
    
    ### Run agent to filter links further - Todo 
    
    ### Save unique links for future reference
    unique_links_save_path = os.path.join(params.LINKS_CACHE_DIR, params.UNIQUE_LINKS_FILE)
    with open(unique_links_save_path, 'w', encoding='utf-8') as ff:
        json.dump(unique_links,ff)
    
    
    
    # Run the scraper to scrape pages 
    scrape_pages = await scrape_pages_func(list_of_links[:10])
    
    
    
    
    print(f"{scrape_status_dict} \n\n\n\n Done")
    return

    