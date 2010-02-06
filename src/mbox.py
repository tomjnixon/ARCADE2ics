import re
import os
from datetime import tzinfo, timedelta, datetime
from compatibility import strptime

ZERO = timedelta(0)

# A UTC class (from the python docs).
class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()

from_re = re.compile("\n>(>*From)")
subject_re = re.compile("\nSubject:(.*)\n")
date_re = re.compile("\nDate:(.*) [^ ]+\n")

def unescape(msg):
    return from_re.sub("\\1", msg)


def parse(file_name):
    f = open(os.path.expanduser(file_name))
    messages = map(Message, f.read().split("\nFrom "))

    return messages


class Message(object):
    def __init__(self, msg_string):
        self.msg_string = msg_string
    
    _split_cache = None

    @property
    def _split(self):
        if self._split_cache is None:
            self._split_cache = unescape(self.msg_string).split("\n\n", 1)
        return self._split_cache

    @property
    def sender(self):
        return self.msg_string.split(' ', 1)[0]

    @property
    def subject(self):
        match = subject_re.search(self.msg_string)
        if match:
            return match.group(1).strip()
        else:
            return ""
    
    @property
    def date(self):
        match = date_re.search(self.msg_string)
        if match:
            time = strptime(match.group(1).strip(),
                            "%a, %d %b %Y %H:%M:%S")
            return time.replace(tzinfo=utc)
        else:
            return None

    @property
    def body(self):
        return self._split[1]


#msgs = parse("/home/tom/.cs_maildir/Inbox")
#for x in [x for x in msgs if x.subject.startswith("ARCADE Session")][-1:]: 
#for x in msgs[-2:]: 
    #print "\n\n\n-%s-\n-%s-\n%s" % (x.sender, x.subject, x.date)
