import json
import logging

import arrow

from db_tools import database as db


async def user_context_handler(user_input: str, user_id, session):
    data = json.loads(user_input)
    if data.get("user_context", None) == "create_new_event":
        event_id = await db.add_event(session, user_id, data)
        reply = await display_event_card(event_id, session, user_id)
        return reply
    elif data.get("user_context", None) == "create_new_note":
        note_id = await db.add_note(session, user_id, data)
        reply = await display_note_card(note_id, session, user_id)
        print(data)
        return reply
    else:
        return "None"


async def display_event_card(event_id, session, user_id):
    event = await db.show_one_event(session, event_id)
    user_tz = await db.get_user_tz(session, user_id)
    card_id = event.id
    time = arrow.get(event.ev_datetime).to(user_tz).format("HH:mm")
    date = arrow.get(event.ev_datetime).to(user_tz).format("DD.MM.YYYY")
    title = event.ev_title
    tags = event.ev_tags
    text = event.ev_text

    message = f"""<i>Event details:</i> [{card_id}]
<b>{title}</b>
<i>{tags}</i>
on <b>{date}</b> at <b>{time}</b>
{text}"""
    return message


async def display_note_card(note_id, session, user_id):
    note = await db.show_one_note(session, note_id)
    card_id = note.id
    title = note.note_title
    text = note.note_text
    tags = note.note_tags
    message = f"""<i>Note details:</i> [{card_id}]
<b>{title}</b>
<i>{tags}</i>
{text}"""
    return message
