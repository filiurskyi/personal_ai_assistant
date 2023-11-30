import arrow
from sqlalchemy import select

from db_tools.models import Event, Note, User


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


async def add_event(session, tg_id, event_dict: dict) -> None:
    # get user_id by tg_id
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id

    # ev_datetime
    user_default_tz = "Europe/Berlin"
    date_time_format = "DD.MM.YYYY HH:mm"
    date_time_str = event_dict.get("ev_datetime")
    arrow_dt = arrow.get(date_time_str, date_time_format, tzinfo=user_default_tz).to(
        "UTC"
    )

    # add new event do db
    event = Event(
        user_tg_id=user_id,
        ev_datetime=arrow_dt.datetime,
        ev_title=event_dict.get("ev_title"),
        ev_tags=event_dict.get("ev_tags"),
        ev_text=event_dict.get("ev_text"),
    )
    session.add(event)
    await session.commit()
    return event.id


async def add_note(session, tg_id, note_dict: dict):
    # get user_id by tg_id
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id

    # add new note do db
    note = Note(
        user_tg_id=user_id,
        note_title=note_dict.get("nt_title"),
        note_text=note_dict.get("nt_text"),
    )
    session.add(note)
    await session.commit()
    return note.id


async def delete_all_events(session, tg_id) -> None:
    events = await show_all_events(session, tg_id)
    for event in events:
        await session.delete(event)
        await session.commit()


async def show_all_events(session, tg_id) -> list:
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id

    events = await session.execute(select(Event).filter_by(user_tg_id=user_id))
    events = events.fetchall()
    events_list = [event[0] for event in events]
    return events_list


async def show_one_event(session, event_id):
    events = await session.execute(select(Event).filter_by(id=event_id))
    return events.scalar()


async def show_one_note(session, note_id):
    notes = await session.execute(select(Note).filter_by(id=note_id))
    return notes.scalar()

