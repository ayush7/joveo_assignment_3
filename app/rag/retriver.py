"""
Retriver for the database. 
Uses (hopefully) 2 step retrival along with reranking. 
Maybe can add prompt variation and combine outputs and then rerank them as well. We'll see. 
"""

from langchain_chroma import Chroma
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
    def __init__(self, db_path, collection_name="default"):
        
        self.db_path = db_path
        self.embeddings = HuggingFaceEmbeddings(model_name=params.EMBEDDING_MODEL)
        self.model = CrossEncoder(params.CROSS_ENCODER_MODEL)
        self.collection_name = collection_name
        self.db = Chroma(
            persist_directory=self.db_path,
            collection_name=self.collection_name,
            embedding_function=self.embeddings
        )


    async def two_step_retrieval(self, query):
        # Initial retrieval
        initial_results = self.db.similarity_search(query, 
                                         k=20, 
                                        #  filter=None   # Add filter dictionary here if you want to filter from metadata
                                         )
        
        print("Initial Results: ",len(initial_results))
        sources_dict = {'1':'234'} #Placeholder for testing rn 
        sources_list = []
        print("xcheck1")
        for item in initial_results:
            sources_list.append(item.page_content)
        
        print("xcheck2")
        # print(f"Initial Results: \n\n {initial_results}")
        # print(initial_results)
        # Refine results
        print("Refining results")
        refined_results = await self.refine_results(results=initial_results, query=query)
        
        print("Returning RAG Results" )
        return refined_results, sources_list

    async def refine_results(self, results, query):
    # Cross encoder based scoring -> Get top 10 results maybe
        print("Starting Reranking")
        model_inputs = [(query, result.page_content) for result in results]
        print(f"serach results: {len(model_inputs)}")
        # print(model_inputs)
        scores = self.model.predict(model_inputs)

        # Sort scores in decreasing order (not ascending reverse=True always)
        results = [{"input": inp, "score": score} for inp, score in zip(model_inputs, scores)]
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        print("Query:", query)

        scores = set()
        for hit in results:
            scores.add(hit["score"])
        print(scores)
        # print(results[0:1])
        
        return results[:10]

class QueryHandler:
    def __init__(self, database_path):
        self.retriever = AdvanceRetriever(database_path)

    def handle_query(self, query):
        return self.retriever.two_step_retrieval(query)
    

