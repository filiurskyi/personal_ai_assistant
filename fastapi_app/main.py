import json
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from urllib.parse import unquote, parse_qs

from db.models import User, Event, Note, Setting, Screenshot
from bot.db_tools.database import show_all_events, show_all_notes

app = FastAPI()

# Mount the "static" directory to serve static files (e.g., CSS, JS)
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="fastapi_app/templates")


DB_URI = "sqlite+aiosqlite:///database.db/"




@app.get("/", response_class=HTMLResponse)
async def list_events(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/events", response_class=HTMLResponse)
async def list_events(request: Request):
    engine = create_async_engine(DB_URI, echo=False)
    sessionmaker = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with sessionmaker() as session:
        events = await show_all_events(session, 306067192)

    return templates.TemplateResponse("events.html", {"request": request, "events": events})


@app.get("/notes", response_class=HTMLResponse)
async def list_notes(request: Request):
    engine = create_async_engine(DB_URI, echo=False)
    sessionmaker = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with sessionmaker() as session:
        notes = await show_all_notes(session, 306067192)
    return templates.TemplateResponse("notes.html", {"request": request, "notes": notes})


# @app.post("/login", response_class=HTMLResponse)
# async def login_tg(request: Request):
#     data = await request.json()
#     print(parse_qs(unquote(data.get("initData"))))
#     return templates.TemplateResponse("events.html", {"request": request})


@app.get("/login-tg", response_class=HTMLResponse)
async def login_tg(request: Request):
    try:
        data = await request.json()
        print(" get ", parse_qs(unquote(data.get("initData"))))
    except Exception as e:
        print(e)
    return templates.TemplateResponse("login-tg.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    try:
        data = await request.json()
        print(" post ", parse_qs(unquote(data.get("initData"))))
    except Exception as e:
        print(e)
    return templates.TemplateResponse("login.html", {"request": request})
    # return RedirectResponse(url="login")
