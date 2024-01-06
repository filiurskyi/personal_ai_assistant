from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from bot.db_tools.database import show_all_events
from fastapi_app.conf.config import DB_URI, templates

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_class=HTMLResponse)
async def list_events(request: Request):
    engine = create_async_engine(DB_URI, echo=False)
    sessionmaker = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with sessionmaker() as session:
        events = await show_all_events(session, 306067192)

    return templates.TemplateResponse(
        "events.html", {"request": request, "events": events}
    )
