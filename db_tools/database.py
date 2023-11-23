# from datetime import datetime

from sqlalchemy import select

from db_tools.models import Base, Event, Setting, User


async def old_user_check(session, tg_id) -> bool:
    """returns False if user exists"""
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar()
    if user_id:
        return False
    return True


async def add_user(session, tg_id, tg_username, tg_full_name) -> None:
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar()
    if not user_id:
        user = User(
            user_tg_id=tg_id, tg_username=tg_username, tg_full_name=tg_full_name
        )
        session.add(user)
        await session.commit()


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
