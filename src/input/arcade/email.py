import inbox
import config
import convert

def get_events():
    parts, time_stamp = inbox.get_recent_sessions(config.mailbox)
    return convert.get_events_from_parts(parts)
