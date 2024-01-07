from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Event
from fastapi_app.schemas.events import EventCreateSchema
from fastapi import Path, Query


async def get_events(limit: int, offset: int, db: AsyncSession):
    stmt = select(Event).offset(offset).limit(limit)
    events = await db.execute(stmt)
    return events.scalars().all()


async def get_event(event_id: int, db: AsyncSession):
    stmt = select(Event).filter_by(id=event_id)
    events = await db.execute(stmt)
    return events.scalar_one_or_none()


async def create_event(body: EventCreateSchema, db: AsyncSession):
    event = Event(**body.model_dump())
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


async def update_event(db: AsyncSession):
    ...


async def delete_event(db: AsyncSession):
    ...
