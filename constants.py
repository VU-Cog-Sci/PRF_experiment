# checken dubbele flash: 
# psychopy realtime mac os -> zit nu in run script
# waitblanking checken in de libscreen -> libscreen maakt een psychopy display aan zonder waitblanking op te geven, maar die is default true

# analyse saccades meer rigoreus doen en toepassen voor trialselectie op gedrag 
# saccade latency histogram maken 
# verwachting van target minimaliseren door exponentiele(?) random interval
# trials kunen nu sneller voor gedrag
    
# remove target if saccade is not detected 100ms after flash
# plot mislocalization as function of flash relative to saccade onset


# SP versie: implement jitter van target onset relatief aan fixatie
# Sacc: terug naar oude versie met index voor terug naar center

location = 'K2D38'# 'office','laptop','K2D38','7T'
full_screen = True#lse

# standard parameters
standard_parameters = {

    ##############################
    # common params
    ##############################

    # define screen size:
    'ref_stim_width':                                 0.05,      # in deg
    'eyetracking_amplitude':                    16,         # custom calibration x-width
    'sa_path_amplitude':                          12,         # width in degrees of sp amplitude
    'sp_path_amplitude':                          8,         # width in degrees of sp amplitude
    'sp_path_elevation':                           0.5,        # ratio of screen height (0.5 for middle)
    'default_answer':                                0,            # for in trial object
    'test_stim_y_offset':                           2.5,         # in degrees, if 0 takes mid between fp and y boundary
    'test_stim_height':                              2,            # in degrees, if 0, takes 1/4 of available y space
    'test_stim_width':                               0.5,          # in degrees 
    'sp_target_size':                                 0.75,         # in degrees # also for fp in saccade exp
    # 'target_max_ecc':                               4,            # in degrees # now set to sp_path_amplitude/4 in the experiment 
    'n_targets':                                          80,          # number of target positions, should be divisible by 4 (one for every eye dir and y position)
    'pupil_tracking_mode':                       0,             # 0: centroid, 1 = ellipse



    ##############################
    # SP  variables:
    ##############################

    # temporal parameters (NOTE: rerun create_ITIs when changing any of these parameters)
    'warming_up_period':                          2,           # in sp cycles (i.e. 1/tf)
    'mean_iti_sp':                                      2,           # in sp cycles (i.e. 1/tf)
    'min_iti_sp':                                         3,           # in sp cycles (i.e. 1/tf)
    'sp_path_temporal_frequency':          0.5,         # in Hz 
    'sp_type' :                                          0,          # 0 for sin, 1 for lin
    'ref_stim_line_width' :                         .01,    # in deg
    'ref_stim_line_factor':                         1,       # scaling of sp_path_amplitude
    
    # other parameters
    'window':                                             True,
    'square_window':                                False,

    ##############################
    # saccade variables
    ##############################

    # temporal parameters (NOTE: rerun create_ITIs when changing any of these parameters)
    'target_delay_mean_left':                     .275,         # in s this is the saccade delay duration 
    'target_delay_mean_right':                   .260,         # in s this is the saccade delay duration 
    'target_delay_window':                         .050,         # [[target_delay_mean - target_delay_window/2] - [target_delay_mean + target_delay_window/2]] is uniform window for target delays
    'offset_delay':                                       .100,
    'mean_iti_precue':                               1,          # in s
    'min_iti_precue':                                  1,             # in s
    'mean_iti_postcue':                             1,          # in s
    'min_iti_postcue':                                2,             # in s
    'return_cue_dur':                                 .500,        # in s

    'saccade_cue_x_offset':                      0.5,
    'saccade_cue_width':                         0.2,
    'saccade_cue_height':                       0.05,

    'ref_stim_width':                                   0.2,       # in deg
    'ref_stim_height':                                  0.5,       # in deg
    'ref_y_offset':                                        4.5,

    'ref_x_offset':                                         2,              
}

# subject_specific_latencies = {
    
#     'ms': [280,290],
#     'de': [275,260],
# }

# print 
    
#############################################
# screen settings 
#############################################

FGC = (255,0,0)
BGC = (0,0,0) # this is converted to -1<->1 in SPSession
FULLSCREEN  = full_screen
if location == 'K2D38':

    # K2D-38 (all in cm):
    DISPSIZE = (1024,768) # at 120 Hz (can be 160 but cant get it to work)
    SCREENSIZE = (39.6,29.7) # conforms to 36.53 by 27.80 (so 28.03 x 27.623 pixels per degree (should be same, but differ slightly due to computation with small angle (why?))), mean 27.83
    SCREENDIST = 50.0#60.0

elif location == '7T':
    #7T scan room (all in cm):
    DISPSIZE = (1920,1080)# at 120 Hz
    SCREENSIZE = (69.84,39.29) #physical screen size in centimeters
    SCREENDIST = 225 # centimeters; distance between screen and participant's eyes

elif location == 'office':
    #office screen
    DISPSIZE = (2560,1440) # at .. Hz
    SCREENSIZE = (59.83,33.72)# physical screen size in centimeters
    SCREENDIST = 75# centimeters; distance between screen and participant's eyes

elif location == 'laptop':
   
    #MBP screen
    DISPSIZE = (1920,1080) # at 60 Hz
    SCREENSIZE = (20.71 ,30.72)# guesstimates (height and depth with estimated 1 cm *2 edge space)
    SCREENDIST = 50 # guesstimate centimeters; distance between screen and participant's eyes 



