"""Just run this file. Will add argv options maybe, with a main function"""
import asyncio
import career_app

if __name__=="__main__":
    asyncio.run(career_app.run_career_app("https://crawl4ai.com/", delete_old_cache = True))