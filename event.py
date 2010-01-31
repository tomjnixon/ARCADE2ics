import os
from compatibility import *
import re

date_re = re.compile("(\d+)/(\d+)")
hour_re = re.compile("[\d:]+[ap]m")
time_parse_re = re.compile("(\d+):?(\d*)([ap]m)")

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

    
def get_from_descriptions(name, desc_name, default=None):
    def get(self):
        if hasattr(self, name) and getattr(self, name) is not None:
            return getattr(self, name)
        elif self.unit in self.descriptions:
            return self.descriptions[self.unit].get(desc_name, default)
        else:
            return default
    return get


class Event(object):
    """A representation of an event from the ARCADE timetable."""

    _time = None
    room = None
    descriptions = None


    def __init__(self, event_str):
        self.event_str = event_str
        self.parse_event(event_str)


    @classmethod
    def set_descriptions(cls, descriptions):
        cls.descriptions = descriptions


    room = property(get_from_descriptions("_room", "room"))

        
    time_str = property(get_from_descriptions("_time", "time"))


    def parse_event(self, event_str):
        """Parse an event, setting the following 
        "raw" - the original event string, "date", "session", "unit", "group",
        and possibly "room", and "time"
        """
        tokens = filter(len, event_str.split())
        self.date_str = tokens.pop(0)
        self.session = tokens.pop()
        if hour_re.match(tokens[0]):
            self._time = tokens.pop(0)
        self.unit = tokens.pop(0)
        self.group = tokens.pop(0)
        if tokens:
            self._room = tokens.pop(0)


    @property
    def summary(self):
        """Get the summary"""
        return "%s %s" % (self.unit, self.session)


    @property
    def uid(self):
        return "%s/%s" % (md5(self.event_str), os.getenv("USER"))


    @property 
    def date(self):
        day, month = map(int, date_re.search(self.date_str).groups())
        return (day, month)

    
    @property
    def time(self):
        """Get the time (and date) from an event."""
        day, month = self.date

        if self.time_str:
            minute, hour = parse_time(self.time_str)
        else:
            minute, hour = None, None

        return (minute, hour, day, month)


