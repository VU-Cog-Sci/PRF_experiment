

# standard parameters
standard_parameters = {
	
	## common parameters:
	'stim_size': 0.9,						# 13.5 degree stim radius
	'num_elements' : 2500,
	'period' : 36.0,
	'ITI':-0.001,
	'TR':1.5,				
	'redraws_per_TR' : 3,
	'task_rate' : 2.0,						# this + minimum_pulse_gap is average of exponential distribution
	'minimum_pulse_gap':2.0,				# the '0' point for the exponential distribution out of which transients are generated
	'fast_speed': 6,
	'slow_speed': 4,
	# 'RG_color': 1,
	# 'BY_color':1,
	'element_size': 45.0,
	'element_spatial_frequency': 2.0,

	## attention experiment variables:
	'orientation' : 0.0,					# just for initiation
	'bar_width_ratio': 0.125,				# 0.2 times the stimulus radius, which is 2.7 degrees

	## mapper variables:
	'mapper_period': 2.0,					# duration of mapper stimulus
	'mapper_ITI':2.0,

	## Color and Speed matcher variables:
	'num_trials': 10,
	'BY_comparison_color': 0.75,
}

response_button_signs = {'e':-1, 'b':1, 'g':2}  #first is left answer, second the right, third the continue trial in the mappers


screen_res = (1920,1080)
# screen_res = (1152, 870)
background_color = (-0.75,-0.75,-0.75)
initial_wait_time = 0.0
