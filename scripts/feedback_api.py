from pathlib import Path
from typing import Optional, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Reuse the CLI ingestion logic to avoid duplication
from scripts.add_feedback_to_kb import ingest_feedback
from core.nl_mapper import extract_structured_from_nl, map_to_bsp_custom_vars, map_to_agent_input


class IngestRequest(BaseModel):
    domain: Literal["ism", "bsp", "prs", "pds"]
    file_path: Optional[str] = Field(
        default=None, description="Absolute path to a generated document to ingest"
    )
    content: Optional[str] = Field(
        default=None, description="Raw text content to ingest if file_path is not provided"
    )
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    feedback_text: Optional[str] = None
    priority: Literal["low", "normal", "high", "urgent"] = "normal"
    verify_query: Optional[str] = None


app = FastAPI(title="Feedback Ingestion API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/feedback/ingest")
async def feedback_ingest(req: IngestRequest) -> dict:
    # Determine content: prefer file_path, else content
    content_source = None
    if req.file_path:
        path = Path(req.file_path)
        if not path.exists() or not path.is_file():
            raise HTTPException(status_code=400, detail=f"File not found: {req.file_path}")
        content_source = req.file_path
    elif req.content:
        # Write to a temp in-memory variable; the ingestion util expects a file path or content string.
        # We'll call the underlying ingest function with content directly by writing a small wrapper here.
        pass
    else:
        raise HTTPException(status_code=400, detail="Provide either file_path or content")

    # If raw content was provided, write to a temporary file to reuse the exact ingestion path
    temp_file: Optional[Path] = None
    try:
        if req.content and not req.file_path:
            temp_file = Path.cwd() / "_tmp_ingest.txt"
            temp_file.write_text(req.content, encoding="utf-8")
            content_source = str(temp_file)

        result = await ingest_feedback(
            domain=req.domain,
            file_path=content_source,
            session_id=req.session_id,
            user_id=req.user_id,
            feedback_text=req.feedback_text,
            priority=req.priority,
            verify_query=req.verify_query,
        )
        return result
    finally:
        if temp_file and temp_file.exists():
            try:
                temp_file.unlink()
            except Exception:
                pass


class NLMapRequest(BaseModel):
    text: str = Field(..., description="Natural language paragraph(s)")
    target: str = Field(
        default="bsp_custom_vars",
        description="Target mapping: 'bsp_custom_vars' or one of agent types: ism|bsp|pds|prs",
    )


@app.post("/nl/map")
async def nl_map(req: NLMapRequest) -> dict:
    extracted = extract_structured_from_nl(req.text)
    if req.target == "bsp_custom_vars":
        return {
            "extracted": extracted,
            "placeholders": map_to_bsp_custom_vars(extracted),
        }
    # Otherwise map to agent input skeleton
    placeholders = map_to_agent_input(req.target, extracted)
    return {"extracted": extracted, "agent_input": placeholders}


# Convenience: uvicorn entrypoint hint (run without reloader for simplicity)
#   /Users/allenliu/Desktop/ML-Project/AutocollableSNAgt/venv/bin/uvicorn scripts.feedback_api:app --host 0.0.0.0 --port 8000


