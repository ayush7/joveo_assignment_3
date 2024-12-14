import os
from langchain_community.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate  # Added this import


from dotenv import load_dotenv



## Load environment variables (for OpenAI API key)
load_dotenv()

def process_pdfs(pdf_directory):

    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len
    )
    splits = text_splitter.split_documents(documents)
    
    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    
    # Create and persist vector store
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    return vectorstore


class LangChainWebsiteStore:
    def __init__(self, chunksize=3000, chunkoverlap=300) -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(
                                                    chunk_size=2000,
                                                    chunk_overlap=200,
                                                    length_function=len
                                                )
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        # self.vector_store = Chroma.from_documents(
        #                                 documents=splits,
        #                                 embedding=embeddings,
        #                                 persist_directory="./chroma_db"
        #                             )
        
    def load_document(self, markdown_path):
        pass 