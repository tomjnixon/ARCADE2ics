import re
import icalendar
from icalendar import UTC
from datetime import datetime, date
import time
import os

# Try to use hashlib, otherwise fall back on the old md5 module.
try: 
    import hashlib
    def md5(data):
        return hashlib.md5(data).hexdigest()
except ImportError:
    import md5 as _md5
    def md5(data):
        return _md5.new(data).hexdigest()

desc_time_re = re.compile("are at (\S*)")
desc_room_re = re.compile("in room (\S*)")

date_re = re.compile("(\d+)/(\d+)")
hour_re = re.compile("[\d:]+[ap]m")
time_parse_re = re.compile("(\d+):?(\d*)([ap]m)")


def get_events(table_str):
    """Split a table up into fields."""
    # Split into lines
    lines = map(str.strip, table_str.split('\n'))
    # Remove horizontal dividers
    lines = [line for line in lines if line.count('-') < 20]
    # Join the lines back together again (apart from the first), split at '|'s,
    # strip the whitespace, remove empty fields, and finally parse each event.
    return map(parse_event,
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


def parse_time(time_str):
    """Parse a time, returning the minute and the hour.
    accepts formats: "noon", "XX[ap]m", "XX:XX[ap]m"
    """
    if time_str == "noon":
        return (0, 12)

    match = time_parse_re.match(time_str)
    hour = int(match.group(1))
    if match.group(3) == "pm" and hour != 12:
        hour += 12

    if match.group(2):
        minute = int(match.group(2))
    else:
        minute = 0
    
    return (minute, hour)
    

def get_time(event, descriptions):
    """Get the time (and date) from an event.
    If there is no time in the event, try to find one in the descriptions.
    """
    day, month = map(int, date_re.search(event["date"]).groups())
    if "time" in event:
        minute, hour = parse_time(event["time"])
    else:
        description = descriptions.get(event["unit"])
        if description and "time" in description:
            minute, hour = parse_time(description["time"])
        else:
            minute, hour = None, None
    return (minute, hour, day, month)

def get_room(event, descriptions):
    """Get the room from event, otherwise try to find it in descriptions,
    otherwise return none."""
    if "room" in event:
        return event["room"]
    elif event["unit"] in descriptions:
        return descriptions[event["unit"]].get("room", None)
    else:
        return None


def make_event(event, descriptions, time_stamp):
    """Make an iCal event from an ARCADE event."""
    vevent = icalendar.Event()
    minute, hour, day, month = get_time(event, descriptions)
    year = time_stamp.year

    whole_day = minute is None or hour is None
    if whole_day:
        startdate = date(year, month, day)
    else:
        startdate = datetime(year, month, day, hour, minute, tzinfo=UTC)

    vevent.add('summary', event.summary)
    vevent.add('dtstart', startdate)

    if not whole_day:
        vevent.add('dtend', datetime(year, month, day, hour + 1, minute, tzinfo=UTC))

    room = get_room(event, descriptions)
    if room: 
        vevent.add('location', room)

    vevent.add('dtstamp', time_stamp)
    vevent["uid"] = "%s/%s" % (md5(event["raw"]), os.getenv("USER"))
    return vevent

    
def make_cal(events, descriptions, time_stamp):
    """Make an iCalendar object from a set of events and descriptions."""
    cal = icalendar.Calendar()
    cal.add('prodid', '-//ARCADE to iCal Converter//nixont9@cs.man.ac.uk//EN')
    cal.add('version', '2.0')
    for event in events:
        cal.add_component(make_event(event, descriptions, time_stamp))
    return cal

def write_cal(descriptions_str, events_str, time_stamp, file_name):
    """Write a .ics file to file_name."""
    descriptions = get_descriptions(descriptions_str)
    events = get_events(events_str)
    ical_string = make_cal(events, descriptions, time_stamp).as_string()

    f = open(os.path.expanduser(file_name), 'wb')
    f.write(ical_string)
    f.close()
