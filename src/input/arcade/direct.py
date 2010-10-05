import convert
import inbox
import ARCADE

def get_events():
    # Read the descriptions and the table from arcade
    print "Running ARCADE... (cross your fingers now) "
    
    input = ARCADE.ArcadeClient().getTimetable()
    
    print "OK! (Probably.)"
    
    # Get the parts from the ARCADE output.
    parts = inbox.get_parts(input)
    
    return convert.get_events_from_parts(parts)
