# Sonu Portfolio AI

Sonu Portfolio AI is a retrieval-augmented generation (RAG) assistant for answering questions about Sonu Yadav's professional profile, skills, education, experience, and projects. It exposes a FastAPI endpoint and also includes a command-line chat interface.

The assistant retrieves relevant information from a local Chroma vector database and uses the Groq API (through LangChain's OpenAI-compatible client) to draft an answer. Its prompt instructs the model to answer from retrieved portfolio data and to say when information is unavailable.

## Features

- FastAPI chat endpoint with interactive API documentation.
- Semantic search over portfolio documents using Chroma and sentence-transformer embeddings.
- Data-processing stages for consolidating, cleaning, and chunking portfolio information.
- Command-line RAG chat and document retrieval utilities.

## Project structure

```text
api/
  main.py                       FastAPI application
ingestion/
  github_collector.py           GitHub API helper
  linkedin_collector.py         LinkedIn collector (currently empty)
processing/
  data_conslidation.py          Combines prepared GitHub and LinkedIn JSON
  document_processor.py         Converts consolidated data to documents
  text_cleaner.py               Cleans and deduplicates documents
  chunker.py                    Splits documents into overlapping chunks
  embedding_genrator.py         Embeds chunks and stores them in Chroma
rag/
  rag_pipeline.py               Coordinates retrieval and answer generation
  rag_retriever.py              Searches the vector store
  genrator.py                   Calls the language model and refines answers
data/
  raw/                          Source profile data
  processed/                    Intermediate documents and chunks
  vector_db/                    Local Chroma database
requirements.txt                Python dependencies
```

The filenames `data_conslidation.py`, `embedding_genrator.py`, and `genrator.py` are spelled this way in the current project.

## Requirements

- Python with support for the pinned packages in `requirements.txt`.
- A Groq API key for generating answers.
- Internet access the first time the embedding model is loaded, so it can be downloaded.

## Setup

From the project root, create and activate a virtual environment on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root and set your key:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Do not commit `.env` or real API keys. The GitHub collector also reads `GITHUB_USERNAME` and `GITHUB_TOKEN` from the environment, but the current repository does not provide a complete, runnable ingestion workflow for collecting all source data.

## Prepare the knowledge base

The processing scripts expect prepared JSON files in these locations:

- `data/raw/github/profile.json`
- `data/raw/github/repositories.json`
- `data/raw/github/projects.json`
- `data/raw/linkedin/linkedin_profile.json`

The profile JSON should contain the fields expected by `processing/data_conslidation.py`. To process the data, run these commands from the project root:

```powershell
python -m processing.data_conslidation
```

There is currently a path mismatch between the consolidation and document-processing stages: the consolidator writes to `data/raw/processed/consolidated_data.json`, while the document processor reads `data/processed/consolidated_data.json`. Copy the generated file to the path expected by the processor before continuing:

```powershell
New-Item -ItemType Directory -Force data\processed
Copy-Item data\raw\processed\consolidated_data.json data\processed\consolidated_data.json
```

Then run the remaining stages in order:

```powershell
python -m processing.document_processor
python -m processing.text_cleaner
python -m processing.chunker
python -m processing.embedding_genrator
```

This generates cleaned documents and chunks under `data/processed/` and builds the local vector store under `data/vector_db/`. The LinkedIn collector is currently empty, and the GitHub collector only provides helper methods; obtain or prepare the source JSON files before running this pipeline.

## Run the API

Start the development server from the project root:

```powershell
python -m uvicorn api.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/` | Welcome message |
| `POST` | `/chat` | Ask a portfolio question |

Example request:

```http
POST /chat
Content-Type: application/json
```

```json
{
  "question": "What projects has Sonu worked on?"
}
```

The response contains an `answer` string. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Command-line tools

Start an interactive RAG chat:

```powershell
python -m rag.rag_pipeline
```

Run the standalone retriever to inspect matching chunks:

```powershell
python -m rag.rag_retriever
```

Both tools require a populated vector store. Answer generation also requires `GROQ_API_KEY`.

## Notes

- The embedding model is `sentence-transformers/all-MiniLM-L6-v2`; the first run may download model files.
- The vector store is persisted locally in `data/vector_db/`.
- Portfolio source files and generated vector data can contain personal information. Keep them private unless you intend to publish them.
- If an API request fails, check that `GROQ_API_KEY` is set and that `data/vector_db/` contains the expected Chroma collection.
