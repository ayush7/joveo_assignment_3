import gradio as gr 
from agents import call_agent
from rag.retriver import AdvanceRetriever
import params 

initial_query = "Tell me about the website and what are the different sections in the website."

async def retrival_chatbot_main(user_query=initial_query, 
                                conversational_histoy=None):
    """Runs the chatbot"""
    
    
    
    # Advance Retriver
    adv_retr_obj = AdvanceRetriever(params.RAG_DATABASE_DIR)
    results = adv_retr_obj.two_step_retrieval(query=initial_query)
    print(results[0].keys())
    r = []
    for item in results:
        r.append(str(item["input"]))
    
    results = r 
    
    
    opeai_obj = call_agent.OpenAICaller()
    reply, conversation_history = opeai_obj.multi_turn_chat(context=results, agent="rag_chatbot", turn_prompt=initial_query)
    
    print(reply)
    # print(reply.content)
    
    return reply, conversation_history, results


async def retrival_chatbot_without_retrival(user_query="tell me more", 
                                conversational_histoy=None):
    """Runs the chatbot without retrival"""
    
    results = None
    
    opeai_obj = call_agent.OpenAICaller()
    reply, conversation_history = opeai_obj.multi_turn_chat(context=results, agent="rag_chatbot", turn_prompt=user_query)
    
    print(reply)
    # print(reply.content)
    
    return reply, conversation_history, results

async def gradio_chatbot_interface(user_query, conversation_history=None, run_retrival=False):
    """Gradio interface for the chatbot"""
    retrieval_results_html = None
    # Call the retrival_chatbot_main function with the user's query and the conversation history
    if conversation_history is None or run_retrival is True:
        response, updated_conversation_history, retrival_results = await retrival_chatbot_main(user_query, conversation_history)
        # Convert the retrieval results to HTML for display in a scrollable box
        retrieval_results_html = str(retrival_results)
    else :
        response, updated_conversation_history, retrival_results = await retrival_chatbot_without_retrival(user_query, conversation_history)
    
    
    return response, updated_conversation_history, retrieval_results_html

# Define the Gradio interface
with gr.Blocks() as iface:
    with gr.Row():
        text1 = gr.Textbox(label = "Retrive Website")
    with gr.Column(scale=0.5, min_width=300):
        # show context from retrival outputs
        text1 = gr.Textbox(label="Retrived Data")
    with gr.Column(scale=1, min_width=500):
        with gr.Chatbot() 
        
        

