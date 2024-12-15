"""
Just run this file. Will add argv options maybe, with a main function. 
Will see how it all pans out
"""
import asyncio
import career_app
import time 


if __name__=="__main__":
    
    vectorization_start_time = time.time()
    # asyncio.run(career_app.run_career_app("https://crawl4ai.com/", delete_old_cache = True))
    print(f"Total time for Vectorization {time.time() - vectorization_start_time}")
    
    
    asyncio.run(career_app.retrival_chatbot_main())