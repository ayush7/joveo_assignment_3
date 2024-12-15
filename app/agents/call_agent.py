from openai import OpenAI
from google import generativeai as geminiai 
from agents.agent_utils import agent_prompts
from dotenv import dotenv_values
import params
env_vals = dotenv_values(".env")
opeanai_key = env_vals["OPENAI_KEY"]
gemini_key = env_vals["GEMINI_KEY"]


class GeminiCaller:
    def __init__(self) -> None:
        pass


class OpenAICaller:
    def __init__(self, model = None, temperature=0.5) -> None:
        self.api_key = opeanai_key
        
        if model == None:
            self.model = params.OPENAI_MODEL
        else:
            self.model = model 
            
        
        self.temperature = temperature
        self.client = OpenAI(api_key=self.api_key)
        self.conversation = []
        
    

    def single_call(self, context, agent="rag_chatbot"):
        system_prompt, user_prompt, replace_keyword, structured_output_format = agent_prompts(agent=agent)
        system_prompt = system_prompt.replace(replace_keyword, str(context))
        
        
        
        messages = [{"role":"system", "content":system_prompt},
                    {"role":"user", "content":user_prompt}]
        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            response_format=structured_output_format
        )
        
        return response.choices[0].message.content
    
    def handle_messages_for_long_chat(self, conversation_history):
        return
    

    def multi_turn_chat(self, context, agent, turn_prompt = "tell me more" ,conversation_history=None):
        if conversation_history is None:
            conversation_history = []

            system_prompt, user_prompt, replace_keyword = agent_prompts(agent=agent)
            system_prompt = system_prompt.replace(replace_keyword, str(context))
            user_prompt = user_prompt.replace("[QUERY]", turn_prompt)
            
            # Add initial system and user prompts to the conversation history
            conversation_history.append({"role": "system", "content": system_prompt})
            conversation_history.append({"role": "user", "content": user_prompt})
        else:
            conversation_history.append({"role":"user", "content":turn_prompt})
            

        response = self.client.chat.completions.create(
            model=self.model,
            messages=conversation_history,
            temperature=self.temperature
        )
        
        
        reply = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": reply})
        
        return reply, conversation_history







def get_gemini_response(context, agent:str, model = "gemini-1.5-flash"):

    system_prompt, user_prompt , replace_keyword = agent_prompts(agent=agent)    
    
    model=geminiai.GenerativeModel(
        model_name=model,
        system_instruction=system_prompt.replace(replace_keyword,str(context)))
    
    response = model.generate_content(user_prompt)
    
    print(response.text)
    
    return response


