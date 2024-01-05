import json
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import STATIC_PATH, templates
from .routers import events, login, notes

app = FastAPI()


app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")


app.include_router(login.router)
app.include_router(events.router)
app.include_router(notes.router)


@app.get("/", response_class=HTMLResponse)
async def list_events(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
