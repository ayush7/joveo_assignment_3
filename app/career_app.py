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
from tqdm import tqdm  


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


async def scrape_pages_func(list_of_links:list, link_titles_list:list):
    # Scrapes and saves pages for further processing 
    # Can use cache and stuff but better design so you don't have to do scraping time and again
    
    
    for link, title in zip(list_of_links, link_titles_list):
        link_status = {"link": link}
        saved_db, saved_path, scrape_success = await scrape_and_save.scrape_and_save_page(link, page_title=title)
        if not scrape_success:
            print(f"Failed to scrape : {link}")
            link_status["scrape_success"] = False
        else:
            print(f"Scrape successful for : {link}")
            link_status["scrape_success"] = True
            link_status["saved_path"] = saved_path

        
        scrape_status_dict.append(link_status)
         
    
    return scrape_status_dict, saved_db

def delete_cache(cache_path = ".cache"):
    shutil.rmtree(cache_path)
    
def deleted_vec_db(db_path = ".ragdb/chroma_db/"):
    shutil.rmtree(db_path)


def rag_pages_for_vectordb(scrape_status_list, saved_scraped_db, collection_name):
    
    # Open DB for saved pages
    with open(saved_scraped_db, 'r') as ff:
        scraped_db = json.load(ff)
    
    
    # Get the rag object
    rag_obj = build_db.LangChainWebsiteStore(db_location=params.RAG_DATABASE_DIR)
    
    # Run loop to ingest documents
    print(f"RUNNING RAG INGESTION")

    
    for scrape_list_item in tqdm(scraped_db["scraped_data"]):
        metadata = {}
        metadata["content-link"] = scrape_list_item["link"]
        
        metadata["category"] = "default"                                     # Variable for later once done with category agent
        metadata["page-title"] = scrape_list_item["page_title"]         
        
        vectorstore = rag_obj.ingest_markdown(markdown_file_path=scrape_list_item["filepath"],
                                metadata=metadata,
                                collection_name=metadata["category"])
    
    return vectorstore


async def run_career_app(url, delete_old_cache = True, delete_persistent_db = False, create_vector_db = True):
    
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
        json.dump(unique_links,ff, indent=4)
    

    
    # Run the scraper to scrape pages 
    scrape_status_list, saved_scraped_db = await scrape_pages_func(list_of_links[:5], link_titles[:5])
    
    
    
    # Vector Ingestion Pipeline
    if delete_persistent_db == True:
        deleted_vec_db()
        
    
    if create_vector_db:
        rag_pages_for_vectordb(scrape_status_list=scrape_status_list, saved_scraped_db=saved_scraped_db, collection_name="default_collection")
    
    
    
    
    print(f"{scrape_status_dict} \n\n\n\n RAG DB CREATED. DONE")
    return 


def retrival_chatbot_main():
    """Runs the chatbot"""
    return


    