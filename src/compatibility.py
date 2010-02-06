# Provide some functions for backwards compatibility.

# Provide an 'all' function to older pythons
if "all" not in dir(__builtins__):
    def all(xs):
        for x in xs:
            if not x:
                return False
        return True

# In old pythons, datetime has no 'strptime' function
from datetime import datetime
import time
def strptime(date_string, format):
    # From the python docs.
    return datetime(*(time.strptime(date_string, format)[0:6]))


# Try to use hashlib, otherwise fall back on the old md5 module.
try: 
    import hashlib
    def md5(data):
        return hashlib.md5(data).hexdigest()
except ImportError:
    import md5 as _md5
    def md5(data):
        return _md5.new(data).hexdigest()
