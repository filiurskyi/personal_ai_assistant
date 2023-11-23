from datetime import datetime, timedelta
from typing import List, Type

from ics import Calendar, Event

from db_tools.models import Base


def generate_ics_file(events_list: List[Type[Base]]):
    # Create a Calendar
    cal = Calendar()
    default_event_duration = timedelta(hours=1.0)
    # Create an Event
    date_time_format = "%Y-%m-%d %H:%M:%S"
    date_time_ics = "%Y-%m-dT%H:M:%s"
    for event_dict in events_list:
        evn = event_dict.as_dict()
        event = Event()
        date_time_str = f"{evn.get('ev_date')} {evn.get('ev_time')}"
        event.name = evn.get("ev_title")
        event.begin = datetime.strptime(date_time_str, date_time_format)
        event.end = (event.begin + default_event_duration)
        event.description = evn.get("ev_text") + "\n\n" + evn.get("ev_tags")

        cal.events.add(event)
        print("-------------cal-------------\n", cal)
    with open("./temp/calendar.ics", "w", encoding="utf-8") as f:
        f.writelines(str(cal))

    return "./temp/calendar.ics"
