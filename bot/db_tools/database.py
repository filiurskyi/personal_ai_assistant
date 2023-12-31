import asyncio
import datetime
from typing import Union

import arrow
from sqlalchemy import and_, or_, select
from db.conf import OPENAI_API_KEY
from db.models import Event, Note, Screenshot, Setting, User


async def old_user_check(session, tg_id) -> bool:
    """returns False if user exists"""
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar()
    if user_id:
        return False
    return True


async def add_user(session, tg_id, tg_username, tg_full_name) -> None:
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user = res.scalar()
    if not user:
        user = User(
            user_tg_id=tg_id, tg_username=tg_username, tg_full_name=tg_full_name
        )
        session.add(user)
        await session.commit()  # Commit the transaction here

    # Now that the user is committed, you can access user.user_tg_id
    res = await session.execute(select(Setting).filter_by(user_tg_id=user.user_tg_id))
    sett_user_id = res.scalar()
    if not sett_user_id:
        settings = Setting(
            user_tg_id=user.id,
            user_timezone="Europe/Berlin",
            ai_platform="openai",
            ai_api_key=OPENAI_API_KEY,
            calendar_event_duration=30,
        )
        session.add(settings)
        await session.commit()


async def get_user_default_event_duration(session, tg_id):
    # get user_id by tg_id
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id

    res = await session.execute(
        select(Setting.calendar_event_duration).filter_by(user_tg_id=user_id)
    )
    user_id = res.scalar()
    return user_id


async def get_user_tz(session, tg_id) -> Union[str, None]:
    # get user_id by tg_id
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id
    print(f"{user_id}")

    user_default_tz = await session.execute(
        select(Setting.user_timezone).filter_by(user_tg_id=user_id)
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
    if user_tz is not None:
        arrow_dt = arrow.get(date_time_str, date_time_format, tzinfo=user_tz).to("UTC")
    else:
        return None

    # add new event do db
    event = Event(
        user_tg_id=user_id,
        ev_datetime=arrow_dt.datetime.replace(tzinfo=None),
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
    scal = res.scalar()
    if not scal:
        return []

    user_id = scal.id
    events = await session.execute(select(Event).filter_by(user_tg_id=user_id))
    events = events.fetchall()
    events_list = [event[0] for event in events]
    return events_list


async def show_all_notes(session, tg_id) -> list:
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    scal = res.scalar()
    if not scal:
        return []

    user_id = scal.id
    notes = await session.execute(select(Note).filter_by(user_tg_id=user_id))
    notes = notes.fetchall()
    notes_list = [event[0] for event in notes]
    return notes_list


async def show_one_event(session, event_id: int):
    events = await session.execute(select(Event).filter_by(id=event_id))
    return events.scalar()


async def show_one_note(session, note_id):
    notes = await session.execute(select(Note).filter_by(id=note_id))
    return notes.scalar()


async def add_new_screenshot(session, tg_id, file_id, caption, ocr_text) -> int:
    if caption is not None:
        tags = [tag for tag in caption.split() if tag.startswith("#")]
        hashtags = " ".join(tags)
        caption = caption.lower()
    else:
        hashtags = None
    # get user_id by tg_id
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id
    screenshot = Screenshot(
        user_tg_id=user_id,
        file_id=file_id,
        hashtags=hashtags,
        caption=caption,
        ocr_text=ocr_text.lower() if ocr_text is not None else None,
        created_at=datetime.datetime.now(),
    )
    session.add(screenshot)
    await session.commit()
    return screenshot.id


async def find_screenshot(session, tg_id, prompt):
    # get user_id by tg_id
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id
    screenshot_id = await session.execute(
        select(Screenshot.id, Screenshot.file_id)
        .filter(
            or_(
                Screenshot.ocr_text.like("%" + prompt.lower() + "%"),
                Screenshot.hashtags.like("%" + prompt.lower() + "%"),
                Screenshot.caption.like("%" + prompt.lower() + "%"),
            )
        )
        .where(Screenshot.user_tg_id == user_id)
    )
    return screenshot_id.all()


async def delete_screenshot(session, tg_id: int, screenshot_id: str) -> bool:
    # get user_id by tg_id
    if not screenshot_id.isnumeric():
        return False
    else:
        screenshot_id = int(screenshot_id)
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    user_id = res.scalar().id

    screenshot_query = await session.execute(
        select(Screenshot).where(
            and_(Screenshot.id == screenshot_id, Screenshot.user_tg_id == user_id)
        )
    )
    screenshot = screenshot_query.scalar()
    if screenshot is not None:
        await session.delete(screenshot)
        await session.commit()
        return True
    else:
        return False


async def show_all_screenshots(session, tg_id) -> list:
    res = await session.execute(select(User).filter_by(user_tg_id=tg_id))
    if not res.scalar():
        return []

    user_id = res.scalar().id
    screenshots = await session.execute(select(Screenshot).filter_by(user_tg_id=user_id))
    screenshots = screenshots.fetchall()
    screenshots_list = [event[0] for event in screenshots]
    return screenshots_list
