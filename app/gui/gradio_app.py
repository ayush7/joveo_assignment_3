# import gradio as gr 
# from agents import call_agent
# from rag.retriver import AdvanceRetriever
# import params 

# initial_query = "Tell me about the website and what are the different sections in the website."

# class WebsiteChatBotRag:
#     async def retrival_chatbot_main(self,user_query=initial_query, 
#                                     conversational_histoy=None):
#         """Runs the chatbot with retrival"""
        
        
        
#         # Advance Retriver
#         adv_retr_obj = AdvanceRetriever(params.RAG_DATABASE_DIR)
#         results = adv_retr_obj.two_step_retrieval(query=initial_query)
#         print(results[0].keys())
#         r = []
#         for item in results:
#             r.append(str(item["input"]))
        
#         results = r 
        
        
#         opeai_obj = call_agent.OpenAICaller()
#         reply, conversation_history = opeai_obj.multi_turn_chat(context=results, agent="rag_chatbot", turn_prompt=initial_query)
        
#         print(reply)
#         # print(reply.content)
        
#         return reply, conversation_history, results


#     async def retrival_chatbot_without_retrival(self,user_query="tell me more", 
#                                     conversational_histoy=None):
#         """Runs the chatbot without retrival"""
        
#         results = None
        
#         opeai_obj = call_agent.OpenAICaller()
#         reply, conversation_history = opeai_obj.multi_turn_chat(context=results, agent="rag_chatbot", turn_prompt=user_query)
        
#         print(reply)
#         # print(reply.content)
        
#         return reply, conversation_history, results

#     async def gradio_chatbot_interface(self,user_query, conversation_history=None, run_retrival=False):
#         """Gradio interface for the chatbot"""
#         retrieval_results_html = None
#         # Call the retrival_chatbot_main function with the user's query and the conversation history
#         if conversation_history is None or run_retrival is True:
#             response, updated_conversation_history, retrival_results = await retrival_chatbot_main(user_query, conversation_history)
#             # Convert the retrieval results to HTML for display in a scrollable box
#             retrieval_results_html = str(retrival_results)
#         else :
#             response, updated_conversation_history, retrival_results = await retrival_chatbot_without_retrival(user_query, conversation_history)
        
        
#         return response, updated_conversation_history, retrieval_results_html

# # Define the Gradio interface
# def create_interface():

#     with gr.Blocks() as demo:
#         gr.Markdown("#Website Chatbot")
        
#         with gr.Row():
#             # Left column for website input and processing
#             with gr.Column(scale=1):
#                 # Website URL input
#                 url_input = gr.Textbox(label="Enter Website URL")
                
#                 # Process website button
#                 process_btn = gr.Button("Process Website")
                
#                 # Clear context button
#                 clear_btn = gr.Button("Clear Conversation Context")
                
#                 # Status message
#                 status_output = gr.Textbox(label="Status", interactive=False)
#                         # Right column for chat interface
            
#             with gr.Column(scale=2):
#                 # Chatbot interface
#                 chatbot_interface = gr.ChatInterface(
#                     chatbot.chat, 
#                     title="Chat with Website Content"
#                 )
#                 # Sources section
#                 with gr.Accordion("Sources", open=False):
#                     sources_output = gr.Textbox(label="Relevant Sources")
       
#         # Wire up the interactions
#         process_btn.click(
#             chatbot.process_website, 
#             inputs=[url_input], 
#             outputs=[status_output]
#         )
#         # Update sources after each chat interaction
#         chatbot_interface.chatbot.then(
#             lambda x: x[-1][1], 
#             inputs=[chatbot_interface.chatbot], 
#             outputs=[sources_output]
#         )

#     return demo


import gradio as gr 
from agents import call_agent
from rag.retriver import AdvanceRetriever
import params 
import chromadb
import asyncio
from career_app import run_career_app


