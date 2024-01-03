from sqlalchemy import Text  # variable length
from sqlalchemy import (Column, DateTime, ForeignKey, Integer,  # SmallInteger,
                        String)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_tg_id = Column(Integer, nullable=False, unique=True)
    tg_username = Column(String(250), nullable=False)
    tg_full_name = Column(String(250))

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_tg_id = Column(Integer, ForeignKey("users.id"))
    # user = relationship(User)
    ev_datetime = Column(DateTime)
    ev_title = Column(String(100))
    ev_tags = Column(Text)
    ev_text = Column(Text)

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_tg_id = Column(Integer, ForeignKey("users.id"))
    # user = relationship(User)
    note_title = Column(Text)
    note_text = Column(Text)
    note_tags = Column(Text)

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_tg_id = Column(Integer, ForeignKey("users.id"))
    # user = relationship(User)
    user_timezone = Column(String(20))  # Europe/Berlin etc...
    ai_platform = Column(String(50))
    ai_api_key = Column(String(100))
    calendar_event_duration = Column(Integer)

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Screenshot(Base):
    __tablename__ = "screenshots"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_tg_id = Column(Integer, ForeignKey("users.id"))
    file_id = Column(String(100))
    hashtags = Column(Text)
    caption = Column(Text)
    ocr_text = Column(Text)
    created = Column(DateTime)
