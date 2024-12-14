# Career Chatbot - Joveo Assignment 

## Instructions to Run 

### Setup the environment

```
git clone https://github.com/ayush7/joveo_assignment_3
cd joveo_assignment_3
python3 -m venv .ragenv
source .ragenv/bin/activate
pip install -r requirements.txt
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
- [x] Retrival Module (Testing)
- [x] Rerank Module/2 step retriver (Testing)
- [ ] Advanced Multi prompt retriver :thumbsdown:

Agents Module
- [ ] Context Compression Agent :thumbsdown:
- [ ] RAG Agent
- [x] Gemini Single Query Module (not tested)
- [ ] OpenAI Single Query Module 
- [ ] Gemini Conversational AI Module
- [ ] OpenAI Conversational AI Module 

GUI
- [ ] Create basic Streamlit app
- [ ] Upgrade app with options

Logging 
- [ ] Add logger (low priority as of now)
