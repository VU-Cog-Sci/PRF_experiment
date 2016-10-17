

# standard parameters
standard_parameters = {
	
	'practice':					True,
	## common parameters:
	'stim_size': 		          1.,		# that means 0.5 * 15 degrees = 7.5 degree stim diameter (3.6 radius)
	'num_elements':             1500,		# amount of elements in bar, this will be num_elements * (1/bar_width_ratio) = 8000 for Mapper
	'PRF_period_in_TR':           32,		# that is 24*1.5=36 sec, which is 15/24 = 0.625 degree per step
	'PRF_ITI_in_TR':             0.5,		# that is 2*1.5 = 3 sec # used: 2
	'TR':               	    0.944,		# VERY IMPORTANT TO FILL IN AFTER PLANNING IN!			
	'redraws_per_TR' :     		 3.0,		# TR/redraws_per_TR is the length of the transients, in this case 500 ms: #used e
	'task_rate' :       	     2.0,		# this + minimum_pulse_gap is average of exponential distribution, #used :2
	'minimum_pulse_gap':		 2.0,		# the '0' point for the exponential distribution out of which transients are generated, #used: 2
	'fast_speed':      			 7.0,		# speed of the fast elements for TK/DE/JW: 6, for JS/SN/NA: 7
	'slow_speed':      			 3.0,		# speed of the slow elements for TK/DE/JW: 4, for JS/SN/NA: 3
	'element_size':    			35.0,		# size of the elements # used: 35
	'element_spatial_frequency': 0.5,		# sf of the elemenets # used: 2

	## PRF experiment variables:
	'bar_width_ratio': 			0.1,		# 0.125 * 0.
	'num_fns_trials':			  4,		# speaks for itself

	## mapper variables:
	'mapper_stim_in_TR': 	      2.0,		# duration of mapper stimulus in TRs
	'mapper_ITI_in_TR':  		  1.0,		# duration of mapper ITI in TRs

	## Color matcher variables:
	'num_trials': 				    10,		# amount of matcher trials
	'BY_comparison_color': 		   0.5,		# color to compare to; 0.5 is best.
}

response_button_signs = {
'e':-1,  # left 'less' answer  e
'b':1,   # right 'more' answer   b
'y':0}   # confirm color match y 
# }  	

screen_res = (1920,1080)
background_color = (0.5,0.5,0.5)#-0.75,-0.75,-0.75)
