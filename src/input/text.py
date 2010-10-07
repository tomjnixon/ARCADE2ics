import urllib2
import re
from compatibility import *
import datetime
import config
import os

timetable_url = "http://www.cs.manchester.ac.uk/undergraduate/timetable/table_pr"
calendar_url = "http://www.cs.manchester.ac.uk/undergraduate/timetable/cscalendar.php"

days = "Mon Tue Wed Thu Fri".split()
day_nos = dict((day_name, i) for i, day_name in enumerate(days))



def get_text_timetable():
	return urllib2.urlopen(timetable_url).read()
	#return open("table_pr").read()


class Filter(object):
	
	field_names = "sem day time week lol course type group location".split()
	
	def __init__(self, **kwargs):
		self.predicates = kwargs
	
	def match(self, line):
		pos_fields = line.split("\t")
		fields = dict(zip(self.field_names, pos_fields))
		
		for key, value in self.predicates.iteritems():
			if fields.get(key, None) != value:
				return None
		
		return fields


def get_matching(filters):
	lines = get_text_timetable().split('\n')
	for line in lines:
		for filter in filters:
			match = filter.match(line)
			if match is not None:
				yield match
				break


def get_weeks_section(s):
	try:
		return [int(s)]
	except ValueError:
		try:
			left, right = s.split('-')
			return range(int(left), int(right) + 1)
		except ValueError:
			assert s.endswith('+')
			return range(int(s.rstrip('+')), 13)


def get_weeks(fields):
	weeks_str = fields["week"].strip()
	tokens = weeks_str.split()
	week_letter = None
	weeks = range(1, 13)
	
	for token in tokens:
		if token.startswith('w'):
			token = token.lstrip('w')
			weeks = []
			for x in token.split(','):
				weeks.extend(get_weeks_section(x))
		elif token in ['A', 'B']:
			week_letter = token
	
	return (weeks, week_letter)


def get_week_nos():
	week_re = re.compile(r'(\d+).(\d+)\s*\(([AB])\)')
	
	from BeautifulSoup import BeautifulSoup
	soup = BeautifulSoup(urllib2.urlopen(calendar_url).read())
	
	table = [[' '.join(td(text=True)) for td in tr("td")[1:]] 
	         for tr in soup("table")[0]("tr")[1:]]
	
	for date, week_no in table:
		match = week_re.search(week_no)
		if match is not None:
			semester, week = map(int, match.group(1, 2))
			week_letter = match.group(3)
			date = strptime(date, "%d/%m/%Y")
			yield (semester, week, week_letter, date)


def get_datetimes(week_nos, match):
	weeks = get_weeks(match)
	for semester, week, week_letter, date in week_nos:
		if (semester == int(match["sem"][3:]) and
		    week in weeks[0] and
		    (weeks[1] is None or weeks[1] == week_letter)):
			day_no = day_nos[match["day"].strip()]
			day_delta = datetime.timedelta(days=day_no)
			time = strptime(match["time"].strip(), "%H:%M") - strptime("0:00", "%H:%M")
			yield date + day_delta + time


class MyEvent(object):
    pass


def _convert_event(unit_names, match, date):
	event = MyEvent()
	event.whole_day = False
	event.datetime_start = date
	event.datetime_end = date + datetime.timedelta(hours=1)
	event.category = match["type"]
	event.room = match["location"]
	event.summary = "%s %s" % (unit_names[config.get_normal_unit(match["course"])],
	                           match["type"])
	event.description = ""
	event.uid = "%s/%s" % (md5(str(match) + str(date)), os.getenv("USER"))
	return event



def convert_event(unit_names, week_nos, match):
	for date in get_datetimes(week_nos, match):
		yield _convert_event(unit_names, match, date)


def get_events():
	filters = [Filter(course="COMP23420", type="Lec")
	          ,Filter(course="COMP25111", type="Lec")
	          ,Filter(course="COMP22111", type="Lec")
	          ,Filter(course="COMP24111", type="Lec")
	          ,Filter(course="COMP23111", type="Lec")
	          ,Filter(course="COMP26120", type="Lec")
	          ,Filter(course="2nd Yr Tutorial", group="All")
	          ]
	
	week_nos = list(get_week_nos())
	
	from unitname import UnitNames
	
	unit_names = UnitNames()
	
	for match in get_matching(filters):
		for event in convert_event(unit_names, week_nos, match):
			yield event

