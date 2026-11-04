import json
import uuid

from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentChunker:

    def __init__(self):

        self.input_path = Path(
            "data/processed/cleaned_documents.json"
        )

        self.output_path = Path(
            "data/processed/chunks.json"
        )

        self.chunk_size = 300

        self.chunk_overlap = 50

        self.text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=self.chunk_size,

            chunk_overlap=self.chunk_overlap,

            length_function=len,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]

        )

    # --------------------------------
    # 1. Load cleaned documents
    # --------------------------------

    def load_documents(self):

        with open(
            self.input_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    # --------------------------------
    # 2. Generate chunks
    # --------------------------------

    def create_chunks(self, documents):

        all_chunks = []

        for document in documents:

            content = document.get("content", "")

            if not content.strip():
                continue

            metadata = document.get("metadata", {})

            document_id = document["id"]

            # Split document into smaller chunks

            text_chunks = self.text_splitter.split_text(
                content
            )

            total_chunks = len(text_chunks)

            for index, chunk_text in enumerate(text_chunks):

                chunk = {

                    "chunk_id": str(uuid.uuid4()),

                    "parent_document_id": document_id,

                    "chunk_index": index,

                    "total_chunks": total_chunks,

                    "content": chunk_text,

                    "metadata": {

                        **metadata,

                        "parent_document_id": document_id,

                        "chunk_index": index,

                        "total_chunks": total_chunks

                    }

                }

                all_chunks.append(chunk)

        return all_chunks

    # --------------------------------
    # 3. Save chunks
    # --------------------------------

    def save_chunks(self, chunks):
        with open(self.output_path,"w",encoding="utf-8") as file:
            json.dump(chunks,file,indent=4,ensure_ascii=False)
        print("\nChunks saved successfully!")
        print(f"Output: {self.output_path}")

    # --------------------------------
    # 4. Execute pipeline
    # --------------------------------

    def run(self):

        print("\nStarting Document Chunking...\n")

        documents = self.load_documents()

        print("Total documents:", len(documents))

        chunks = self.create_chunks(documents)

        self.save_chunks(chunks)

        print("\nChunking Summary")
        print("----------------------")

        print("Total documents:", len(documents))

        print("Total chunks:", len(chunks))

        print("Chunk size:", self.chunk_size)

        print("Chunk overlap:", self.chunk_overlap)

        return chunks


if __name__ == "__main__":

    chunker = DocumentChunker()

    chunker.run()