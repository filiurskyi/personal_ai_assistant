from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from bot.db_tools.database import show_all_notes
from fastapi_app.conf.config import DB_URI, templates
from db.conf import get_db
router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_class=HTMLResponse)
async def get_notes(request: Request, db: AsyncSession = Depends(get_db)):
    notes = await show_all_notes(db, 306067192)
    return templates.TemplateResponse(
        "notes.html", {"request": request, "notes": notes}
    )


@router.get("/{note_id}")
async def get_note(request: Request, note_id: int):
    pass


@router.put("/{note_id}")
async def put_note(request: Request, note_id: int):
    pass


@router.delete("/{note_id}")
async def delete_note(request: Request, note_id: int):
    pass
