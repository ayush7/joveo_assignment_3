from openai import OpenAI
from google import generativeai as geminiai 

from dotenv import dotenv_values

env_vals = dotenv_values(".env")
opeanai_key = env_vals["OPENAI_KEY"]
gemini_key = env_vals["GEMINI_KEY"]

