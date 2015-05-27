import sys

sys.path.append( 'exp_tools' )

from SubjectiveIsoLuminanceSession import *
from plot_staircases import *
import appnope

def main():
	initials = raw_input('Your initials: ')
	run_nr = int(raw_input('Run number: '))
	scanner = raw_input('Are you in the scanner (y/n)?: ')

	appnope.nope()

	ts = SubjectiveIsoLuminanceSession( initials, run_nr, scanner, tracker_on = False )
	ts.run()
	
if __name__ == '__main__':
	main()