"""
Retriver for the database. 
Uses (hopefully) 2 step retrival along with reranking. 
Maybe can add prompt variation and combine outputs and then rerank them as well. We'll see. 
"""

from langchain import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder
import params

class SimpleLangChainRetriever:
    """
    Retrieves documents simply without 2 step process
    """

    def __init__(self, db_location="./chroma_db", collection_name="default"):
        self.db_location = db_location
        self.collection_name = collection_name
        self.vectorstore = Chroma(
            persist_directory=self.db_location,
            collection_name=self.collection_name
        )

    def retrieve(self, query, top_k=5):
        """
        Retrieves the top_k most similar documents to the query.
        """
        results = self.vectorstore.similarity_search(query, top_k=top_k)
        print(results)
        return results



class AdvanceRetriever:
    def __init__(self, db_path):
        self.db = Chroma(db_path)
        self.embeddings = HuggingFaceEmbeddings(model_name=params.EMBEDDING_MODEL)
        self.model = CrossEncoder("cross-encoder/ms-marco-TinyBERT-L-2")


    def two_step_retrieval(self, query):
        # Initial retrieval
        initial_results = self.db.search(query, top_k=50)
        print(f"Initial Results: \n\n {initial_results}")
        
        # Refine results
        refined_results = self.refine_results(initial_results, query)
        return refined_results

    def refine_results(self, results, query):
    # Cross encoder based scoring -> Get top 10 results maybe
    
        model_inputs = [[query, result] for result in results]
        scores = self.model.predict(model_inputs)

        # Sort scores in decreasing order (not ascending reverse=True always)
        results = [{"input": inp, "score": score} for inp, score in zip(model_inputs, scores)]
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        print("Query:", query)

        for hit in results[0:3]:
            print("Score: {:.2f}".format(hit["score"]), "\t", hit["input"][1])
        
        return results[:10]

class QueryHandler:
    def __init__(self, database_path):
        self.retriever = Retriever(database_path)

    def handle_query(self, query):
        return self.retriever.two_step_retrieval(query)