
from __future__ import division

# standard parameters
standard_parameters = {
    
    'eyelink_calib_size':               0.5,     

    'stim_size':                        200,            
    'stim_x_offset':                    170,    
    'stim_spatial_frequency':           0.0375,  
    'stim_flicker_freq':                8.0,       
    
    'block_duration_minimum':           6,        
    'block_duration_range':             8,
    'total_nr_trials':                  60,
    'total_ITI_tolerance':              0.025,

    'high_reward_probability':          0.8,
    'TR':                               0.945,     

    'stim_dur' :                        0.75,       
    'fb_dur' :                          1.0,       
    'ITI_minimum':                      1.5,       
    'ITI_mean':                         2.0        
}

# response_button_signs = {
# 'e':-1,  # left 'less' answer  e
# 'b':1,   # right 'more' answer   b
# 'y':2}   # confirm color match y 

response_button_signs = {
        'f':-1,  # left 'less' answer  e
        'j':1,   # right 'more' answer   b
        'y':2}   # confirm color match y 
# }      

# screen_res = (1920,1080)
# background_color = (0.5,0.5,0.5)#-0.75,-0.75,-0.75)

full_screen = True
FGC = (0,0,0)
BGC = (255*0.5,255*0.5,255*0.5) # this is converted to -1<->1 in SPSession

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


