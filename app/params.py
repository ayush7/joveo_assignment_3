"""
Kept this for default values.
Will use it later once I clean a bit of the code
"""


MAX_DEPTH = 2                                                    # Depth to crawl 

CACHE_DIR = ".cache/"                                            # Cache base directory 
LINKS_CACHE_DIR = ".cache/links_cache"                           # Crawled links cache dir
SCRAPE_CACHE_DIR = ".cache/scraped_data"                         # Scraped pages cache dir 
UNIQUE_LINKS_FILE = "unique_links.json"                          # DB of unique links -  helper
RAG_DATABASE_DIR = ".ragdb/chroma_db/"                           # Vector Database storage path

EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"      # Embedding model for rag agent
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-TinyBERT-L-2"      # Model for reranking retrived items
SIMPLE_TEST_QUERY = "What is the primary purpose of the website?"


OPENAI_MODEL = "gpt-4o-mini"
GEMINI_MODEL = "gemini-1.5-flash"

DEFAULT_WEBSITE = "https://www.anthropic.com/"
