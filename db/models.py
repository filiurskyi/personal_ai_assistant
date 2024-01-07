from datetime import datetime

from sqlalchemy import (DateTime, ForeignKey, Integer,  # SmallInteger,
                        String)
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    user_tg_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    tg_username: Mapped[str] = mapped_column(String(250), nullable=False)
    tg_full_name: Mapped[str] = mapped_column(String(250))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    user_tg_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="events")
    ev_datetime: Mapped[datetime] = mapped_column(DateTime)
    ev_title: Mapped[str] = mapped_column(String(100))
    ev_tags: Mapped[str] = mapped_column(String())
    ev_text: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    user_tg_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="notes")
    note_title: Mapped[str] = mapped_column(String())
    note_text: Mapped[str] = mapped_column(String())
    note_tags: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Setting(Base):
    __tablename__ = "settings"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    user_tg_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="settings")
    user_timezone: Mapped[str] = mapped_column(String(20))  # Europe/Berlin etc...
    ai_platform: Mapped[str] = mapped_column(String(50))
    ai_api_key: Mapped[str] = mapped_column(String(100))
    calendar_event_duration: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Screenshot(Base):
    __tablename__ = "screenshots"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    user_tg_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="screenshots")
    file_id: Mapped[str] = mapped_column(String(100))
    hashtags: Mapped[str] = mapped_column(String(), nullable=True)
    caption: Mapped[str] = mapped_column(String(), nullable=True)
    ocr_text: Mapped[str] = mapped_column(String(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())


class Session(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    user_tg_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="sessions")
    session_id: Mapped[str] = mapped_column(String(100))  # uuid4 hash for verification
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
