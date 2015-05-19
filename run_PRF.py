import sys

sys.path.append( 'exp_tools' )

from PRFSession import *
import appnope

def main():
	initials = raw_input('Your initials: ')
	run_nr = int(raw_input('Run number: '))
	
	appnope.nope()

	ts = PRFSession( initials, run_nr, tracker_on = False )
	ts.run()
	

	
if __name__ == '__main__':
	main()