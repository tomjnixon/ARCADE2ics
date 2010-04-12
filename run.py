#!/usr/bin/python
import os
import sys

def init():
    # Add src and lib directories to the path.
    # It's a nasty hack, but it means you can just un-tar and go.
    current_dir = os.path.dirname(sys.argv[0])
    sys.path.append(os.path.join(current_dir, "src"))
    sys.path.append(os.path.join(current_dir, "lib"))

init()

import config
import inbox
import convert
import exams

from stat import *


def run_with_input(parts, time_stamp):
    """Write an .ics file to the place specified in config,
    chmod-ing to 644. This is the common function of all run_*.py files.
    """
    # Get event objects from parts.
    events = convert.get_events_from_parts(parts) + list(exams.get_exam_events())
    # Write the iCal file.
    convert.write_cal(events, time_stamp, config.ical)
    # Make the iCal file readable by all.
    os.chmod(os.path.expanduser(config.ical),
             S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH)


def main():
    # Read the parts from the users inbox
    parts, time_stamp = inbox.get_recent_sessions(config.mailbox)
    # write the ics file.
    run_with_input(parts, time_stamp)


if __name__ == "__main__":
    main()
