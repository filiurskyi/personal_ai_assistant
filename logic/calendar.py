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
    # date_time_ics = "%Y-%m-dT%H:M:%S"
    for event_dict in events_list:
        evn = event_dict.as_dict()
        event = Event()
        date_time_str = f"{evn.get('ev_date')} {evn.get('ev_time')}"
        event.name = evn.get("ev_title")
        print(event.name)
        event.begin = datetime.strptime(date_time_str, date_time_format)
        print(event.begin)
        event.end = event.begin + default_event_duration
        print(event.end)
        event.description = evn.get("ev_text") + "\n\n" + evn.get("ev_tags")
        print(event.description)
        # event.location = ""

        # cal.events.add(event)

    # Save the calendar to an .ics file
    with open("./temp/calendar.ics", "w") as f:
        f.writelines(cal)
    return "./temp/calendar.ics"
