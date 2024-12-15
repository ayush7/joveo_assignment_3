"""
Main file doing the backend pipeline's heavylifting. 
run.py is just the entrypoint 

"""

from crawler import links_finder, links_util
from scraper import scrape_and_save
from rag import build_db, retriver
from rag.retriver import AdvanceRetriever, SimpleLangChainRetriever
from agents import call_agent

import params 
import os 
import shutil
import json 
import time 
from tqdm import tqdm  
from agents.call_agent import OpenAICaller
import ast 
import tldextract

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


async def scrape_pages_func(links_dict, list_of_links:list = [], link_titles_list:list = []):
    # Scrapes and saves pages for further processing 
    # Can use cache and stuff but better design so you don't have to do scraping time and again
    
    list_of_links = []
    link_titles_list = []
    link_category_list = []
    
    for link_item in links_dict["categorised_links"]:
        list_of_links.append(link_item["link"])
        link_titles_list.append(link_item["page_title"])
        link_category_list.append(link_item["category"])
    
    
    for link, title , cat in zip(list_of_links, link_titles_list, link_category_list):
        link_status = {"link": link}
        saved_db, saved_path, scrape_success = await scrape_and_save.scrape_and_save_page(link, page_title=title, category=cat)
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
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)
    
def deleted_vec_db(db_path = ".ragdb/chroma_db/"):
    if os.path.exists(db_path):
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
        
        metadata["category"] =  collection_name #scrape_list_item["category"]                                   # Variable for later once done with category agent
        metadata["page-title"] = scrape_list_item["page_title"]         
        try:
            vectorstore = rag_obj.ingest_markdown(markdown_file_path=scrape_list_item["filepath"],
                                metadata=metadata,
                                collection_name=metadata["category"])
        except Exception as e:
            print(f"Error occured while vecotrizing {scrape_list_item['filepath'] -- {str(e)}}")
    return vectorstore



def categorize_links_from_dict(links_dict:dict):
    print("Calling Classifier")
    llm_obj = OpenAICaller()
    
    classifier_response = llm_obj.single_call(str(links_dict), agent="links_classifier")
    
    classification_dict = ast.literal_eval(classifier_response)
    
    # print(classification_dict)
    # print(type(classification_dict))
    
    new_dict = {"categorised_links":[]}
    
    # Brute force: Can use better .join logic
    for item in classification_dict["categorised_links"]:
        for l,pt in links_dict.items():
            print(l, ":", pt, "--", item)
            if l == item["link"]:
                entry = {
                    "link" : l,
                    "page_title": pt,
                    "category": item["category"]
                }
                
                new_dict["categorised_links"].append(entry)
            
    
    
    return new_dict



async def run_career_app(url, delete_old_cache = True, delete_persistent_db = True, create_vector_db = True):
    
    ### Deleted old cache, just using it for testing and presentation
    if delete_old_cache :
        delete_cache()
    
    
    
    ### Run crawler - get all the links and shit 
    unfiltered_links = get_links(url, depth=params.MAX_DEPTH)
    list_of_links, link_titles , unique_links  = parse_links_dict(unfiltered_links)
    
    
    ### Run agent to filter links further - Todo 
    unique_links = categorize_links_from_dict(unique_links)
    
    ### Save unique links for future reference
    unique_links_save_path = os.path.join(params.LINKS_CACHE_DIR, params.UNIQUE_LINKS_FILE)
    with open(unique_links_save_path, 'w', encoding='utf-8') as ff:
        json.dump(unique_links,ff, indent=4)
    
    print(len(list_of_links))

    
    # # Run the scraper to scrape pages 
    scrape_status_list, saved_scraped_db = await scrape_pages_func(unique_links,list_of_links[:20], link_titles[:20])
    
    collection_name = primary_domain = str(tldextract.extract(url).registered_domain)
    
    # Vector Ingestion Pipeline
    if delete_persistent_db == True:
        deleted_vec_db()
        
    # Create Vector store
    if create_vector_db:
        rag_pages_for_vectordb(scrape_status_list=scrape_status_list, saved_scraped_db=saved_scraped_db, collection_name=collection_name)
        
    
    
    
    
    print(f"{scrape_status_dict} \n\n\n\n RAG DB CREATED. DONE")
    return 



async def retrival_chatbot_looper():
    return 



async def retrival_chatbot_main():
    """Runs the chatbot"""
    
    initial_query = "Tell me about the website and what are the different sections in the website."
    
    # Advance Retriver
    adv_retr_obj = AdvanceRetriever(params.RAG_DATABASE_DIR)
    results = adv_retr_obj.two_step_retrieval(query=initial_query)
    
    opeai_obj = call_agent.OpenAICaller()
    reply, conversation_history = opeai_obj.multi_turn_chat(context=results, agent="rag_chatbot", turn_prompt=initial_query)
    
    print(reply)
    print(reply.content)
    
    return 


    