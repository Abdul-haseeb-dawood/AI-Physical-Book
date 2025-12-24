import os
import time
import uuid
import requests
import xml.etree.ElementTree as ET
import trafilatura
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import cohere
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat_routes import router as chat_router
from config.settings import settings
import uvicorn


app = FastAPI(
    title="RAG Chatbot API",
    description="API for the RAG chatbot system that answers questions based on book content",
    version="1.0.0"
)

SITEMAP_URL = "https://abdul-haseeb-dawood.github.io/AI-Physical-Book/sitemap.xml"
COLLECTION_NAME = "physical-ai-book"

MAX_CHARS = 1200
EMBED_BATCH_SIZE = 10          # 🔑 RATE SAFE
SLEEP_BETWEEN_BATCHES = 2      # 🔑 RATE SAFE
MAX_TEXT_LENGTH = 200_000

# -------------------------------------
# COHERE
# -------------------------------------

COHERE_API_KEY = "ECp0Gq0zlyihswblqqp56T6Ej6UKPQFsC0ocEh6I"
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY not set")

co = cohere.Client(COHERE_API_KEY)
EMBED_MODEL = "embed-english-v3.0"

# -------------------------------------
# QDRANT
# -------------------------------------

QDRANT_URL = "https://2134dfd0-9e1d-4561-9378-a3b7eecdd74d.europe-west3-0.gcp.cloud.qdrant.io:6333" \
""
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.jRMgTFfyIjn6d8v-ib5X2AF4MuwXYLI8m2ky75fLDaM"

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("QDRANT credentials not set")

qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    check_compatibility=False
)

# -------------------------------------
# SITEMAP
# -------------------------------------

def get_all_urls():
    r = requests.get(SITEMAP_URL, timeout=20)
    r.raise_for_status()
    root = ET.fromstring(r.text)

    urls = set()
    for child in root:
        loc = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc is not None and "/docs/" in loc.text:
            urls.add(loc.text.strip())

    return list(urls)

# -------------------------------------
# TEXT EXTRACTION
# -------------------------------------

def extract_text(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    if r.status_code != 200:
        return None

    text = trafilatura.extract(r.text)
    if not text:
        return None

    text = text.strip()
    return text[:MAX_TEXT_LENGTH]

# -------------------------------------
# SAFE CHUNKING
# -------------------------------------

def chunk_text(text):
    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + MAX_CHARS, n)
        chunk = text[start:end]

        dot = chunk.rfind(". ")
        if dot != -1 and end < n:
            end = start + dot + 1
            chunk = text[start:end]

        chunk = chunk.strip()
        if len(chunk) > 150:
            chunks.append(chunk)

        start = end

    return chunks

# -------------------------------------
# BATCH EMBEDDING (RATE SAFE)
# -------------------------------------

def embed_batch(texts):
    while True:
        try:
            res = co.embed(
                model=EMBED_MODEL,
                input_type="search_document",
                texts=texts
            )
            return res.embeddings

        except cohere.errors.TooManyRequestsError:
            print("⚠️ Cohere rate limit hit — sleeping 10s")
            time.sleep(10)

# -------------------------------------
# QDRANT
# -------------------------------------

def create_collection():
    if not qdrant.collection_exists(COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=1024,
                distance=Distance.COSINE
            )
        )
        print("✅ Collection created")
    else:
        print("ℹ️ Collection already exists")

def save_batch(chunks, embeddings, url):
    points = []

    for text, vector in zip(chunks, embeddings):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "url": url,
                    "text": text
                }
            )
        )

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

# -------------------------------------
# MAIN PIPELINE
# -------------------------------------

def ingest():
    urls = get_all_urls()
    create_collection()

    total = 0

    for url in urls:
        print(f"\nProcessing: {url}")
        text = extract_text(url)
        if not text:
            continue

        chunks = chunk_text(text)

        for i in range(0, len(chunks), EMBED_BATCH_SIZE):
            batch = chunks[i:i + EMBED_BATCH_SIZE]
            embeddings = embed_batch(batch)
            save_batch(batch, embeddings, url)

            total += len(batch)
            print(f"  ✔ Saved {total} chunks")

            time.sleep(SLEEP_BETWEEN_BATCHES)

    print("\n✅ INGESTION COMPLETED")
    print("Total chunks:", total)

# -------------------------------------
# RUN
# -------------------------------------

def create_app():
    app = FastAPI(
        title="RAG Chatbot API",
        description="API for the RAG chatbot system that answers questions based on book content",
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify your frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(chat_router)

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app

app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
    ingest()