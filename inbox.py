import mbox
import config
from compatibility import all

def is_line(line):
    """Is line full of dashes?"""
    return line.count("-") == len(line)

def is_arcade_part(part):
    """Try to work out if the given block is a table generated by ARCADE.
    This is true if the first, third and last line satisfies is_line."""
    lines = part.split("\n")
    return (len(lines) >= 5 
            and all(map(is_line, [lines[0], lines[2], lines[-1]])))


def is_arcade_email(msg):
    """Is msg an email from ARCADE?"""
    return (msg.sender.startswith(config.sender) and
            msg.subject == config.subject)
            

def find_arcade_email(box):
    """Find the last email in box to satisfy is_arcade_email"""
    for msg in reversed(box):
        if is_arcade_email(msg):
            return msg
    raise Exception("No recognised emails in inbox.")
            

def get_recent_sessions(file_name):
    """Extract descriptions and the table from email file file_name."""
    box = mbox.parse(file_name)    
    msg = find_arcade_email(box)
    
    parts = msg.body.split("\n\n")
    for i in reversed(xrange(len(parts))):
        if is_arcade_part(parts[i]):
            return (parts[i-1], parts[i], msg.date)



