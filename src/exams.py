import os
from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta
import time
from config import main_categories
from compatibility import *


class MyEvent(object):
    pass


def get_exam_events():
    """Get some exam events from ~/exams.html (if it exists),
    which is the central university exam timetable page.
    Hairy, i know.
    """
    try:
        doc = open(os.path.expanduser("~/exams.html"))
    except:
        return
    
    soup = BeautifulSoup(doc)
    rows = soup("table")[1]("tr")[1:]
    cells = [[td.string for td in tr("td")] for tr in rows]

    for row in cells:
        code, title, date, location, seat, start, finish = row

        date = strptime(date, "%d-%b-%y")
        start = datetime.combine(date, strptime(start, "%I:%M %p").time())
        finish = datetime.combine(date, strptime(finish, "%I:%M %p").time())

        event = MyEvent()
        event.whole_day = False
        event.datetime_start = start
        event.datetime_end = finish
        
        category = main_categories["X"]

        event.summary = "%s %s" % (title, category)
        event.category = category
        event.room = "%s - %s" % (seat, location)
        event.description = "Code: %s" % code

        event.uid = "%s/%s" % (md5(''.join(row)), os.getenv("USER"))

        yield event


    
    
