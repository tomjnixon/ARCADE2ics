#!/usr/bin/python
import run
run.init()

import sys
import datetime

import inbox
from icalendar import UTC

import ARCADE


def main():
    # Read the descriptions and the table from arcade
    print "Running ARCADE... (cross your fingers now) ",
    sys.stdout.flush()
    
    input = ARCADE.ArcadeClient().getTimetable()
    
    print "OK! (Probably.)"
    
    # Get the parts from the ARCADE output.
    parts = inbox.get_parts(input)

    # Use the current time as the timestamp.
    time_stamp = datetime.datetime.now(UTC)

    # Write the iCal file
    run.run_with_input(parts, time_stamp)



if __name__ == "__main__":
    main()
