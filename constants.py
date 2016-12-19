

# standard parameters
standard_parameters = {
	
	'practice':					True,
	## common parameters:
	'vertical_stim_size': 		 1,		# portion of 
	'horizontal_stim_size': 	 1,		# portion of 
	'num_elements':             2000,		# amount of elements in bar, this will be num_elements * (1/bar_width_ratio) = 8000 for Mapper
	'vertical_pass_dur':           32,		# that is 24*1.5=36 sec, which is 15/24 = 0.625 degree per step
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

# response_button_signs = {
# 'e':-1,  # left 'less' answer  e
# 'b':1,   # right 'more' answer   b
# 'y':2}   # confirm color match y 

response_button_signs = {
'f':-1,  # left 'less' answer  e
'j':1,   # right 'more' answer   b
'y':2}   # confirm color match y 
# }  	

# screen_res = (1920,1080)
# background_color = (0.5,0.5,0.5)#-0.75,-0.75,-0.75)

full_screen = True
FGC = (0,0,0)
BGC = (255*0.5,255*0.5,255*0.5) # this is converted to -1<->1 in SPSession

# K2D-38 (all in cm):
#DISPSIZE = (1024,768)
#SCREENSIZE = (39.0,29.0)
#SCREENDIST = 60.0
#7T scan room (all in cm):
#DISPSIZE = (1024,768)
DISPSIZE = (1920,1200)#(1280,720)#,1080)#(1024,768)#(1920,1080)
SCREENSIZE = (69.84,39.29) #physical screen size in centimeters
SCREENDIST = 225#60.0#65.0#57.0 # centimeters; distance between screen and participant's eyes
#office screen
# DISPSIZE = (2560,1440)#(1280,720)#,1080)#(1024,768)#(1920,1080)
# SCREENSIZE = (59.83,33.72)# physical screen size in centimeters
# SCREENDIST = 75# centimeters; distance between screen and participant's eyes


