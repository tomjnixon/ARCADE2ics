ARCADE2ics converts ARCADE emails into iCalendar files that can be imported into
Google calendar, your phone, or almost any other piece of calendar software.

By deafult, ARCADE2ics puts your timetable online, and updates automatically,
allowing you to 'subscribe' to the timetable, meaning that you will always
have the latest version available. 

Installation
------------
-   Get the source. Either:
    -   Download and extract [ARCADE2ics-0.1.tar.gz](http://cloud.github.com/downloads/tomjnixon/ARCADE2ics/ARCADE2ics-0.1.tar.gz)

            $ wget http://cloud.github.com/downloads/tomjnixon/ARCADE2ics/ARCADE2ics-0.1.tar.gz
            $ tar -xzvf ARCADE2ics-0.1.tar.gz

    -   Check out the latest version from git:

             $ git clone git://github.com/tomjnixon/ARCADE2ics.git

-   Run `setup` on the computer which you wish to run this on
    (this will install it into your crontab).
    -   For example, to run this on soba.cs.man.ac.uk:

            $ ssh user_name@soba.cs.man.ac.uk ~/ARCADE2ics/setup

Usage
-----
- The default iCalendar location is `~/public_html/timetable.ics`
- This can be accessed at [http://www2.cs.man.ac.uk/~user_name/timetable.ics](http://www2.cs.man.ac.uk/~user_name/timetable.ics)
- If using google calendar, this address will not work (due to robots.txt).
  You may use [http://tnutils.appspot.com/timetable-user_name.ics](http://tnutils.appspot.com/timetable-user_name.ics) instead.
- By default, this is updated every day at 3:30am.
- To manually re-generate the timetable, run run.py.

Licence
-------
All ARCADE2ics code is published under the MIT Licence (see MIT-LICENCE.txt),
and Copyright (c) 2010 Thomas Nixon

The iCalendar module is published under the LGPL (see icalendar/LICENCE.txt)
From [http://codespeak.net/icalendar/](http://codespeak.net/icalendar/), some modifications.