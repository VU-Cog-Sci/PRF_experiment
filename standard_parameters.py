

# standard parameters
standard_parameters = {
    
    'practice':                         True,
    ## common parameters:
    'TR':                               0.944,        # VERY IMPORTANT TO FILL IN AFTER PLANNING IN!            
    'minimal_iti':                      2.0
    ## SP experiment variables:
    'test_stim_width':                  0.1,        # 0.125 * 0.
    'test_stim_height':                 4,        # 
    'sp_target_size':                   4,        #
    'sp_path_temporal_frequency':       1.0,        #
    'sp_path_amplitude':                0.8,        # ratio of screen widht (1.0 for full width, 0 for standstill at fixation)
    'sp_path_elevation':                0.8,        # ratio of screen height (0.5 for middle)
    'test_stim_1_color':                (1, -1, -1),        # 
    'test_stim_2_color':                (-1, 1, -1),        # 

    'test_stim_positions':              [-3,-1,0,1,3],        # 


    ## mapper variables:
    'mapper_stim_in_TR':                2.0,        # duration of mapper stimulus in TRs
    'mapper_ITI_in_TR':                 1.0,        # duration of mapper ITI in TRs

    ## Color matcher variables:
    'num_trials':                       10,        # amount of matcher trials
    'BY_comparison_color':              0.5,        # color to compare to; 0.5 is best.
}

response_button_signs = {
'e':-1,  # left 'less' answer  e
'b':1,   # right 'more' answer   b
'y':0}   # confirm color match y 
# }      
    
screen_res = (1920,1080)    
background_color = (-1, -1, -1)#-0.75,-0.75,-0.75)
