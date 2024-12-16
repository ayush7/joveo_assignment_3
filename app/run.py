"""
Just run this file. Will add argv options maybe, with a main function. 
Will see how it all pans out
"""
import asyncio
import career_app
import time 
from gui import gradio_app
import params

import logging 

logging.basicConfig()
logging.getLogger().setLevel(logging.WARNING)

if __name__=="__main__":
    
    # # Run scraping+vectorization 
    # vectorization_start_time = time.time()
    # website = "https://www.paulgraham.com/" #params.DEFAULT_WEBSITE
    # asyncio.run(career_app.run_career_app(website, delete_old_cache = True, create_vector_db=False))
    # print(f"Total time for Vectorization {time.time() - vectorization_start_time}")
    
    
    # # RUN Only vectorizer on scraped db 
    # career_app.deleted_vec_db()
    # career_app.rag_pages_for_vectordb([],".cache/scraped_data/scrape_db.json", collection_name='anthropic.com')
    
    
    # # Run Simple Retrival
    # asyncio.run(career_app.retrival_chatbot_main())
    
    
    # # Run the GUI
    interface = gradio_app.create_interface()
    asyncio.run(interface.launch())