class WebsiteChatBotRag:
    def __init__(self):
        self.conversation_history = []
        self.retrieval_results = None
        self.current_website = None
        self.current_collection = None
        self.sources_list = None
        
        


    async def process_website(self, website_url,delete_old_cache=False,
                           delete_persistent_db=False,
                           create_vector_db=True):
        """Process the website for retrieval - Scrapes and stores website"""
        try:
            
            
            x = await run_career_app(url=website_url, 
                           delete_old_cache=delete_old_cache,
                           delete_persistent_db=delete_persistent_db,
                           create_vector_db=True)

            
            return f"Website {website_url} processed successfully!\nMessage: {x}"
        except Exception as e:
            return f"Error processing website: {str(e)}"

    async def retrival_chatbot_main(self, user_query, conversational_history=None, collection_name="default"):
        """Runs the chatbot with retrieval"""
        try:
            # Use the current website's retrieval results if available
            # context = self.retrieval_results or ""
            
            adv_retr_obj = AdvanceRetriever(params.RAG_DATABASE_DIR, collection_name=self.current_collection)
            refined_results, self.sources_list = await adv_retr_obj.two_step_retrieval(query=user_query)
            print(len(refined_results))
            # print(refined_results[0]["input"])
            
            r = []
            for item in refined_results:
                r.append(str(item["input"]))
            
            context = r 
            
            # # Prepare conversation history
            # if conversational_history is None or conversational_history==[]:
            #     conversational_history = []
            
            # OpenAI agent call
            
            print("Calling OpenAI ")
            opeai_obj = call_agent.OpenAICaller()
            reply, updated_conversation_history = opeai_obj.multi_turn_chat(
                context=context, 
                agent="rag_chatbot", 
                turn_prompt=user_query
            )
            
            # Update conversation history
            self.conversation_history = updated_conversation_history
            
            return reply, updated_conversation_history, self.retrieval_results, self.sources_list 
        
        except Exception as e:
            return f"[x2] Error in chat: {str(e)}", [], None, self.sources_list 

    async def retrival_chatbot_without_retrival(self, user_query, conversational_history=None):
        """Runs the chatbot without retrieval"""
        try:
            # Prepare conversation history
            if conversational_history is None:
                conversational_history = []
            
            # OpenAI agent call
            opeai_obj = call_agent.OpenAICaller()
            reply, updated_conversation_history = opeai_obj.multi_turn_chat(
                context=None, 
                agent="rag_chatbot", 
                turn_prompt=user_query,
                conversation_history=conversational_history
            )
            
            # Update conversation history
            self.conversation_history = updated_conversation_history
            
            return reply, updated_conversation_history, None, self.sources_list
        
        except Exception as e:
            return f"Error in chat: {str(e)}", [], None

    async def gradio_chatbot_interface(self, user_query, conversation_history=None, run_retrival=False):
        """Gradio interface for the chatbot"""
        print(f"Called chatbot_interface")

        retrieval_results_html = None
        
        # Determine which chat method to use
        
        if self.retrieval_results is None or run_retrival:
            print(f"Called chatbot_interface - Condition Retrival")

            response, updated_conversation_history, retrival_results, sources_list = await self.retrival_chatbot_main(
                user_query, 
                conversation_history
            )
            retrieval_results_html = str(retrival_results)
        else:
            print(f"Called chatbot_interface - Condition NoRet")

            response, updated_conversation_history, retrival_results, sources_list = await self.retrival_chatbot_without_retrival(
                user_query, 
                conversation_history
            )
        
        return response, updated_conversation_history, retrieval_results_html, self.sources_list
    
    async def converser_main(self, user_query, conversation_history):
        
        print(f"Called Converser")
        
        response = "" 
        updated_conversation_history = conversation_history 
        retrieval_results_html = self.retrieval_results
        sources_list = ["None", "None"]
        
        try:
            if self.conversation_history == []:
                print(f"Called converser - Condition Retriver")

                # Call retriver enabled function
                response, updated_conversation_history, retrieval_results_html, sources_list = await self.gradio_chatbot_interface(
                    user_query=user_query,
                    conversation_history=conversation_history,
                    run_retrival=True)
                
            else:
                # Call no retriver function
                print(f"Called Converser - Condition NoRet")

                response, updated_conversation_history, retrieval_results_html, sources_list = await self.gradio_chatbot_interface(
                    user_query, 
                    conversation_history
                )
                
        except Exception as e:
            return f"[xx] Error in Chatbot Response Generation {str(e)}", conversation_history, self.retrieval_results
        print(f"x3: {type(sources_list)}")
        return response, updated_conversation_history, retrieval_results_html, self.sources_list
    
    
    def clear_conversation_history(self):
        self.conversation_history = []

    def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        self.retrieval_results = None
        self.current_website = None
        return "Conversation history and context cleared."


class ChatResponses:
    def __init__(self) -> None:
        self.response = ""
        self.updated_history = [] 
        self.sources = ""
        self.sources_list = []
        
def get_collection_names(db_path: str) :
    """Retrieve all collection names from ChromaDB"""
    client = chromadb.PersistentClient(path=db_path)
    collections = client.list_collections()
    return [collection.name for collection in collections]


