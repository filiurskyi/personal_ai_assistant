from datetime import datetime

from sqlalchemy import select

from db_tools.models import Base, Event, Setting, User


async def old_user_check(session, tg_id) -> bool:
    """returns False if user exists"""
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id
    if user_id:
        return False
    return True


async def add_user(session, tg_id, tg_username, tg_full_name) -> None:
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id
    if not user_id:
        user = User(
            user_tg_id=tg_id, tg_username=tg_username, tg_full_name=tg_full_name
        )
        session.add(user)
        await session.commit()


async def add_event(session, tg_id, event_dict: dict) -> None:
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id
    date_time_str = f"{event_dict.get('ev_date')} {event_dict.get('ev_time')}"
    date_time_format = "%d.%m.%Y %H:%M"
    event = Event(
        user_tg_id=user_id,
        ev_date=datetime.strptime(date_time_str, date_time_format).date(),
        ev_time=datetime.strptime(date_time_str, date_time_format).time(),
        ev_title=event_dict.get("ev_title"),
        ev_tags=event_dict.get("ev_tags"),
        ev_text=event_dict.get("ev_text"),
    )
    session.add(event)
    await session.commit()


async def show_all_events(session, tg_id) -> list:
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id
    
    events = await session.execute(select(Event).filter_by(user_tg_id=user_id))
    events = events.all()
    events_list = [event[0].as_dict() for event in events]
    return events_list


# if __name__ == "__main__":
#     initialize_database()
#     tg_id = 123456789
#     user_id = session.query(User).filter_by(user_tg_id=tg_id).first()
#     if not user_id:
#         user = User(user_tg_id=tg_id, tg_name="user123")
#         session.add(user)
#         user_id = session.query(User).filter_by(user_tg_id=tg_id).first()
#         session.commit()

#     date_time_str = "2023-01-01 12:00:00"
#     date_time_format = "%Y-%m-%d %H:%M:%S"
#     event_date = datetime.strptime(date_time_str, date_time_format).date()
#     event_time = datetime.strptime(date_time_str, date_time_format).time()

#     ev1 = Event(
#         user_tg_id=user_id.id,
#         ev_date=event_date,
#         ev_time=event_time,
#         ev_tags="#tag #tag1",
#         ev_text="Event text 1",
#     )
#     ev2 = Event(
#         user_tg_id=user_id.id,
#         ev_date=event_date,
#         ev_time=event_time,
#         ev_tags="#tag #tag1",
#         ev_text="Event text 2",
#     )

#     session.add(ev1)
#     session.add(ev2)
#     session.commit()
