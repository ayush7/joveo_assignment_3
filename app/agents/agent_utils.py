"""Mostly used for retriving different agents based on the query. Use internally."""

import agents.links_classifier_agent as linksagent
import agents.website_query_agent as websiteagent

def agent_prompts(agent):
    sys = ""
    usr = ""
    context_replace_keyword = ""
    
    if agent == "links_classifier":
        sys = linksagent.links_agent["system_prompt"]
        usr = linksagent.links_agent["user_prompt"]
        context_replace_keyword = linksagent.links_agent["context_replace_keyword"]
    elif agent == "rag_chatbot":
        sys = websiteagent.website_query_agent["system_prompt"]
        usr = websiteagent.website_query_agent["user_prompt"]
        context_replace_keyword= websiteagent.website_query_agent["context_replace_keyword"]
        
    
    
    
    return sys, usr, context_replace_keyword