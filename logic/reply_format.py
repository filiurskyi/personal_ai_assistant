import arrow
import json

from db_tools import database as db


async def user_context_handler(user_input: str, user_id, session):
    data = json.loads(user_input)
    if data.get("user_context", None) == "create_new_event":
        event_id = await db.add_event(session, user_id, data)
        return await display_event_card(event_id, session, user_id)
    else:
        return "None"


async def display_event_card(event_id, session, user_id):
    event = await db.show_one_event(session, event_id)
    card_id = event.id
    time = arrow.get(event.ev_datetime).to("Europe/Berlin").format("HH:mm")
    date = arrow.get(event.ev_datetime).to("Europe/Berlin").format("DD.MM.YYYY")
    title = event.ev_title
    tags = event.ev_tags
    text = event.ev_text

    message = f"""<i>Event details:</i> [{card_id}]
<b>{title}</b>
<i>{tags}</i>
on <b>{date}</b> at <b>{time}</b>
{text}"""
    return message
