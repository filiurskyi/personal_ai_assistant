from ics import Calendar, Event


def generate_ics_file():
    # Create a Calendar
    cal = Calendar()

    # Create an Event
    event = Event()
    event.name = "Meeting with Client"
    event.begin = "2023-01-01T12:00:00"
    event.end = "2023-01-01T13:00:00"
    event.description = "Discuss project updates and goals."
    event.location = "Conference Room 123"

    # Add the event to the calendar
    cal.events.add(event)

    # Save the calendar to an .ics file
    with open("calendar.ics", "w") as f:
        f.writelines(cal)
    return ".\calendar.ics"
