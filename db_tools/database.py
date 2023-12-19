import datetime

import arrow
from sqlalchemy import select, and_

from db_tools.models import Event, Note, Screenshot, Setting, User


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
        settings = Setting(
            user_tg_id=tg_id,
            user_timezone="Europe/Berlin",
            ai_platform="openai",
            ai_api_key=None,
            calendar_event_duration=30,
        )
        session.add(user)
        session.add(settings)
        await session.commit()


async def get_user_default_event_duration(session, tg_id):
    res = await session.execute(
        select(Setting.calendar_event_duration).filter_by(user_tg_id=tg_id)
    )
    user_id = res.scalar()
    return user_id


async def get_user_tz(session, tg_id):
    user_default_tz = await session.execute(
        select(Setting.user_timezone).filter_by(user_tg_id=tg_id)
    )
    return user_default_tz.fetchone()[0]


async def add_event(session, tg_id, event_dict: dict) -> None:
    # get user_id by tg_id
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id

    # ev_datetime
    user_tz = await get_user_tz(session, tg_id)
    date_time_format = "DD.MM.YYYY HH:mm"
    date_time_str = event_dict.get("ev_datetime")
    arrow_dt = arrow.get(date_time_str, date_time_format, tzinfo=user_tz).to("UTC")

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
        note_tags=note_dict.get("nt_tags"),
    )
    session.add(note)
    await session.commit()
    return note.id


async def delete_all_events(session, tg_id) -> None:
    events = await show_all_events(session, tg_id)
    for event in events:
        await session.delete(event)
        await session.commit()


async def del_all_notes(session, tg_id) -> None:
    notes = await show_all_notes(session, tg_id)
    for note in notes:
        await session.delete(note)
        await session.commit()


async def show_all_events(session, tg_id) -> list:
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id

    events = await session.execute(select(Event).filter_by(user_tg_id=user_id))
    events = events.fetchall()
    events_list = [event[0] for event in events]
    return events_list


async def show_all_notes(session, tg_id) -> list:
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id

    notes = await session.execute(select(Note).filter_by(user_tg_id=user_id))
    notes = notes.fetchall()
    notes_list = [event[0] for event in notes]
    return notes_list


async def show_one_event(session, event_id):
    events = await session.execute(select(Event).filter_by(id=event_id))
    return events.scalar()


async def show_one_note(session, note_id):
    notes = await session.execute(select(Note).filter_by(id=note_id))
    return notes.scalar()


async def add_new_screenshot(session, tg_id, file_id, caption, ocr_text) -> int:
    tags = [tag for tag in caption.split() if tag.startswith("#")]
    hashtags = " ".join(tags)
    screenshot = Screenshot(
        user_tg_id=tg_id,
        file_id=file_id,
        hashtags=hashtags,
        caption=caption.lower(),
        ocr_text=ocr_text.lower(),
        created=datetime.datetime.now(),
    )
    session.add(screenshot)
    await session.commit()
    return screenshot.id


async def find_screenshot(session, tg_id, prompt):
    screenshot_id = await session.execute(
        select(Screenshot.id, Screenshot.file_id)
        .filter(Screenshot.ocr_text
                .like("%" + prompt.lower() + "%"))
        .where(Screenshot.user_tg_id == tg_id)
    )
    return screenshot_id.all()


async def delete_screenshot(session, tg_id, screenshot_id) -> bool:
    screenshot_query = await session.execute(
        select(Screenshot)
        .where(and_(Screenshot.id == screenshot_id, Screenshot.user_tg_id == tg_id))
    )
    screenshot = screenshot_query.scalar()
    if screenshot is not None:
        await session.delete(screenshot)
        await session.commit()
        return True
    else:
        return False
