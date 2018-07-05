
from __future__ import division
import numpy as np
import sys

if len(sys.argv)>1:
    wanted_dur = 24. # in seconds

    #rest is computed
    TR = float(sys.argv[1])/1000. # should be given in ms in terminal
    nr_TRs = np.int(np.round(wanted_dur/TR))
    print '\n%d TRs of %.3fs makes %.3fs per bar pass, total of %.3fm\n'%(nr_TRs,TR,TR*nr_TRs,TR*nr_TRs*7/60)
else:
    print '\n\n\n!!!please indicate the desired TR in ms as first argument!!!\n\n\n'
    exit()

# standard parameters
standard_parameters = {
    
    'practice':                         0,
    ## spatial dimensions:
    'eyelink_calib_size':               0.5,       # portion of screen heigth
    'mask_type':                        1,         # 0: circle, 1: square
    'vertical_stim_size':               1,            # portion of horizontal screen space covered
    'horizontal_stim_size':             1,         # when wanting a circular mask, set this to screen_size[1]/screen_size[0]
    'x_offset':                         0,          # when wanting a circular mask, x-offset
    'bar_width_ratio':                  0.125,        # portion of screen height
    
    ## temporal dimensions:
    ## common parameters:    # 351 dyns
    'num_elements':                     4000,        # amount of elements in bar, this will be num_elements * (1/bar_width_ratio) = 8000 for Mapper
    'vertical_pass_dur':                int(2.0*nr_TRs/3.0),#32,        # that is 24*1.5=36 sec, which is 15/24 = 0.625 degree per step 
    'horizontal_pass_dur':              nr_TRs,#32,
    'nr_staircases_ecc':                4,
    'PRF_ITI_in_TR':                    0.5,        # fill in 0.5 less than wanted to accomodate for t waiting
    'TR':                               TR,#1.3,        # VERY IMPORTANT TO FILL IN AFTER PLANNING IN!            
    'redraws_per_TR' :                  3.0,        # TR/redraws_per_TR is the length of the transients, in this case 500 ms: #used e
    'fast_speed':                       12.0,        # speed of the fast elements for TK/DE/JW: 6, for JS/SN/NA: 7
    'slow_speed':                       7.0,        # speed of the slow elements for TK/DE/JW: 4, for JS/SN/NA: 3
    'element_size':                     45.0,        # size of the elements # used: 35
    'element_spatial_frequency':        2,        # sf of the elemenets # used: 2

    ## stim feature params
    'fast_speed':                       12.0,        # speed of the fast elements for TK/DE/JW: 6, for JS/SN/NA: 7
    'num_fns_trials':                   4,        # speaks for itself

    ## mapper variables:
    'mapper_stim_in_TR':                1.0,        # duration of mapper stimulus in TRs
    'minimum_pulse_gap':                2.0,
    'warming_up_n_TRs':                 12,
    'mapper_task_rate':                 4,

    ## Color matcher variables:
    'num_trials':                       10,        # amount of matcher trials
    'BY_comparison_color':              0.5,        # color to compare to; 0.5 is best.

    # staircase variables:
    'quest_initial_stim_values':        1,
    'quest_stepsize':                   0.75,
    'quest_stepsize_multiplication_on_reversal': 0.95
}

# response_button_signs = {
# 'e':-1,  # left 'less' answer  e
# 'b':1,   # right 'more' answer   b
# 'y':2}   # confirm color match y 

# response_button_signs = {
#         'b':-1,  # left 'less' answer  e
#         'y':1,   # right 'more' answer   b
#         'g':2}   # confirm color match y 
# }      
# response_button_signs = {
#         'b':-1,
#         'y':1
#         }

response_button_signs = {
        'e':-1,
        'w':1
        }
# screen_res = (1920,1080)
# background_color = (0.5,0.5,0.5)#-0.75,-0.75,-0.75)

full_screen = True
FGC = (0,0,0)
BGC = (255*0.75,255*0.75,255*0.75) # this is converted to -1<->1 in SPSession

# K2D-38 (all in cm):
#DISPSIZE = (1024,768)
#SCREENSIZE = (39.0,29.0)
#SCREENDIST = 60.0
#7T scan room (all in cm):
#DISPSIZE = (1024,768)
DISPSIZE = (1920,1080)#(2560,1440)#(1280,720)#,1080)#(1024,768)#(1920,1080)#(2560,1440)
SCREENSIZE = (69.84,39.29) #physical screen size in centimeters
SCREENDIST = 225#60.0#65.0#57.0 # centimeters; distance between screen and participant's eyes
#office screen
# DISPSIZE = (2560,1440)#(1280,720)#,1080)#(1024,768)#(1920,1080)
# SCREENSIZE = (59.83,33.72)# physical screen size in centimeters
# SCREENDIST = 75# centimeters; distance between screen and participant's eyes


