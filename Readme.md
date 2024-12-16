# Website Chatbot - Joveo Assignment 

## Notes

- The scraping may not work for every website as I used crawl4ai which is open source but has limits when it comes to websites with good robot protection
- The database creation takes some time as crawling, scraping and vectorization all happens at the same time - Be patient, can take upto 20-30 minutes even for 400 links
- Context limiter has not been added so there can be some errors for larger websites. I have tried to limit it with rudimentary methods but it may still cause issues sometimes. 

## Optimizations 
-  Added metadata fields for easy filteration during retrival. Query classification agent was having adding additional time so removes it.
-  Reranking - once retrivals are done contextual similarity between documents are found using a Cross Encoder and scored. Better encoders  can be tried to improve accuracy. 
- Every page is converted to Markdown for ease of passing to LLMs. Links are removed from all page contents to ensure better contextual understanding


## Optimizations I could not do yet:
- Prompt Classification
- Multi Prompt retriver - To ensure variations of each prompt is passed in order to query the database. All the results are combined and then reranked. 
- Optimization with summarizations - For reducing time. Instead of full text, a summary of the text with only the basic version is used for retrival. Then the full text retrived from matches. Increase information density and gives better results. 
- Multi algo serach -> search with different strategies but combine scores to get best matches 





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

### params.py
Edit the values in params.py for changing things like depth of retrival. <br>
Note: The deeper the crawl the higher the chances of breaking in intermediory LLM calls - which have not been optimized. 


## Progress <br>

Tested Module - :white_check_mark:
Probably won't be able to finish :thumbsdown: 

Crawler
- [x] Write Crawler :white_check_mark:
- [x] Crawler Link Parser :white_check_mark:


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
- [x] RAG Agent :white_check_mark:
- [x] Gemini Single Query Module (not tested)
- [x] OpenAI Single Query Module :white_check_mark:
- [ ] Gemini Conversational AI Module 
- [x] OpenAI Conversational AI Module :white_check_mark:

Special Agents
- [x] Link classification Agent :white_check_mark:
- [ ] Query Classifier Agent 

GUI
- [x] Create basic Streamlit/gradio app :white_check_mark:
- [x] Upgrade app with options :white_check_mark:

Logging 
- [ ] Add logger (low priority as of now) :thumbsdown:

Error Handlers
- [x] Add error handling for each module :white_check_mark:
