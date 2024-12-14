from pydantic import BaseModel
from typing import List

class LinksStrEntity(BaseModel):
    link: str
    category: str 
    
class ListLinksOutput(BaseModel):
    categorised_links : List[LinksStrEntity]



links_agent = {
    "system_prompt":"""You are a classifier agent whose job is to correctly classify links and page titles to the correct category. You are given a set of page title and their corresponding link in a dictionary format.
    For each each link and page title pair, correctly classify them into one of these 5 categories: 'career','details','services','documentation' or 'others'.
    Your job is to go through each input pair and correctly determine what the page might contain. Give the output in a JSON format containing 'link' and 'category'. 
    Here is the dictionary of inputs:
    [CONTEXT]   
    """,
    "user_prompt":"""Given the input, categorise each of them into the correct category : 'career','details','services','documentation' or 'others'. Return the output in JSON format. """,
    "context_replace_keyword":"""[CONTEXT]"""
}