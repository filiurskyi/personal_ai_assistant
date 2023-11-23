from datetime import datetime, timedelta

from ics import Calendar, Event


def generate_ics_file(events_list: list):
    # Create a Calendar
    cal = Calendar()
    default_event_duration = timedelta(hours=1.0)
    # Create an Event
    for event_dict in events_list:
        event = Event()
        event.name = event_dict.get("ev_title", None)
        event.begin = "2023-01-01T12:00:00"
        event.end = "2023-01-01T13:00:00"
        event.description = "Discuss project updates and goals."
        event.location = "Conference Room 123"

        # Add the event to the calendar
        cal.events.add(event)

    # Save the calendar to an .ics file
    with open("./temp/calendar.ics", "w") as f:
        f.writelines(cal)
    return "./temp/calendar.ics"
