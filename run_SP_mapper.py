import sys

sys.path.append( 'exp_tools' )

from SPMapperSession import *
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
    if track_eyes == 'y':
        tracker_on = True
    elif track_eyes == 'n':
        tracker_on = False


    ts = SPMapperSession( initials, run_nr, scanner, tracker_on )
    ts.run()
    
if __name__ == '__main__':
    main()