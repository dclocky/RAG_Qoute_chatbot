from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Supplier Quote Multi-Agent RAG System",
    version="1.0.0"
)

app.include_router(router)
