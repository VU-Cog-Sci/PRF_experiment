
from __future__ import division
import numpy as np

####################################
#  !!! ADJUST THESE PARAMETERS!!!  #
####################################
TR = 1.9
n_TR_vertical_pass = 15
practice = 1
screen = '7T_bold'
# screen = 'office'
# screen = 'K2D-38'
# screen = 'laptop'
FULLSCREEN = True

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
elif screen == 'K2D-38':    
    DISPSIZE = (1280,1024)
    SCREENSIZE = (39.0,29.0)
    SCREENDIST = 50.0

# standard parameters
standard_parameters = {
    
    'practice':                         practice,
    ## spatial dimensions:
    'eyelink_calib_size':               0.5,        # portion of screen heigth
    'mask_type':                        1,          # 0: circle, 1: square
    'vertical_stim_size':               1,          # portion of horizontal screen space covered
    'horizontal_stim_size':             1,          # only does something when mask == 1, otherwise this is set to DISPSIZE[1]/DISPSIZE[0] in session
    'x_offset':                         0,          # when wanting a circular mask, x-offset
    'bar_width_ratio':                  0.1,      # portion of screen height (in both directions)
    'fix_size':                          0.25,      # in dva, outer_rim will be twice this size

    ## temporal dimensions:
    'num_elements':                     1500,       # amount of elements in bar, this will be num_elements * (1/bar_width_ratio) = 8000 for Mapper
    'vertical_pass_dur':                n_TR_vertical_pass,         # that is 15*1.9=28.5 sec, which is about 10/15 = 0.66 degree per step
    'PRF_ITI_in_TR':                    0.5,        # fill in 0.5 less than wanted to accomodate for t waiting
    'TR':                               TR,         # VERY IMPORTANT TO FILL IN AFTER PLANNING IN!            
    'redraws_per_TR' :                  3.0,        # TR/redraws_per_TR is the length of the transients, in this case 500 ms: #used e
    'fast_speed':                       7.0,        # speed of the fast elements for TK/DE/JW: 6, for JS/SN/NA: 7
    'slow_speed':                       3.0,        # speed of the slow elements for TK/DE/JW: 4, for JS/SN/NA: 3
    'element_size':                     35.0,       # size of the elements # used: 35
    'element_sf_min':                   0.5,        # min sf of the elemenets
    'element_sf_mean':                    5,         # this + min is mean sf of the elemenets

    ## mapper variables:
    'mapper_stim_in_TR':                1.0,        # duration of mapper stimulus in TRs
    'minimum_pulse_gap':                2.0,
    'warming_up_n_TRs':                 18,
    'mapper_task_rate':                 4,

    ## Color matcher variables:
    'num_trials':                       10,         # amount of matcher trials
    'BY_comparison_color':              0.5,        # color to compare to; 0.5 is best.
    'matcher_num_elements':            10000,

    # staircase variables:
    'initial_stim_values':                      1,
    'stepsize':                              0.75,
    'stepsize_multiplication_on_reversal':   0.95,
    'nr_staircases_ecc':                        4,# for the left-right bar passes 4, for horizontal 3
}

standard_parameters['horizontal_pass_dur'] = np.ceil(SCREENSIZE[0]/SCREENSIZE[1] * standard_parameters['vertical_pass_dur'])


n_empty_trials = 3
n_vertical_passes = 2
n_horizontal_passes = 2
n_vertical_trials = n_vertical_passes + n_empty_trials
n_horizontal_trials = n_horizontal_passes
n_TRs = (n_horizontal_trials * (standard_parameters['horizontal_pass_dur']+1)) + (n_vertical_trials * (standard_parameters['vertical_pass_dur']+1))
duration_minutes = (n_TRs*TR)/60.

print '\n\n\n'
print 'PRF run in scanner will last %d TRs of %.3fs (%.0f minutes, %.0f seconds)'%(n_TRs,TR,duration_minutes,np.ceil((duration_minutes-np.floor(duration_minutes))*60.))
print '\n\n\n'

if practice == 0:
    response_button_signs = {
    'e':-1,  # left 'less' answer  e
    'b':1,   # right 'more' answer   b
    'y':2}   # confirm color match y 
elif practice == 1:
    response_button_signs = {
    'f':-1,  # left 'less' answer  e
    'j':1,   # right 'more' answer   b
    'k':2}   # confirm color match y 

FGC = (0,0,0)
BGC = (255*0.5,255*0.5,255*0.5) # this is converted to -1<->1 in SPSession


