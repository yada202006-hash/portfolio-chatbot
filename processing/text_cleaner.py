import json
import re
import hashlib

from pathlib import Path


class TextCleaner:

    def __init__(self):

        self.input_path = Path(
            "data/processed/document.json"
        )

        self.output_path = Path(
            "data/processed/cleaned_documents.json"
        )

    # --------------------------------
    # 1. Normalize text
    # --------------------------------

    def normalize_text(self, text):

        if not isinstance(text, str):
            return ""

        # Normalize line endings
        text = text.replace("\r\n", "\n")

        # Remove null characters
        text = text.replace("\x00", "")

        # Remove excessive spaces
        text = re.sub(r"[ \t]+", " ", text)

        # Normalize excessive newlines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove unnecessary spaces around lines
        lines = [
            line.strip()
            for line in text.split("\n")
        ]

        text = "\n".join(lines)

        return text.strip()

    # --------------------------------
    # 2. Load documents
    # --------------------------------

    def load_documents(self):

        with open(
            self.input_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    # --------------------------------
    # 3. Remove empty documents
    # --------------------------------

    def remove_empty_documents(self, documents):

        cleaned = []

        for document in documents:

            content = document.get("content", "")

            if content and content.strip():

                cleaned.append(document)

        return cleaned

    # --------------------------------
    # 4. Remove duplicate documents
    # --------------------------------

    def remove_duplicates(self, documents):

        unique_documents = []

        seen_hashes = set()

        for document in documents:

            content = document["content"]

            content_hash = hashlib.sha256(
                content.encode("utf-8")
            ).hexdigest()

            if content_hash not in seen_hashes:

                seen_hashes.add(content_hash)

                unique_documents.append(document)

        return unique_documents

    # --------------------------------
    # 5. Clean documents
    # --------------------------------

    def clean_documents(self, documents):

        cleaned_documents = []

        for document in documents:

            cleaned_content = self.normalize_text(
                document.get("content", "")
            )

            if not cleaned_content:
                continue

            cleaned_document = {

                "id": document["id"],

                "content": cleaned_content,

                "metadata": document.get("metadata", {})

            }

            cleaned_documents.append(cleaned_document)

        return cleaned_documents

    # --------------------------------
    # 6. Save documents
    # --------------------------------

    def save_documents(self, documents):

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                documents,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("\nCleaned documents saved successfully!")

        print(f"Output: {self.output_path}")

    # --------------------------------
    # 7. Execute pipeline
    # --------------------------------

    def run(self):

        print("\nStarting Text Cleaning...\n")

        documents = self.load_documents()

        original_count = len(documents)

        documents = self.clean_documents(documents)

        documents = self.remove_empty_documents(documents)

        documents = self.remove_duplicates(documents)

        self.save_documents(documents)

        print("\nCleaning Summary")
        print("----------------------")

        print("Original documents:", original_count)

        print("Cleaned documents:", len(documents))

        print(
            "Removed documents:",
            original_count - len(documents)
        )

        return documents


if __name__ == "__main__":

    cleaner = TextCleaner()

    cleaner.run()