def create_interface():
    response_store = ChatResponses()
    # Initialize the chatbot
    chatbot = WebsiteChatBotRag()
    
    with gr.Blocks() as demo:
        gr.Markdown("# Website RAG Chatbot")
        
        with gr.Row():
            # Left column for website input and controls
            with gr.Column(scale=1):
                url_input = gr.Textbox(
                    label="Enter Website URL",
                    placeholder="https://example.com"
                )
                
                delete_scraped_data_checkbox = gr.Checkbox(
                    label="Delete Old Scraped Data (Recommended)"
                )
                delete_vector_data_checkbox = gr.Checkbox(
                    label="Delete Old Vector DB"
                )
                
                # scrape_depth_dropdown = gr.Dropdown(
                    
                #     [str(i) for i in range(1, 6)],label="Scrape Depth"
                    
                # )
                
                
                with gr.Row():
                    process_btn = gr.Button("Scrape and Vectorize Website", variant="primary")
                    
                
                status_output = gr.Textbox(
                    label="Status",
                    interactive=False,
                    show_copy_button=False
                )
            
            # Right column for chat interface
            with gr.Column(scale=2):
                chatbox = gr.Chatbot(
                    label="Chat History",
                    height=500,
                    show_copy_button=True
                )
                
                with gr.Row():
                    msg_input = gr.Textbox(
                        label="Message",
                        placeholder="Type your message here...",
                        scale=9
                    )
                    submit_btn = gr.Button("Send", variant="primary", scale=1)
                    # clear_btn = gr.Button("Clear History", variant="secondary")
                
                collection_dropdown = gr.Dropdown(
                    choices=get_collection_names(params.RAG_DATABASE_DIR),
                    label="Select Collection",
                    interactive=True
                )
                
                # Add collection refresh 
                refresh_collections_btn = gr.Button("Refresh Collections")


                # Sources section
                with gr.Accordion("Sources", open=False):
                    sources_output = gr.Textbox(
                        label="Relevant Sources",
                        interactive=False,
                        
                        show_copy_button=True
                    )

        # Chat handler function
        async def chat_handler(message, history, collection_name):
            if collection_name:
                chatbot.current_collection = collection_name
                
            response_store.response, response_store.updated_history, response_store.sources, response_store.sources_list  = await chatbot.converser_main(
                user_query=message,
                conversation_history=response_store.updated_history
            )
            
            # Format the history correctly by adding the new message pair
            history = history or []
            history.append([message, response_store.response])
            
            formatted_sources = "\n\n".join([f"Source {i+1}:\n{source}" for i, source in enumerate(response_store.sources_list)]) if response_store.sources else ""
    
            
            # Update sources if needed (you might want to add sources_output as an output)
            return history, formatted_sources

                
        
        # Process website button handler
        process_btn.click(
            fn=chatbot.process_website,
            inputs=[url_input, delete_scraped_data_checkbox, delete_vector_data_checkbox],
            outputs=[status_output]
        )
        
        
        # Handle message submission with updated chat handler
        submit_btn.click(
            fn=chat_handler,
            inputs=[msg_input, chatbox, collection_dropdown],
            outputs=[chatbox, sources_output],
            api_name="chat"
        ).then(
            fn=lambda: None,  # Clear input after sending
            outputs=[msg_input]
        )

        # Also trigger on Enter key with updated chat handler
        msg_input.submit(
            fn=chat_handler,
            inputs=[msg_input, chatbox, collection_dropdown],
            outputs=[chatbox, sources_output],
        ).then(
            fn=lambda: None,  # Clear input after sending
            outputs=[msg_input]
        )
        def refresh_collections():
            return gr.Dropdown(choices=get_collection_names(params.RAG_DATABASE_DIR))
            
        refresh_collections_btn.click(
                fn=refresh_collections,
                outputs=[collection_dropdown]
            )

        
        # # Clear context button handler
        # clear_btn.click(
        #     fn=chatbot.clear_conversation_history,
        #     outputs=[status_output, chatbox, sources_output]
        # )
        
        # Update sources after each chat interaction
        def update_sources(message, chat_history):
            return chatbot.retrieval_results if chatbot.retrieval_results else ""
        
        submit_btn.click(
            fn=update_sources,
            inputs=[msg_input, chatbox],
            outputs=[sources_output]
        )

    return demo
# Launch the interface
if __name__ == "__main__":
    interface = create_interface()
    interface.launch()
