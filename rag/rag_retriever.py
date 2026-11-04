from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

class Retriever:
    def __init__(self):
        self.chroma_db = "data/vector_db"
        self.collection_name = "portfolio_knowledge"
        self.embedding_model = ("sentence-transformers/all-MiniLM-L6-v2")
        self.embedding = None
        self.vector_store = None

    # Initialize embedding model
    def get_embedding(self):
        print("loading embedding model...")
        self.embedding = HuggingFaceEmbeddings(model_name=self.embedding_model) 
        return self.embedding

    # load existing vector store
    def load_vector_store(self):
        print("loading vector store")
        self.vector_store = Chroma(
            persist_directory=self.chroma_db,
            collection_name=self.collection_name,
            embedding_function=self.embedding
        )
        return self.vector_store
    # Retrieve relevant documents based on query
    def retrieve(self,query,k=5):
        print("retrieving relevant documents...")
        self.get_embedding()
        vector_store = self.load_vector_store()
        if vector_store is None:
            raise ValueError("Vector store is not loaded. Please load the vector store first.")
        return vector_store.similarity_search(query, k=k)
    # main execution function
    def run(self,k=5):
        print("running retriever...")
        # self.get_embedding()
        # self.load_vector_store()
        query=input("Enter your query: ")
        print("\nRetrieved Results")
        print("-------------------------")
        results=self.retrieve(query)
        for i,doc in enumerate(results,start=1):
            print(f"Result {i}:")
            print(f"Content: {doc.page_content}")
            print(f"Metadata: {doc.metadata}")
            print("-------------------------")

if __name__ == "__main__":
    retriever = Retriever()
    retriever.run()

