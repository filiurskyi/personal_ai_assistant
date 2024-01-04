from datetime import timedelta
from typing import List, Type

import arrow
from ics import Calendar, Event

from db.models import Base


def generate_ics_file(events_list: List[Type[Base]], event_duration=30):
    # Create a Calendar
    cal = Calendar()

    # Create an Event
    for event_dict in events_list:
        evn = event_dict.as_dict()
        event = Event()
        event.name = evn.get("ev_title")
        event.begin = arrow.get(evn.get("ev_datetime"))
        event.duration = timedelta(minutes=event_duration)
        event.description = evn.get("ev_text") + "\n\n" + evn.get("ev_tags")

        cal.events.add(event)
    with open("./temp/calendar.ics", "w", encoding="utf-8") as f:
        f.writelines(cal.serialize())

    return "./temp/calendar.ics"
