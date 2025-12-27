# main.py

import os
import time
import uuid
import requests
import xml.etree.ElementTree as ET
import trafilatura
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import cohere
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import numpy as np

# -------------------------------------
# CONFIG
# -------------------------------------

SITEMAP_URL = "https://abdul-haseeb-dawood.github.io/AI-Physical-Book/sitemap.xml"
COLLECTION_NAME = "physical-ai-book"
MAX_CHARS = 1200
EMBED_BATCH_SIZE = 10
SLEEP_BETWEEN_BATCHES = 2
MAX_TEXT_LENGTH = 200_000

# Cohere
COHERE_API_KEY = "ECp0Gq0zlyihswblqqp56T6Ej6UKPQFsC0ocEh6I"
co = cohere.Client(COHERE_API_KEY)
EMBED_MODEL = "embed-english-v3.0"

# Qdrant
QDRANT_URL = "https://2134dfd0-9e1d-4561-9378-a3b7eecdd74d.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.jRMgTFfyIjn6d8v-ib5X2AF4MuwXYLI8m2ky75fLDaM"

qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    check_compatibility=False
)

# -------------------------------------
# TEXT EMBEDDING
# -------------------------------------

def get_embedding(text):
    res = co.embed(
        model=EMBED_MODEL,
        input_type="search_query",
        texts=[text]
    )
    return res.embeddings[0]

# -------------------------------------
# CHAT QUERY
# -------------------------------------

def semantic_search(query, top_k=3):
    query_emb = get_embedding(query)
    hits = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_emb,
        limit=top_k
    )
    # Extract text from payload
    results = [hit.payload["text"] for hit in hits]
    return results

# -------------------------------------
# FASTAPI APP
# -------------------------------------

app = FastAPI(
    title="RAG Chatbot API",
    description="API for the RAG chatbot system that answers questions based on book content",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Request model
class ChatRequest(BaseModel):
    query: str

# Response model
class ChatResponse(BaseModel):
    answer: str
    retrieved_docs: list

# Chat endpoint
@app.post("/chat/response", response_model=ChatResponse)
async def chat_response(request: ChatRequest):
    try:
        retrieved = semantic_search(request.query)
        if not retrieved:
            return ChatResponse(answer="I don't know.", retrieved_docs=[])
        
        # Combine top results as a simple answer
        answer = " ".join(retrieved)
        return ChatResponse(answer=answer, retrieved_docs=retrieved)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------
# RUN
# -------------------------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
