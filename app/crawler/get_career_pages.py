"""
Calls an agent to filter links pages.
Context is provided as a dictionary containing links and page name. 
The agent categorizes it into various categories like - about, finance, career, docs, services etc.

The RAG pages are then saved into various collections depending on this tag. 

"""



from agents import call_agent
