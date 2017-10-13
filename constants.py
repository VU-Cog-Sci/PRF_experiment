

# standard parameters
standard_parameters = {
	
	## common parameters:
	'practice':						1,
	'stim_size': 		         1,		# 7.5 degree stim radius
	'num_elements':             1500,		# amount of elements in bar, this will be num_elements * (1/bar_width_ratio) = 8000 for Mapper
	'PRF_period_in_TR':           24,		# that is 24*1.5=36 sec, which is 7.5/24 = 0.625 degree per step
	'PRF_ITI_in_TR':             2.0,		# that is 2*1.5 = 3 sec
	'TR':               	   1.594,		# VERY IMPORTANT TO FILL IN!!				
	'redraws_per_TR' :     		 3.0,		# TR/redraws_per_TR is the length of the transients, in this case 500 ms
	'task_rate' :       	     2.0,		# this + minimum_pulse_gap is average of exponential distribution
	'minimum_pulse_gap':		 2.0,		# the '0' point for the exponential distribution out of which transients are generated
	'fast_speed':      			 6.0,		# speed of the fast elements
	'slow_speed':      			 4.0,		# speed of the slow elements
	'element_size':    			35.0,		# size of the elements
	'element_spatial_frequency': 2.0,		# sf of the elemenets

	## PRF experiment variables:
	'bar_width_ratio': 			0.125,		# 0.125 * 0.9 * screen heigth = 3.375
	'num_fns_trials':			  4,		# speaks for itself

	## mapper variables:
	'mapper_stim_in_TR': 	      2.0,		# duration of mapper stimulus in TRs
	'mapper_ITI_in_TR':  		  1.0,		# duration of mapper ITI in TRs

	## Color matcher variables:
	'num_trials': 				  10,		# amount of matcher trials
	'BY_comparison_color': 		   0.5,		# color to compare to; 0.5 is best.
}

response_button_signs = {
'e':-1,  # left 'less' answer
'b':1,   # right 'more' answer
'y':2}   # confirm color match

screen_res = (1920,1080)
background_color = (0,0,0)

full_screen = False

