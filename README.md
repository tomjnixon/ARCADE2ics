ARCADE2ics converts ARCADE emails into iCalendar files that can be imported into
Google calendar, your phone, or almost any other piece of calendar software.

By default, ARCADE2ics puts your timetable on-line, and updates automatically,
allowing you to 'subscribe' to the timetable, meaning that you will always
have the latest version available. 

Installation
------------
Either:

-   Local installation:
    -   Check out the latest version from git:

            $ git clone git://github.com/tomjnixon/ARCADE2ics.git

    -   Run `setup` on the computer which you wish to run this on
        (this will install it into your crontab).
        -   For example, to run this on soba.cs.man.ac.uk:

                $ ssh user_name@soba.cs.man.ac.uk "~/ARCADE2ics/setup"


- Use my installation - I keep the latest version publicly accessible in my home directory. This ensures that you are always using the latest stable version.
    -   Run `~nixont9/ARCADE2ics/setup` on the computer which you wish to run this on
        -   For example, to run this on soba.cs.man.ac.uk:

                $ ssh user_name@soba.cs.man.ac.uk "~nixont9/ARCADE2ics/setup"

Usage
-----
- The default iCalendar location is `~/public_html/timetable.ics`
- This can be accessed at [http://www2.cs.man.ac.uk/~user_name/timetable.ics](http://www2.cs.man.ac.uk/~user_name/timetable.ics)
- If using Google calendar, this address will not work (due to robots.txt).
  You may use [http://tnutils.appspot.com/timetable-user_name.ics](http://tnutils.appspot.com/timetable-user_name.ics) instead.
- By default, this is updated every day at 3:30am.
- To manually re-generate the timetable, run run.py.
- To change the names of modules in the calendar, edit `~/.unit_titles`. This is in the form of a python dictionary, and should be fairly self-explanatory.

Licence
-------
All ARCADE2ics code is published under the MIT Licence (see MIT-LICENCE.txt), and is copyright (c) 2010 Thomas Nixon.

The iCalendar module is published under the LGPL (see icalendar/LICENCE.txt), from [http://codespeak.net/icalendar/](http://codespeak.net/icalendar/), some modifications.