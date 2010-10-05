#!/usr/bin/python
import os
import sys

def init():
    # Add the lib directory to the path.
    # It's a nasty hack, but it means you can just un-tar and go.
    current_dir = os.path.dirname(sys.argv[0])
    sys.path.append(os.path.join(current_dir, "../lib"))

init()

import config
import inbox
import convert
import exams

from stat import *
import datetime
from icalendar import UTC



def get_events_from_module(mod_name):
    full_name = "input.%s" % mod_name
    __import__(full_name)
    
    module = sys.modules[full_name]
    
    return list(module.get_events())


def get_events_from_modules(mod_names):
    return sum(map(get_events_from_module, mod_names), [])


def write_events(events):
    """Write an .ics file to the place specified in config,
    chmod-ing to 644.
    """
    # Use the current time as the timestamp (originally came from email).
    time_stamp = datetime.datetime.now(UTC)
    # Write the iCal file.
    convert.write_cal(events, time_stamp, config.ical)
    # Make the iCal file readable by all.
    os.chmod(os.path.expanduser(config.ical),
             S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH)


def main():
    # Get the events.
    events = get_events_from_modules(config.input_methods)
    
    # Write the events.
    write_events(events)


if __name__ == "__main__":
    main()
