from fastapi import Depends, FastAPI, File, Form, HTTPException, Security, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from agent import run_agent
import shutil
import os
import json
import hmac
import uuid

def load_env_file(env_path: str = ".env") -> None:
    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


load_env_file()

EXPECTED_API_KEY = os.getenv("SMARTHIRE_API_KEY")
if not EXPECTED_API_KEY:
    raise RuntimeError("SMARTHIRE_API_KEY is missing. Set it in .env before starting the API.")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(api_key: str | None = Security(api_key_header)) -> str:
    if not api_key or not hmac.compare_digest(api_key, EXPECTED_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key"
        )
    return api_key

app = FastAPI(
    title="SmartHire AI Agent",
    description="AI-powered recruitment agent for SmartHire",
    version="1.0.0"
)

ALLOWED_CORS_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_CORS_ORIGINS,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/", dependencies=[Depends(require_api_key)])
def home():
    return {
        "message": "SmartHire AI Agent is running",
        "version": "1.0.0",
        "endpoints": [
            "POST /score-resume",
            "POST /rank-candidates",
            "POST /chat"
        ]
    }

@app.post("/score-resume", dependencies=[Depends(require_api_key)])
async def score_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    safe_name = os.path.basename(file.filename)
    temp_path = f"temp_{uuid.uuid4().hex}_{safe_name}"

    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        result = run_agent(
            "score",
            file_path=temp_path,
            job_description=job_description
        )
        return result
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/rank-candidates", dependencies=[Depends(require_api_key)])
async def rank_candidates(
    candidates: str = Form(...),
    top_n: int = Form(5)
):
    try:
        candidates_list = json.loads(candidates)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="`candidates` must be valid JSON") from exc

    if not isinstance(candidates_list, list):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="`candidates` must be a JSON array")
    
    result = run_agent(
        "rank",
        candidates=candidates_list,
        top_n=top_n
    )
    
    return result

@app.post("/chat", dependencies=[Depends(require_api_key)])
async def chat(
    job_description: str = Form(...),
    question: str = Form(...)
):
    result = run_agent(
        "chat",
        job_description=job_description,
        question=question
    )
    
    return result

