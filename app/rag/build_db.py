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



class LangChainWebsiteStore:
    def __init__(self, chunksize=3000, chunkoverlap=300, db_location = "./chroma_db", collection_name = "default") -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(
                                                    chunk_size=chunksize,
                                                    chunk_overlap=chunkoverlap,
                                                    length_function=len
                                                )
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.single_document = []
        self.documents = []
        self.db_location = db_location
        self.collection_name = collection_name
        
    def load_document(self, markdown_path):
        self.loader = UnstructuredMarkdownLoader(markdown_path)
        
        return self.loader.load()
    
    def generate_splits(self, documents):
        splits = self.text_splitter.split_documents(documents)
        return splits

    def store_document(self, splits):
        vectorstore = Chroma.from_documents(
                    documents=splits,
                    embedding=self.embeddings,
                    persist_directory=self.db_location, 
                    collection_name= self.collection_name,
                    collection_metadata = self.metadata
                )
        return vectorstore
    
    def ingest_markdown(self, markdown_file_path, metadata = None, collection_name = "default"):
        self.collection_name = collection_name
        self.metadata = metadata
        mdfile_doc = self.load_document(markdown_path=markdown_file_path)
        splits = self.generate_splits(mdfile_doc)
        vectorstore = self.store_document(splits)
        return vectorstore 
        
        