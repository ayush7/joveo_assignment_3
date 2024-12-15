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
import asyncio
from career_app import run_career_app


class WebsiteChatBotRag:
    def __init__(self):
        self.conversation_history = []
        self.retrieval_results = None
        self.current_website = None
        
        


    async def process_website(self, website_url):
        """Process the website for retrieval - Scrapes and stores website"""
        try:
            
            
            await run_career_app(url=website_url, 
                           delete_old_cache=False,
                           delete_persistent_db=False,
                           create_vector_db=True)
            # # Advance Retriever
            # adv_retr_obj = AdvanceRetriever(params.RAG_DATABASE_DIR)
            
            # # Store the current website for reference
            # self.current_website = website_url
            
            # # Perform initial retrieval about the website
            # initial_query = f"Tell me about the website {website_url} and what are the different sections in the website."
            # results = adv_retr_obj.two_step_retrieval(query=initial_query)
            
            # # Convert results to list of strings
            # r = [str(item["input"]) for item in results]
            # self.retrieval_results = r
            
            return f"Website {website_url} processed successfully!"
        except Exception as e:
            return f"Error processing website: {str(e)}"

    async def retrival_chatbot_main(self, user_query, conversational_history=None):
        """Runs the chatbot with retrieval"""
        try:
            # Use the current website's retrieval results if available
            context = self.retrieval_results or []
            
            # Prepare conversation history
            if conversational_history is None:
                conversational_history = []
            
            # OpenAI agent call
            opeai_obj = call_agent.OpenAICaller()
            reply, updated_conversation_history = opeai_obj.multi_turn_chat(
                context=context, 
                agent="rag_chatbot", 
                turn_prompt=user_query,
                conversation_history=conversational_history
            )
            
            # Update conversation history
            self.conversation_history = updated_conversation_history
            
            return reply, updated_conversation_history, self.retrieval_results
        
        except Exception as e:
            return f"Error in chat: {str(e)}", [], None

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
            
            return reply, updated_conversation_history, None
        
        except Exception as e:
            return f"Error in chat: {str(e)}", [], None

    async def gradio_chatbot_interface(self, user_query, conversation_history=None, run_retrival=False):
        """Gradio interface for the chatbot"""
        retrieval_results_html = None
        
        # Determine which chat method to use
        if self.retrieval_results is not None and run_retrival:
            response, updated_conversation_history, retrival_results = await self.retrival_chatbot_main(
                user_query, 
                conversation_history
            )
            retrieval_results_html = str(retrival_results)
        else:
            response, updated_conversation_history, retrival_results = await self.retrival_chatbot_without_retrival(
                user_query, 
                conversation_history
            )
        
        return response, updated_conversation_history, retrieval_results_html

    def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        self.retrieval_results = None
        self.current_website = None
        return "Conversation history and context cleared."

def create_interface():
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
                
                with gr.Row():
                    process_btn = gr.Button("Process Website", variant="primary")
                    clear_btn = gr.Button("Clear Context", variant="secondary")
                
                status_output = gr.Textbox(
                    label="Status",
                    interactive=False,
                    show_copy_button=True
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
                
                # Sources section
                with gr.Accordion("Sources", open=False):
                    sources_output = gr.Textbox(
                        label="Relevant Sources",
                        interactive=False,
                        lines=3,
                        show_copy_button=True
                    )

        # Chat handler function
        async def chat_handler(message, history):
            response, updated_history, _ = await chatbot.gradio_chatbot_interface(
                message,
                conversation_history=history
            )
            return response

        # Handle message submission
        submit_btn.click(
            fn=chat_handler,
            inputs=[msg_input, chatbox],
            outputs=[chatbox],
            api_name="chat"
        ).then(
            fn=lambda: None,  # Clear input after sending
            outputs=[msg_input]
        )

        # Also trigger on Enter key
        msg_input.submit(
            fn=chat_handler,
            inputs=[msg_input, chatbox],
            outputs=[chatbox],
        ).then(
            fn=lambda: None,  # Clear input after sending
            outputs=[msg_input]
        )
        
        # Process website button handler
        process_btn.click(
            fn=chatbot.process_website,
            inputs=[url_input],
            outputs=[status_output]
        )
        
        # Clear context button handler
        clear_btn.click(
            fn=chatbot.clear_conversation_history,
            outputs=[status_output, chatbox, sources_output]
        )
        
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
