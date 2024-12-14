from openai import OpenAI
from google import generativeai as geminiai 

from dotenv import dotenv_values

env_vals = dotenv_values(".env")
opeanai_key = env_vals["OPENAI_KEY"]
gemini_key = env_vals["GEMINI_KEY"]



def agent_prompts(agent):
    sys = ""
    usr = ""
    context_replace_keyword = ""
    
    
    
    return sys, usr, context_replace_keyword


def get_openai_response():
    return


def get_gemini_response(context, agent:str, model = "gemini-1.5-flash"):

    system_prompt, user_prompt , replace_keyword = agent_prompts(agent=agent)    
    
    model=geminiai.GenerativeModel(
        model_name=model,
        system_instruction=system_prompt.replace(replace_keyword,str(context)))
    
    response = model.generate_content(user_prompt)
    
    print(response.text)
    
    return response


def run_gemini_chatbot():
    return



def run_openai_chatbot():
    return