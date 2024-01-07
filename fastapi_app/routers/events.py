from fastapi import APIRouter, Depends, Query
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (AsyncSession)

from db.conf import get_db
from db.models import Event
from fastapi_app.conf.config import templates
from fastapi_app.repository import events as repo_events

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_class=HTMLResponse)
async def list_events(request: Request, limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                      db: AsyncSession = Depends(get_db)):
    events = await repo_events.get_events(limit, offset, db)
    return templates.TemplateResponse(
        "events.html", {"request": request, "events": events}
    )


@router.get("/<event_id>", response_class=HTMLResponse)
async def list_event(event_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    events = await db.execute(select(Event))
    # return templates.TemplateResponse(
    #     "events.html", {"request": request, "events": events}
    # )
