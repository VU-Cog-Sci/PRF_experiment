####################################
#  !!! ADJUST THESE PARAMETERS!!!  #
####################################
TR = 0.7
practice = 0
screen = '3T_bold'
# screen = '7T_bold'
# screen = 'office'
# screen = 'K2D38'
# screen = 'laptop'
FULLSCREEN = True

standard_parameters = {
    ## ADJUST THESE PARAMETERS
    'practice':             practice,
    'TR':                         TR,       #         

    # stimulus params (spatial)
    'max_ecc':                     7,         # in dva
    'num_elements':             1500,       # amount of elements in bar, this will be num_elements * (1/bar_width_ratio) = 8000 for Mapper
    'fast_speed':                7.0,       # speed of the fast elements
    'slow_speed':                3.0,       # speed of the slow elements
    # 'element_size':             0.35,       # size of the elements in dva
    'element_sf_min':            0.5,       # min sf of the elemenets
    'element_sf_mean':             5,       # this + min is mean sf of the elemenets
    'bar_width_ratio':           0.1,       # 0.1

    # stim params (temporal)
    'PRF_period_in_TR':           40,       # that is 20*1.5=30 sec, which is 10/20 = 0.5 degree per step
    'fns_period_in_TR':           20,       # that is 10*1.5=15 sec, which is 10/20 = 0.5 degree per step
    'PRF_ITI_in_TR':             0.5,#0.5,       # that is 2*1.5 = 3 sec
    'redraws_per_TR' :           1.0,       # TR/redraws_per_TR is the length of the transients, in this case 500 ms
    'calibration_ecc' :            2,       # TR/redraws_per_TR is the length of the transients, in this case 500 ms

    # fixation point and task params
    'fix_size':                  0.35,       # in dva, outer_rim will be twice this size
    'fix_time_steps':            0.4,        # duration of fix transient in seconds
    'minimum_pulse_gap':         2.0,       # shortest duration between fix transients in seconds
    'task_rate' :                2.0,       # this + minimum_pulse_gap is average of exponential distribution

    # mapper temporal variables:
    'pre_post_ITI':                 4,      # amount of fix no stim trials before and after mapper
    'mapper_stim_in_TR':          4.0,      # duration of mapper stimulus in TRs
    'mapper_ITI_in_TR':           3.5,      # duration of mapper ITI in TRs, round up when scanner = true
}

standard_parameters['element_size'] = standard_parameters['max_ecc']*0.07

if practice == 0:
    response_button_signs = {
    'e':-1,  # left 'less' answer
    'b':1}   # right 'more' answer
elif practice == 1:
    response_button_signs = {
    'z':-1,  # left 'less' answer
    'm':1}   # right 'more' answer

import numpy as np
bar_durations = (np.ceil(standard_parameters['PRF_ITI_in_TR'])+standard_parameters['PRF_period_in_TR']) * 8 *standard_parameters['TR']
fns_durations = (np.ceil(standard_parameters['PRF_ITI_in_TR'])+standard_parameters['fns_period_in_TR']) * 6 *standard_parameters['TR']
print 'PRF run will last %.2fs'%(bar_durations+fns_durations)

n_trials = (3**3 -1 + standard_parameters['pre_post_ITI'] * 2)
mapper_TR_per_trial = np.ceil(standard_parameters['mapper_ITI_in_TR'])+standard_parameters['mapper_stim_in_TR']
print 'Mapper run will last %.2fs'%(n_trials*(mapper_TR_per_trial)*standard_parameters['TR'])


if screen == '7T_bold':
    DISPSIZE = (1920,1080)
    SCREENSIZE = (69.84,39.29) # which about 17.64*9.98 dva (108.22 pixels per degree)
    SCREENDIST = 225
if screen == '3T_bold':
    DISPSIZE = (1920,1080)
    SCREENSIZE = (69.84,39.29) # which about 17.64*9.98 dva (108.22 pixels per degree)
    SCREENDIST = 157    
elif screen == 'K2D38':
    DISPSIZE = (1280,1024)
    SCREENSIZE = (40,30) 
    SCREENDIST = 50
elif screen == 'laptop':
    DISPSIZE = (1920,1080)
    SCREENSIZE = (33,20.7)
    SCREENDIST = 50
elif screen == 'office':
    DISPSIZE = (2560,1440)
    SCREENSIZE = (63.93,42.44) 
    SCREENDIST = 75 # guesstimate
BGC = (128,128,128) # should be (128,128,128), so that fixation task is equally different on light and dark transients
FGC = (0,0,0) # should be (0,0,0), so that fixation task is equally different on light and dark transients

