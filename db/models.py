from sqlalchemy import (
    Column,
    Integer,
    SmallInteger,
    Time,  # is datetime.time()
    Text,  # variable length
    Date,  # is datetime.date()
    String,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_tg_id = Column(Integer, nullable=False, unique=True)
    tg_name = Column(String(250), nullable=False)


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_tg_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User)
    ev_date = Column(Date)
    ev_time = Column(Time)
    ev_title = Column(String(100))
    ev_tags = Column(Text)
    ev_text = Column(Text)


class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_tg_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User)
    language = Column(String(2))  # en, ua, ru, de etc...
    ai_platform = Column(String(50))
    ai_api_key = Column(String(100))