ARCADE2ics
==========

ARCADE2ics converts ARCADE emails into iCalendar files that can be imported into
Google calendar, your phone, or almost any other piece of calendar software.

By default, ARCADE2ics puts your timetable on-line, and updates automatically,
allowing you to 'subscribe' to the timetable, meaning that you will always
have the latest version available. 

Installation
------------

      $ git clone git://github.com/tomjnixon/ARCADE2ics.git
      $ ./ARCADE2ics/run

You should be presented with some configuration options. These are explained below:

### Input Method ###

Chose where ARCADE2ics gets its data from. Highlight any that you want and press "space" to select. You should probably chose `arcade.direct` or `arcade.email`.

### Auto Update ###

If selected, ARCADE2ics will update before it's running, so you'll always be running the latest version with the latest fixes and features.

### Send Timetable ###

This option is currently unused, but will soon cause ARCADE2ics to send me a copy of your ARCADE timetable so that I can verify that it's all working properly. You'll probably be making your timetable publicly accessible anyway, so you might as well select this.

### Cron ###

Select this to install to the crontab on this computer. This will make ARCADE2ics run automatically between 3:00 and 4:00 in the morning.


Usage
-----
- The default iCalendar location is `~/public_html/timetable.ics`
- This can be accessed at [http://www2.cs.man.ac.uk/~user_name/timetable.ics](http://www2.cs.man.ac.uk/~user_name/timetable.ics)
- If using Google calendar, this address will not work (due to robots.txt).
  You may use [http://tnutils.appspot.com/timetable-user_name.ics](http://tnutils.appspot.com/timetable-user_name.ics) instead.
- To manually re-generate the timetable, run `run`.
- To change the names of modules in the calendar, edit `~/.unit_titles`. This is in the form of a python dictionary, and should be fairly self-explanatory.

Licence
-------
All ARCADE2ics code is published under the MIT Licence (see MIT-LICENCE.txt), and is copyright (c) 2010 Thomas Nixon.

The iCalendar module is published under the LGPL (see lib/icalendar/LICENCE.txt), from [http://codespeak.net/icalendar/](http://codespeak.net/icalendar/), some modifications.

The BeautifulSoup module is published under the BSD licence (see lib/BeautifulSoup.py), from [http://www.crummy.com/software/BeautifulSoup/](http://www.crummy.com/software/BeautifulSoup/).
