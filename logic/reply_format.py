import json

from db_tools import database as db


async def user_context_handler(input: str, user_id, session):
    data = json.loads(input)
    if data.get("user_context", None) == "create_new_event":
        await db.add_event(session, user_id, data)
        return display_event_card(data)
    else:
        return "None"


def display_event_card(event_dic: dict):
    date = event_dic.get("ev_date", None)
    time = event_dic.get("ev_time", None)
    title = event_dic.get("ev_title", None)
    tags = event_dic.get("ev_tags", None)
    text = event_dic.get("ev_text", None)
    message = f"""<i>You created following event:</i>
<b>{title}</b>
<i>{tags}</i>
on <b>{date}</b> at <b>{time}</b>
{text}"""
    return message
