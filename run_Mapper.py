import sys

sys.path.append( 'exp_tools' )

from MapperSession import *
import appnope

def main():
    initials = raw_input('Your initials: ')
    run_nr = int(raw_input('Run number: '))
    track_eyes = raw_input('Are you recording gaze (y/n)?: ')
    if track_eyes == 'y':
        tracker_on = True
    elif track_eyes == 'n':
        tracker_on = False
    appnope.nope()

    ts = MapperSession( initials, run_nr, tracker_on )
    ts.run()

if __name__ == '__main__':
    main()
