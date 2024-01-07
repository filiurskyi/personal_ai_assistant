from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from bot.db_tools.database import show_all_events
from db.conf import get_db
from fastapi_app.conf.config import DB_URI, templates

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_class=HTMLResponse)
async def list_events(request: Request, db: AsyncSession = Depends(get_db)):
    events = await show_all_events(db, 306067192)

    return templates.TemplateResponse(
        "events.html", {"request": request, "events": events}
    )
