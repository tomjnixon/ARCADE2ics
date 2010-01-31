
# Change these if you require different input/output files.
mailbox = "~/.cs_maildir/Inbox"
ical = "~/public_html/timetable.ics"


# These should not need changing unless you
# are not at the University of Manchester
sender = "jtl@cs.man.ac.uk"
subject = "ARCADE Session details"


# This maps the last character of a class name to the category.
main_categories = {'L' : "Labs",
                   'S' : "Lectures",
                   'E' : "Examples Classes"}

# If the unit name matches this, then the category is selected 
# from main_categories, otherwise other_categories is used.
main_re = "\d{4,}\D"

# Other categories to try - the keys are regular expressions.
other_categories = {"Tut\d" : "Tutorials"}


# You shouldn't need to change anything below here.
# Might still be usefull to some people though.

import re

_main_re = re.compile(main_re)

def get_category(event):
    "Take an event, and find the category."
    if _main_re.match(event.unit):
        return main_categories.get(event.unit[-1], None)
    else:
        for regex in other_categories:
            if re.match(regex, event.unit):
                return other_categories[regex]
        return None
