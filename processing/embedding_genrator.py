import json

from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


class VectorStore:

    def __init__(self):

        self.chroma_db = "data/vector_db"

        self.collection_name = "portfolio_knowledge"

        self.chunks_path = Path(
            "data/processed/chunks.json"
        )

        self.embedding_model = (
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.embedding = None

        self.vector_store = None

    # Load existing chunks
    def load_chunks(self):

        with open(
            self.chunks_path,
            "r",
            encoding="utf-8"
        ) as file:

            chunks = json.load(file)

        return chunks

    # Initialize embedding model
    def get_embedding(self):

        print("Loading embedding model...")

        self.embedding = HuggingFaceEmbeddings(
            model_name=self.embedding_model
        )

        return self.embedding

    # Convert chunks into LangChain Documents
    def prepare_documents(self, chunks):

        documents = []

        for chunk in chunks:

            document = Document(

                page_content=chunk["content"],

                metadata={
                    **chunk["metadata"],
                    "chunk_id": chunk["chunk_id"],
                    "parent_document_id": chunk["parent_document_id"],
                    "chunk_index": chunk["chunk_index"]
                }

            )

            documents.append(document)

        return documents

    # Build ChromaDB vector store
    def build_vector_store(self):

        print("\nBuilding vector store...\n")

        chunks = self.load_chunks()

        if not chunks:
            print("No chunks found.")
            return None

        embedding = self.get_embedding()

        documents = self.prepare_documents(chunks)

        self.vector_store = Chroma.from_documents(

            documents=documents,

            embedding=embedding,

            collection_name=self.collection_name,

            persist_directory=self.chroma_db

        )

        print("\nVector store created successfully!")

        print("Total chunks stored:", len(documents))

        return self.vector_store

    # Main execution
    def run(self):

        print("\nStarting Vector Store Creation...\n")

        self.build_vector_store()


if __name__ == "__main__":

    vector_store = VectorStore()

    vector_store.run()
    