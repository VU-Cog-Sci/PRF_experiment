
location = 'laptop'# 'office','laptop','K2D38','7T'
full_screen = False#lse

# standard parameters
standard_parameters = {

    ##############################
    # common params
    ##############################

    # define screen size:
    'ref_stim_width':                                 0.05,      # in deg
    'eyetracking_amplitude':                    15,         # custom calibration x-width
    'sp_path_amplitude':                          15,         # width in degrees of sp amplitude
    'sp_path_elevation':                           0.5,        # ratio of screen height (0.5 for middle)
    'default_answer':                                0,            # for in trial object
    'test_stim_y_offset':                           1.5,         # in degrees, if 0 takes mid between fp and y boundary
    'test_stim_height':                              2,            # in degrees, if 0, takes 1/4 of available y space
    'test_stim_width':                               0.4,          # in degrees 
    'sp_target_size':                                 0.5,         # in degrees # also for fp in saccade exp
    'target_max_ecc':                               3,            # in degrees
    'n_targets':                                          80,          # number of target positions, should be divisible by 4 (one for every eye dir and y position)
    'pupil_tracking_mode':                       0,             # 0: centroid, 1 = ellipse

    'ref_stim_width':                                   0.01,       # in deg
    'ref_stim_height':                                  0.5,       # in deg

    ##############################
    # SP  variables:
    ##############################

    # temporal parameters (NOTE: rerun create_ITIs when changing any of these parameters)
    'warming_up_period':                          2,           # in sp cycles (i.e. 1/tf)
    'mean_iti_sp':                                      2,           # in sp cycles (i.e. 1/tf)
    'min_iti_sp':                                         3,           # in sp cycles (i.e. 1/tf)
    'sp_path_temporal_frequency':          0.7,         # in Hz 
    'sp_type' :                                        1,          # 0 for sin, 1 for lin

    # other parameters
    'window':                                             False,
    'moving_window':                                False,

    ##############################
    # saccade variables
    ##############################

    # temporal parameters (NOTE: rerun create_ITIs when changing any of these parameters)
    'target_delay':                                      .150,         # in s this is the saccade delay duration
    'mean_iti_precue':                               1,          # in s
    'min_iti_precue':                                  1.5,             # in s
    'mean_iti_postcue':                             1,          # in s
    'min_iti_postcue':                                1.5,             # in s
    'return_cue_dur':                                 .100,        # in s

}

# print 
    
#############################################
# screen settings 
#############################################

FGC = (255,0,0)
BGC = (0,0,0) # this is converted to -1<->1 in SPSession

if location == 'K2D38':

    # K2D-38 (all in cm):
    DISPSIZE = (1280,1024)
    SCREENSIZE = (39.0,29.0)
    SCREENDIST = 60.0

elif location == '7T':
    #7T scan room (all in cm):
    DISPSIZE = (1920,1080)#(1280,720)#,1080)#(1024,768)#(1920,1080)
    SCREENSIZE = (69.84,39.29) #physical screen size in centimeters
    SCREENDIST = 225 # centimeters; distance between screen and participant's eyes

elif location == 'office':
    #office screen
    DISPSIZE = (2560,1440)#(1280,720)#,1080)#(1024,768)#(1920,1080)
    SCREENSIZE = (59.83,33.72)# physical screen size in centimeters
    SCREENDIST = 75# centimeters; distance between screen and participant's eyes

elif location == 'laptop':
   
    #MBP screen
    DISPSIZE = (1920,1080)#(1280,720)#,1080)#(1024,768)#(1920,1080)
    SCREENSIZE = (20.71 ,30.72)# guesstimates (height and depth with estimated 1 cm *2 edge space)
    SCREENDIST = 50 # guesstimate centimeters; distance between screen and participant's eyes 



