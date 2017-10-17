####################################
#  !!! ADJUST THESE PARAMETERS!!!  #
####################################
TR = 1.5
practice = 0
response_button_signs = {
'e':-1,  # left 'less' answer
'b':1,   # right 'more' answer
'y':2}   # confirm color match
screen = '7T_bold'
# screen = 'K2D38'
# screen = 'laptop'
FULLSCREEN = True

standard_parameters = {
    
    ## ADJUST THESE PARAMETERS
    'practice':             practice,
    'TR':                         TR,       #         

    # stimulus params (spatial)
    'max_ecc':                     5,         # in dva
    'num_elements':             1500,       # amount of elements in bar, this will be num_elements * (1/bar_width_ratio) = 8000 for Mapper
    'fast_speed':                6.0,       # speed of the fast elements
    'slow_speed':                4.0,       # speed of the slow elements
    'element_size':             0.35,       # size of the elements in dva
    'element_sf_min':           0.5,        # min sf of the elemenets
    'element_sf_mean':          5,          # mean sf of the elemenets
    'bar_width_ratio':          0.125,      # 0.125 * 0.9 * screen heigth = 3.375

    # stim params (temporal)
    'PRF_period_in_TR':           20,       # that is 20*1.5=30 sec, which is 10/20 = 0.5 degree per step
    'fns_period_in_TR':           10,       # that is 10*1.5=15 sec, which is 10/20 = 0.5 degree per step
    'PRF_ITI_in_TR':             0.5,       # that is 2*1.5 = 3 sec
    'redraws_per_TR' :           3.0,       # TR/redraws_per_TR is the length of the transients, in this case 500 ms

    # fixation point and task params
    'fix_size':                 0.15,       # in dva, outer_rim will be twice this size
    'fix_time_steps':           0.4,        # duration of fix transient in seconds
    'minimum_pulse_gap':         2.0,       # shortest duration between fix transients in seconds
    'task_rate' :                2.0,       # this + minimum_pulse_gap is average of exponential distribution

    # mapper temporal variables:
    'pre_post_ITI':                 4,      # amount of fix no stim trials before and after mapper
    'mapper_stim_in_TR':          2.0,      # duration of mapper stimulus in TRs
    'mapper_ITI_in_TR':           2.0,      # duration of mapper ITI in TRs  so mapper duration is 
}

import numpy as np
TR_per_trial = np.ceil(standard_parameters['PRF_ITI_in_TR'])+standard_parameters['PRF_period_in_TR']
print 'PRF run will last %.2fs'%(14*(TR_per_trial)*standard_parameters['TR'])

n_trials = (3**3 -1 + standard_parameters['pre_post_ITI'] * 2)
mapper_TR_per_trial = np.ceil(standard_parameters['mapper_ITI_in_TR'])+standard_parameters['mapper_stim_in_TR']
print 'PRF run will last %.2fs'%(n_trials*(mapper_TR_per_trial)*standard_parameters['TR'])


if screen == '7T_bold':
    DISPSIZE = (1920,1080)
    SCREENSIZE = (69.84,39.29) # which about 17.64*9.98 dva (108.22 pixels per degree)
    SCREENDIST = 225
elif screen == 'K2D38':
    DISPSIZE = (1280,1024)
    SCREENSIZE = (40,30) # which about 
    SCREENDIST = 50
elif screen == 'laptop':
    DISPSIZE = (1920,1080)
    SCREENSIZE = (33,20.7) # which about 
    SCREENDIST = 50

BGC = (128,128,128) # should be (128,128,128), so that fixation task is equally different on light and dark transients
FGC = (0,0,0) # should be (0,0,0), so that fixation task is equally different on light and dark transients

