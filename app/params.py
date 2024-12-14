"""
Kept this for default values.
Will use it later once I clean a bit of the code
"""
MAX_DEPTH = 1                               # Depth to crawl 
CACHE_DIR = ".cache/"                       # Cache base directory 
LINKS_CACHE_DIR = ".cache/links_cache"      # Crawled links cache dir
SCRAPE_CACHE_DIR = ".cache/scraped_data"    # Scraped pages cache dir 
UNIQUE_LINKS_FILE = "unique_links.json"
RAG_DATABASE_DIR = ".ragdb/chroma_db/"
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
SIMPLE_TEST_QUERY = "What is the primary purpose of the website?"