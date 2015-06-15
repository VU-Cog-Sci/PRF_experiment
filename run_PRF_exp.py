import sys

sys.path.append( 'exp_tools' )

from PRFSession import *
from plot_staircases import *
import appnope

def main():
	initials = raw_input('Your initials: ')
	run_nr = int(raw_input('Run number: '))
	scanner = raw_input('Are you in the scanner (y/n)?: ')
	track_eyes = raw_input('Are you recording gaze (y/n)?: ')
	if track_eyes == 'y':
		tracker_on = True
	elif track_eyes == 'n':
		tracker_on = False

	appnope.nope()

	ts = PRFSession( initials, run_nr, scanner, tracker_on )
	ts.run()

	plot_staircases(initials, run_nr)
	
if __name__ == '__main__':
	main()