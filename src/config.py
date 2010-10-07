
# Change these if you require different input/output files.
mailbox = "~/.cs_maildir/Inbox"
ical = "~/public_html/timetable.ics"
unit_titles = "~/.unit_titles"
user_config_file = "~/.arcade2ics/config.py"

# General config options
debug=True
input_methods=["arcade.direct"]
auto_update=False

# These should not need changing unless you
# are not at the University of Manchester
sender = "jtl@cs.man.ac.uk"
subject = "ARCADE Session details"

# This maps the last character of a class name to the category.
main_categories = {'L' : "Lab",
                   'S' : "Lecture",
                   'E' : "Examples Class",
                   'C' : "Submit",
                   'W' : "Workshop",
                   'X' : "Exam"}

# If the unit name matches this, then the category is selected 
# from main_categories, otherwise other_categories is used.
main_re = "(\d{4,})\D"

# Other categories to try - the keys are regular expressions.
other_categories = {"Tut\d" : "Tutorial"}


# A map from a regex to match the unit name to the length in hours.
# The 'None' case is used by default.
unit_lengths = [("10902L",  1),
                ("\d{4,}L", 2),
                (None,      1)]

# You shouldn't need to change anything below here.
# Might still be usefull to some people though.

import re

_main_re = re.compile(main_re)


def get_normal_unit(unit):
    """Get the normal representation of a unit."""
    match = _main_re.match(unit)
    if match:
        return match.group(1)
    elif unit.startswith("COMP"):
        return unit[4:]
    else:
        return unit


def get_category(event):
    "Take an event, and find the category."
    if _main_re.match(event.unit):
        return main_categories.get(event.unit[-1], event.unit[-1])
    else:
        for regex in other_categories:
            if re.match(regex, event.unit):
                return other_categories[regex]
        return None


def get_length(event):
    """Get the length of an event, in hours."""
    return re_guard(unit_lengths, event.unit)


def re_guard(guard, test_exp):
    """For each regular expression and value in guard:
        if the regex is None, return value
        else if the regex matches test_exp, return value."""
    for regex, exp in guard:
        if regex is not None:
            if re.match(regex, test_exp):
                return exp
        else:
            return exp


# Load the per-user configuration.
import os
absolute_config = os.path.expanduser(user_config_file)
if os.path.exists(absolute_config):
    execfile(absolute_config)
    
