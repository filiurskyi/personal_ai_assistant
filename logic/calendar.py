from datetime import timedelta
from typing import List, Type

import arrow
from ics import Calendar, Event

from db_tools.models import Base


def generate_ics_file(events_list: List[Type[Base]]):
    # Create a Calendar
    cal = Calendar()
    default_event_duration = timedelta(minutes=30)
    default_time_zone = "Europe/Berlin"
    # Create an Event
    date_time_format = "YYYY-MM-DD HH:mm:ss"
    for event_dict in events_list:
        evn = event_dict.as_dict()
        event = Event()
        event.name = evn.get("ev_title")
        event.begin = arrow.get(evn.get("ev_datetime"))
        event.duration = default_event_duration
        event.description = evn.get("ev_text") + "\n\n" + evn.get("ev_tags")

        cal.events.add(event)
    with open("./temp/calendar.ics", "w", encoding="utf-8") as f:
        f.writelines(cal.serialize())

    return "./temp/calendar.ics"
