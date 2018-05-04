

# standard parameters
standard_parameters = {

    ##############################
    # Smooth pursuit experiment vars
    ##############################

    # define screen size:
    'ref_stim_width':                                   0.05,      # in deg
    'eyetracking_amplitude':                    15,         # custom calibration x-width
    'sp_path_amplitude':                          15,         # width in degrees of sp amplitude
    'sp_path_elevation':                           0.7,        # ratio of screen height (0.5 for middle)
    
    ## common parameters:
    'TR':                                                   0.945,     # VERY IMPORTANT TO FILL IN AFTER PLANNING IN!            
    'minimal_iti':                                       2,            # should be an even integer
    'warming_up_n_TRs':                        4,            # this is the period before and after experiment while scanner is running
    
    ## SP  variables:
    'test_stim_y_offset':                           1.5,         # in degrees, if 0 takes mid between fp and y boundary
    'test_stim_height':                              2,            # in degrees, if 0, takes 1/4 of available y space
    'test_stim_width':                               0.4,          # in degrees 
    'sp_target_size':                                 0.5,         # in degrees
    'sp_path_temporal_frequency':          0.5,         # per TR
    'target_max_ecc':                               3,            # in degrees
    'n_targets':                                         5,             # number of target positions, right now ony 3/5/8 is possible (otherwise ITIs are messed with)
    'n_target_reps':                                  3,             # n_target_reps * n_targets * 4 is amount of trials
    'pupil_tracking_mode':                       0,             # 0: centroid, 1 = ellipse

    'default_answer':                                0,            # for in trial object

    ##############################
    # Additional saccade experiment vars
    ##############################
    'fp_dim_dur':                                       .150,        # in s duration of fixation dim
    'fp_dim_delay':                                    .200,       # in s this is the saccade delay duration

}

# print 
    
#############################################
# screen settings 
#############################################

full_screen = False
FGC = (255,0,0)
BGC = (0,0,0) # this is converted to -1<->1 in SPSession


# K2D-38 (all in cm):
#DISPSIZE = (1024,768)
#SCREENSIZE = (39.0,29.0)
#SCREENDIST = 60.0
#7T scan room (all in cm):
#DISPSIZE = (1024,768)
DISPSIZE = (1920,1080)#(1280,720)#,1080)#(1024,768)#(1920,1080)
SCREENSIZE = (69.84,39.29) #physical screen size in centimeters
SCREENDIST = 225#60.0#65.0#57.0 # centimeters; distance between screen and participant's eyes
#office screen
#DISPSIZE = (2560,1440)#(1280,720)#,1080)#(1024,768)#(1920,1080)
#SCREENSIZE = (59.83,33.72)# physical screen size in centimeters
#SCREENDIST = 75# centimeters; distance between screen and participant's eyes


