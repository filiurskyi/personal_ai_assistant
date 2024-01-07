from datetime import datetime

from pydantic import BaseModel, Field


class EventCreateSchema(BaseModel):
    ev_datetime: datetime = Field()
    ev_title: str = Field(min_length=1, max_length=100)
    ev_tags: str = Field(min_length=1, max_length=500)
    ev_text: str = Field(min_length=1, max_length=10000)


class EventResponseSchema(EventCreateSchema):
    id: int = Field(1, ge=1)
    user_tg_id: int = Field(1, ge=1)
    created_at: datetime = Field()

    class Config:
        from_attributes = True
