from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
import string, random
from dotenv import load_dotenv
import os


from db import SessionLocal, init_db
from models import ShortURL

app = FastAPI(title="URL Shortener")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용: 모두 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ShortenRequest(BaseModel):
    url: HttpUrl


class ShortenResponse(BaseModel):
    short_code: str
    short_url: str


def generate_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/shorten", response_model=ShortenResponse)
def shorten(req: ShortenRequest, db: Session = Depends(get_db)):
    # 중복 URL 처리 방식은 자유 (같은 URL이면 이전 코드 재사용 등)
    code = generate_code()
    short = ShortURL(short_code=code, original_url=str(req.url))
    db.add(short)
    db.commit()
    db.refresh(short)

    load_dotenv()
    DOMAIN = os.getenv("DOMAIN")

    return ShortenResponse(
        short_code=short.short_code,
        short_url=f"{DOMAIN}{short.short_code}",
    )


@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    short = db.query(ShortURL).filter(ShortURL.short_code == code).first()
    if not short:
        raise HTTPException(status_code=404, detail="Short URL not found")
    short.hit_count += 1
    db.commit()
    return RedirectResponse(short.original_url)


@app.get("/stats/{code}")
def stats(code: str, db: Session = Depends(get_db)):
    short = db.query(ShortURL).filter(ShortURL.short_code == code).first()
    if not short:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return {
        "original_url": short.original_url,
        "hit_count": short.hit_count,
        "created_at": short.created_at,
    }


from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
from fastapi import Request

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["endpoint"])


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    endpoint = request.url.path
    method = request.method

    with REQUEST_LATENCY.labels(endpoint=endpoint).time():
        response = await call_next(request)

    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=response.status_code).inc()
    return response


@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type="text/plain; version=0.0.4")
