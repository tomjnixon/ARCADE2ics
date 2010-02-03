import re
import icalendar
from icalendar import UTC
from datetime import datetime, date
import time
import os
from event import Event
from unitname import UnitNames
from compatibility import *

desc_time_re = re.compile("are at (\S*)")
desc_room_re = re.compile("in room (\S*)")

def get_events(table_str):
    """Split a table up into fields."""
    # Split into lines
    lines = map(str.strip, table_str.split('\n'))
    # Remove horizontal dividers
    lines = [line for line in lines if line.count('-') < 20]
    # Join the lines back together again (apart from the first), split at '|'s,
    # strip the whitespace, remove empty fields, and finally parse each event.
    return map(Event,
               filter(len,
                      map(str.strip, ''.join(lines[1:]).split('|'))))


def parse_description(line):
    """Parse a single line of the description into a dict with keys
    'code', 'time', and 'room'.
    """
    line = line.rstrip('.')
    description = {"code" : line.split(' ')[0]}
    
    time_match = desc_time_re.search(line)
    if time_match:
        description["time"] = time_match.group(1)
        
    room_match = desc_room_re.search(line)
    if room_match:
        description["room"] = room_match.group(1)
        
    return description


def get_descriptions(descriptions_str):
    """Parse a block of descriptions into a dict with keys representing 
    the unit code, and values in the format of parse_description.
    """
    descriptions = map(parse_description,
                       filter(len,
                              map(str.strip,
                                  descriptions_str.split('\n'))))
    return dict((desc["code"], desc) for desc in descriptions)


def make_event(event, time_stamp):
    """Make an iCal event from an ARCADE event."""
    vevent = icalendar.Event()
    minute, hour, day, month = event.time
    year = time_stamp.year

    whole_day = minute is None or hour is None
    if whole_day:
        startdate = date(year, month, day)
    else:
        startdate = datetime(year, month, day, hour, minute, tzinfo=UTC)
        enddate = datetime(year, month, day, 
                           hour + event.length, minute, tzinfo=UTC)

    vevent.add('summary', event.summary)
    vevent.add('dtstart', startdate)

    if not whole_day:
        vevent.add('dtend', enddate)

    if event.room: 
        vevent.add('location', event.room)

    if event.category:
        vevent.add('categories', event.category)

    vevent.add('dtstamp', time_stamp)
    vevent["uid"] = event.uid
    return vevent

    
def make_cal(events, time_stamp):
    """Make an iCalendar object from a set of events and descriptions."""
    cal = icalendar.Calendar()
    cal.add('prodid', '-//ARCADE to iCal Converter//nixont9@cs.man.ac.uk//EN')
    cal.add('version', '2.0')
    for event in events:
        cal.add_component(make_event(event, time_stamp))
    return cal

def write_cal(descriptions_str, events_str, time_stamp, file_name):
    """Write a .ics file to file_name."""
    # Parse the descriptions.
    descriptions = get_descriptions(descriptions_str)
    # Set up the event class.
    Event.set_descriptions(descriptions)
    # Read the unit names from the user's local file.
    unit_names = UnitNames()
    Event.set_unit_names(unit_names)
    # Parse the events and write the calendar.
    events = get_events(events_str)
    ical_string = make_cal(events, time_stamp).as_string()
    # Write the calendar to the .ics file.
    f = open(os.path.expanduser(file_name), 'wb')
    f.write(ical_string)
    f.close()
    unit_names.write()

