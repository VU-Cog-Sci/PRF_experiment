

# standard parameters
standard_parameters = {

    # for pilotting
    # define screen size:
    'sp_path_amplitude':               20,# 0.95,       # ratio of screen widht (1.0 for full width, 0 for standstill at fixation)
    'sp_path_elevation':                0.8,        # ratio of screen height (0.5 for middle)
    
    ## common parameters:
    'TR':                               0.944,        # VERY IMPORTANT TO FILL IN AFTER PLANNING IN!            
    'minimal_iti':                      2,  # int
    ## SP experiment variables:
    'test_stim_y_offset':                 2,    #if 0, takes mid between fp and y boundary
    'test_stim_height':                 3,        # if 0, takes 1/3 of available y space
    'test_stim_width':                  0.2,        # 0.125 * 0.
    'sp_target_size':                   4,        #
    'sp_path_temporal_frequency':       1.0,        #
    'test_stim_1_color':                (1,1,1),#(1, -1, -1),        # 
    'test_stim_2_color':                (1,1,1),#(-1, 1, -1),        # 

    'test_stim_positions':              [-3,-1,0,1,3],        # 

    ## mapper variables:
    'mapper_stim_in_TR':                2.0,        # duration of mapper stimulus in TRs
    'mapper_ITI_in_TR':                 1.0,        # duration of mapper ITI in TRs

    ## Color matcher variables:
    'num_trials':                       10,        # amount of matcher trials
    'BY_comparison_color':              0.5,        # color to compare to; 0.5 is best.

    'pupil_tracking_mode':              0,# 0: centroid, 1 = ellipse
}

response_button_signs = {
'e':-1,  # left answer 
'b':1,   # right answer   
'y':0}   # confirm color match
# }      
    
background_color = (-1, -1, -1)#-0.75,-0.75,-0.75)
full_screen = False
# screen settings:
DISPSIZE = (1024,768)#(1920,1080)
SCREENSIZE = (39.0,29.0)#(33.8,27.1) # physical screen size in centimeters
SCREENDIST = 60.0#65.0#57.0 # centimeters; distance between screen and participant's eyes

#(1280,1024)#(1024,768)#(1680,1050)#(1280,1024) # canvas size
# in case of 7T scanner:
# SCREENSIZE = (49.1,79,7)
# SCREENDIST = 225
# K2D-38:
