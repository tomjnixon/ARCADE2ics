#!/usr/bin/python
import config
import inbox
import convert
import os
from stat import *

def main():
    # Read the descriptions and the table from the users inbox
    descriptions, table, time_stamp = inbox.get_recent_sessions(config.mailbox)
    # Write the iCal file
    convert.write_cal(descriptions, table, time_stamp, config.ical)
    # Make the iCal file readable by all.
    os.chmod(os.path.expanduser(config.ical),
             S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH)

if __name__ == "__main__":
    main()
