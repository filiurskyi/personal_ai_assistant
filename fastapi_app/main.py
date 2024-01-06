from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from fastapi_app.conf.config import STATIC_PATH, templates
from .routers import events, login, notes

app = FastAPI()


app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")


app.include_router(login.router)
app.include_router(events.router)
app.include_router(notes.router)


@app.get("/", response_class=HTMLResponse)
async def list_events(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
