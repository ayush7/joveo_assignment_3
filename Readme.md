# Website Chatbot - Joveo Assignment 

## Notes

- The scraping may not work for every website as I used crawl4ai which is open source but has limits when it comes to websites with good robot protection
- The database creation takes some time as crawling, scraping and vectorization all happens at the same time
- Added latency in retrival due to cross encoder reranking - adding parellel processing can fix it significantly 
- Context limiter has not been added so there can be some errors for larger websites. I have tried to limit it with rudimentary methods but it may still cause issues sometimes. 



## Instructions to Run 

### Setup the environment

```

git clone https://github.com/ayush7/joveo_assignment_3
cd joveo_assignment_3
python3 -m venv .ragenv
source .ragenv/bin/activate
pip install -r requirements.txt
```

### Add keys

- Create a file named `.env` in `app` directory 
- Add :
```
GEMINI_KEY = "your-gemini-key"
OPENAI_KEY = "your-openai-key"
```

### Run setup.py to configure nltk dependency

```
python setup.py
```

### Run the app
```
cd app
python run.py
``` 

## Progress <br>

Tested Module - :white_check_mark:
Probably won't be able to finish :thumbsdown: 

Crawler
- [x] Write Crawler :white_check_mark:
- [x] Crawler Link Parser :white_check_mark:
- [ ] Link Filter Agent

Scraper
- [x] Write scraper :white_check_mark:
- [x] Scraper database :white_check_mark:
- [x] Remove Links from scraped markdown :white_check_mark:

RAG Module
- [x] Database Creator Module :white_check_mark:
- [x] Retrival Module :white_check_mark:
- [x] Adv Rerank Module/2 step retriver :white_check_mark:
- [ ] Adv Multi prompt retriver :thumbsdown:

Agents Module
- [ ] Context Compression Agent :thumbsdown:
- [x] RAG Agent
- [x] Gemini Single Query Module (not tested)
- [x] OpenAI Single Query Module 
- [ ] Gemini Conversational AI Module 
- [x] OpenAI Conversational AI Module 

GUI
- [ ] Create basic Streamlit/gradio app [in progress]
- [ ] Upgrade app with options

Logging 
- [ ] Add logger (low priority as of now) :thumbsdown:

Error Handlers
- [ ] Add error handling for each module :thumbsdown:
