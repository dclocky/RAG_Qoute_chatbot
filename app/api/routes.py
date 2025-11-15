from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
from app.core.orchestrator import orchestrator

router = APIRouter()

@router.post("/upload")
async def upload_quote(file: UploadFile):
    text = (await file.read()).decode("utf-8")
    return JSONResponse(orchestrator.ingest_quote(text))

@router.post("/query")
async def process_query(query: str = Form(...)):
    return JSONResponse(orchestrator.process_query(query))


@router.get("/")
async def root():
    return {"status": "OK"}
