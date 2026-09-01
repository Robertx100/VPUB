import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

# Load environment
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_FILE = BASE_DIR / os.getenv("DATA_FILE", "data/subscribers.json")
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
if not DATA_FILE.exists():
    DATA_FILE.write_text("[]", encoding="utf-8")

app = FastAPI(
    title="vpublication",
    description="Interactive books instead of flat PDFs — vpub",
    version="0.1.0",
    docs_url=None,  # Disabled for landing page
    redoc_url=None,
)

# Static files
app.mount("/static", StaticFiles(directory=BASE_DIR / "app/static"), name="static")

# Templates
templates = Jinja2Templates(directory=BASE_DIR / "app/templates")

# Simple email regex validator
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


def get_subscribers() -> list[dict]:
    try:
        if DATA_FILE.exists():
            content = DATA_FILE.read_text(encoding="utf-8").strip()
            if content:
                return json.loads(content)
    except Exception:
        pass
    return []


def save_subscribers(subs: list[dict]) -> None:
    temp_file = DATA_FILE.with_suffix(".tmp")
    temp_file.write_text(json.dumps(subs, indent=2, ensure_ascii=False), encoding="utf-8")
    temp_file.replace(DATA_FILE)


@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "page_title": "vpublication — Interactive books, not flat PDFs",
            "meta_description": "Transform static PDFs and manuscripts into living, responsive, interactive publications. Discover vpub today.",
        },
    )


@app.post("/api/subscribe", response_class=HTMLResponse)
async def subscribe_email(
    request: Request,
    email: Annotated[str, Form()],
    hp_field: Annotated[str, Form()] = "",
):
    # Bot / Honeypot check
    if hp_field.strip():
        # Silently return success to confuse automated bots
        return templates.TemplateResponse(
            request=request,
            name="partials/subscribe_response.html",
            context={
                "status": "success",
                "message": "Welcome aboard! You're on the early access list.",
            },
        )

    clean_email = email.strip().lower()
    if not clean_email or not EMAIL_REGEX.match(clean_email):
        return templates.TemplateResponse(
            request=request,
            name="partials/subscribe_response.html",
            context={
                "status": "error",
                "message": "Please enter a valid email address.",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    subs = get_subscribers()
    existing_emails = {s.get("email") for s in subs if isinstance(s, dict)}

    if clean_email in existing_emails:
        return templates.TemplateResponse(
            request=request,
            name="partials/subscribe_response.html",
            context={
                "status": "success",
                "message": "You're already on the priority list! We'll be in touch shortly.",
            },
        )

    new_sub = {
        "email": clean_email,
        "subscribed_at": datetime.now(timezone.utc).isoformat(),
        "ip": request.client.host if request.client else None,
    }
    subs.append(new_sub)
    save_subscribers(subs)

    return templates.TemplateResponse(
        request=request,
        name="partials/subscribe_response.html",
        context={
            "status": "success",
            "message": "You're in! We've saved your spot for early access to vpub.",
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={"page_title": "Page Not Found — vpublication"},
            status_code=404,
        )
    return templates.TemplateResponse(
        request=request,
        name="500.html",
        context={"page_title": "Error — vpublication", "error_code": exc.status_code},
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(
        request=request,
        name="500.html",
        context={"page_title": "Server Error — vpublication", "error_code": 500},
        status_code=500,
    )


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
