from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from rag.rag_pipeline import RAGPipeline

app=FastAPI( title="Sonu Portfolio AI API",
    description="AI-powered portfolio assistant",
    version="1.0.0")

pipeline=RAGPipeline()

class chatRequest(BaseModel):
    question:str

class chatResponse(BaseModel):
    answer:str

@app.get("/")
async def root():
    return {"message":"Welcome to Sonu Portfolio AI API"}

# API endpoint to handle chat requests
# @app.post("/chat")
# async def chat(request:chatRequest):
#     try:
#         answer=pipeline.get_answer(request.question)
#         return chatResponse(answer=answer)
#     except Exception:
#         raise HTTPException(status_code=500,detail="unable to genrate answer")

import logging

logging.basicConfig(level=logging.INFO)

@app.post("/chat")
async def chat(request: chatRequest):
    try:
        logging.info("Received question: %s", request.question)

        answer = pipeline.get_answer(request.question)

        logging.info("Answer generated successfully")
        return chatResponse(answer=answer)

    except Exception:
        logging.exception("ERROR INSIDE CHAT ENDPOINT")
        raise HTTPException(
            status_code=500,
            detail="Unable to generate answer"
        )
