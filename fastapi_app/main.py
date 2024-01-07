from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db.conf import get_db
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


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
