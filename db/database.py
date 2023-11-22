from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    SmallInteger,
    Time,  # is datetime.time()
    Text,  # variable length
    Date,  # is datetime.date()
    String,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

# from bot import PG_PWD


engine = create_engine(
    "sqlite:///database.db",
    echo=True,
)

DBSession = sessionmaker(bind=engine)
session = DBSession()

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


Base.metadata.create_all(engine)
Base.metadata.bind = engine

tg_id = 123456789
# user = User(user_tg_id=tg_id, tg_name="user123")
# session.add(user)
# session.commit()

user_id = session.query(User).filter_by(user_tg_id=tg_id).first().id


date_time_str = "2023-01-01 12:00:00"
date_time_format = "%Y-%m-%d %H:%M:%S"
event_date = datetime.strptime(date_time_str, date_time_format).date()
event_time = datetime.strptime(date_time_str, date_time_format).time()


ev1 = Event(
    user_tg_id=user_id,
    ev_date=event_date,
    ev_time=event_time,
    ev_tags="#tag #tag1",
    ev_text="Event text 1",
)
ev2 = Event(
    user_tg_id=user_id,
    ev_date=event_date,
    ev_time=event_time,
    ev_tags="#tag #tag1",
    ev_text="Event text 2",
)

session.add(ev1)
session.add(ev2)
session.commit()
