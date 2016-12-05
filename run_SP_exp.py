import sys

sys.path.append( 'exp_tools' )

from SPSession import *
try:
    import appnope
    appnope.nope()
except:
    print 'APPNOPE NOT ACTIVE!'

def main():
    initials = raw_input('Your initials: ')
    run_nr = int(raw_input('Run number: '))
    fix_sp = raw_input('Set SP amplitude to 0 (y/n): ')
    scanner = raw_input('Are you in the scanner (y/n)?: ')
    track_eyes = raw_input('Are you recording gaze (y/n)?: ')
    if track_eyes == 'y':
        tracker_on = True
    elif track_eyes == 'n':
        tracker_on = False


    ts = SPSession( initials, run_nr, scanner, tracker_on,fix_sp )
    ts.run()
    
if __name__ == '__main__':
    main()
