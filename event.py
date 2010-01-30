

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
    def set_descriptions(class, descriptions):
        class.descriptions = descriptions

    room = property(get_from_descriptions("_room", "room"))
        
    time_str = property(get_from_descriprions("_time", "time"))

    def parse_event(event_str):
        """Parse an event, setting the following 
        "raw" - the original event string, "date", "session", "unit", "group",
        and possibly "room", and "time"
        """
        tokens = filter(len, event_str.split())
        self._date = tokens.pop(0)
        self.session = tokens.pop()
        if hour_re.match(tokens[0]):
            self._time = tokens.pop(0)
        self.unit = tokens.pop(0)
        self.group = tokens.pop(0)
        if tokens:
            self._room = tokens.pop(0)

    @property
    def summary(event):
        """Get the summary"""
        return "%s %s" % (self.unit, self.session)


