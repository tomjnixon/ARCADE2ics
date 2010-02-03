import urllib2
from BeautifulSoup import BeautifulSoup
import sys
import re
import json
from config import unit_titles, get_normal_unit
from UserDict import UserDict
import os.path

master_url = "http://www.cs.manchester.ac.uk/undergraduate/programmes/courseunits/syllabus.php?code=%s"

header_re = re.compile(".*: (.*) \(\d{4}\)")


class UnitNames(UserDict):
    """A dictionary-like class, storing unit titles."""
    def __init__(self, file_name = unit_titles):
        UserDict.__init__(self)
        self.file_name = os.path.expanduser(file_name)
        self.read()


    def __del__(self):
        self.write()


    def read(self):
        """Read the unit names from disk."""
        try:
            self.data = json.load(open(self.file_name))
        except:
            pass


    def write(self):
        """Write the unit names to disk."""
        json.dump(self.data, open(self.file_name, 'w'),
                  indent=4)


    def __getitem__(self, unit):
        if unit in self.data:
            return self.data[unit]
        else:
            title = get_title(unit)
            self.data[unit] = title
            return title


def web_unit_codes(unit):
    """Turn a unit code from ARCADE into a list of possible web unit codes."""
    # Try just prepending 'COMP' to the unit.
    yield "COMP%s" % unit
    # Try decreasing the last number.
    if unit[-1].isdigit():
        for i in reversed(range(int(unit[-1]))):
            yield "COMP%s%i" % (unit[:-1], i)
    # Finally tryjust the unit.
    yield unit


def get_web_title(unit):
    """Get the title of a unit from the web."""
    # Silently ignore all network and parse errors.
    # Failure is always an option!
    try:
        # Download and parse the page.
        page = urllib2.urlopen(master_url % unit)
        soup = BeautifulSoup(page)
        # Find the header text.
        header = soup.find("div", id="content").h1.string.strip()
        # Extract the title from the header
        match = header_re.match(header)
        if match:
            title = match.group(1).strip()
            return title or None
        else:
            return None
    except:
        return None


def get_title(unit):
    """Get the title of a unit."""
    for web_unit in web_unit_codes(unit):
        title = get_web_title(web_unit)
        if title is not None:
            return title
    return unit


def main():
    print "%s : %s" % (sys.argv[1], get_title(sys.argv[1]))
    #print "%s : %s" % (sys.argv[1], list(web_unit_codes(sys.argv[1])))


if __name__ == "__main__":
    main()
