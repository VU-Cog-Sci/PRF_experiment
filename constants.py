

# standard parameters
standard_parameters = {

    # define screen size:
    'sp_path_amplitude':                20,# 0.95,       # ratio of screen widht (1.0 for full width, 0 for standstill at fixation)
    'sp_path_elevation':                0.6,        # ratio of screen height (0.5 for middle)
    
    ## common parameters:
    'TR':                               0.944,        # VERY IMPORTANT TO FILL IN AFTER PLANNING IN!            
    'minimal_iti':                      2,  # int should be eve number 
    'warming_up_n_TRs':                 2,#18, # this + 2 is the period before and after experiment while scanner is running
    
    ## SP  variables:
    'test_stim_y_offset':               2,# 2,    #if 0, takes mid between fp and y boundary
    'test_stim_height':                 2,#3,        # if 0, takes 1/3 of available y space
    'test_stim_width':                  0.4,        # 0.125 * 0.
    'sp_target_size':                   1,        #
    'sp_path_temporal_frequency':       0.5,#25,#1.0,        #
    'test_stim_positions':              [-3,-1,0,1,3],        # 

    'pupil_tracking_mode':              0,# 0: centroid, 1 = ellipse


    ##############
    # Mapper vars
    ##############
    'mapper_period_in_TR':                10, # 
    'mapper_n_trials':                    10, # should be even number (otherwise more SP than fix trials)

}

    
#############################################
# screen settings 
#############################################

full_screen = False
FGC = (255,0,0)
BGC = (0,0,0) # this is converted to -1<->1 in SPSession


# K2D-38 (all in cm):
DISPSIZE = (1024,768)
SCREENSIZE = (39.0,29.0)
SCREENDIST = 60.0
#7T scan room (all in cm):
#DISPSIZE = (1280,720)#(1280,720)#,1080)#(1024,768)#(1920,1080)
#SCREENSIZE = (69.84,39.29)#(79.7,49.1)#(39.0,29.0)#(33.8,27.1) # physical screen size in centimeters
#SCREENDIST = 225#60.0#65.0#57.0 # centimeters; distance between screen and participant's eyes

