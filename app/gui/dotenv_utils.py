import dotenv
import os 

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

def set_new_crawl_depth(crawl_depth):
    dotenv.set_key(dotenv_file, "MAX_DEPTH", os.environ["key"])