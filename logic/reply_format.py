import json

def user_context_handler(input: str):
    data = json.loads(input)
    if data.get("user_context", None) == "create_new_event":
        return display_event_card(data)
    else:
        return None

def display_event_card(event_dic: dict):
    date = event_dic.get("ev_date")
    time = event_dic.get("ev_time")
    tags = event_dic.get("ev_tags")
    text = event_dic.get("ev_text")
    message=f"""<i>You created following event:</i>
    date: <b>{date}</b>
    time: <b>{time}</b>
    tags: <b>{tags}</b>
    text: <b>{text}</b>
    """
    return message