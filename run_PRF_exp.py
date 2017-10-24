import sys, datetime
# from Tkinter import *

sys.path.append( 'exp_tools' )

from PRFSession import *
from plot_staircases import *
try:
    import appnope
    appnope.nope()
except:
    print 'APPNOPE NOT ACTIVE!'

def main():
    initials = raw_input('Your initials: ')
    run_nr = int(raw_input('Run number: '))
    scanner = raw_input('Are you in the scanner (y/n)?: ')
    track_eyes = raw_input('Are you recording gaze (y/n)?: ')
    task_type = 'bar'#raw_input('Attention task (fix/bar): ')
    if track_eyes == 'y':
        tracker_on = True
    elif track_eyes == 'n':
        tracker_on = False

    ts = PRFSession( initials, run_nr, scanner, tracker_on, task_type )
    ts.run()

    plot_staircases(initials, run_nr)

if __name__ == '__main__':
    main()
