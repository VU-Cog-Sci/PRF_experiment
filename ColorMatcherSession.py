from __future__ import division
from psychopy import visual, core, misc, event
import numpy as np
from IPython import embed as shell
from math import *

import os, sys, time, pickle
import pygame
from pygame.locals import *
# from pygame import mixer, time

import Quest

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

from Session import *
from ColorMatcherTrial import *
from constants import *
from Staircase import YesNoStaircase

import appnope
appnope.nope()

class ColorMatcherSession(EyelinkSession):
    def __init__(self, subject_initials, index_number, scanner, tracker_on):
        super(ColorMatcherSession, self).__init__( subject_initials, index_number)
        
        self.background_color = (np.array(BGC)/255*2)-1

        screen = self.create_screen( size = DISPSIZE, full_screen =full_screen, physical_screen_distance = SCREENDIST, 
            background_color = self.background_color, physical_screen_size = SCREENSIZE, wait_blanking = True, screen_nr = 1 )
        screen=self.create_screen( size = screen_res, full_screen = 1, physical_screen_distance = 159.0, background_color = background_color, physical_screen_size = (70, 40) )
        event.Mouse(visible=False, win=screen)

        self.standard_parameters = standard_parameters
        self.response_button_signs = response_button_signs

        self.create_output_file_name()
        if tracker_on:
            self.create_tracker(auto_trigger_calibration = 1, calibration_type = 'HV9')
            if self.tracker_on:
                self.tracker_setup()
        else:
            self.create_tracker(tracker_on = False)
        
        self.scanner = scanner
        # trials can be set up independently of the staircases that support their parameters
        self.prepare_trials()
        self.all_color_values = []
        self.exp_start_time = 0.0
        self.color_step = 0.02

    
    def prepare_trials(self):
        """docstring for prepare_trials(self):"""
        
        self.RG_offsets = (np.random.rand(self.standard_parameters['num_trials']))

        self.phase_durations = np.array([-0.0001,-0.0001, 1.00, -0.0001, 0.001])
        
        # stimuli
        self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=12.5, pos = np.array((0.0,0.0)), color = (0,0,0), maskParams = {'fringeWidth':0.4})
        self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=17.5, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
        self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=9.0, pos = np.array((0.0,0.0)), color = (0,0,0), opacity = 1.0, maskParams = {'fringeWidth':0.4})

        screen_width, screen_height = self.screen_pix_size
        
        # mask
        if self.standard_parameters['mask_type'] ==1:
            draw_screen_space = [self.screen_pix_size[0]*self.standard_parameters['horizontal_stim_size'],self.screen_pix_size[1]*self.standard_parameters['vertical_stim_size']]
            mask = np.ones((self.screen_pix_size[1],self.screen_pix_size[0]))*-1
            x_edge = int(np.round((self.screen_pix_size[0]-draw_screen_space[0])/2))
            y_edge = int(np.round((self.screen_pix_size[1]-draw_screen_space[1])/2))
            if x_edge > 0:
                mask[:,:x_edge] = 1
                mask[:,-x_edge:] = 1
            if y_edge > 0:
                mask[-y_edge:,:] = 1
                mask[:y_edge,:] = 1
            import scipy
            mask = scipy.ndimage.filters.gaussian_filter(mask,5)
            self.mask_stim = visual.PatchStim(self.screen, mask=mask,tex=None, size=[self.screen_pix_size[0],self.screen_pix_size[1]], pos = np.array((self.standard_parameters['x_offset'],0.0)), color = self.screen.background_color) # 
        elif self.standard_parameters['mask_type'] == 0:
            mask = filters.makeMask(matrixSize = self.screen_pix_size[0], shape='raisedCosine', radius=self.standard_parameters['vertical_stim_size']*self.screen_pix_size[1]/self.screen_pix_size[0]/2, center=(0.0, 0.0), range=[1, -1], fringeWidth=0.1 )
            self.mask_stim = visual.PatchStim(self.screen, mask=mask,tex=None, size=[self.screen_pix_size[0]*2,self.screen_pix_size[0]*2], pos = np.array((self.standard_parameters['x_offset'],0.0)), color = self.screen.background_color) # 
    
    def close(self):
        super(ColorMatcherSession, self).close()
        text_file = open("data/%s_color_ratios.txt"%self.subject_initials, "w")
        text_file.write('Mean RG/BY ratio: %.2f\nStdev RG/BY ratio: %.2f'%(np.mean(np.array(self.all_color_values)/self.standard_parameters['BY_comparison_color']),np.std(np.array(self.all_color_values)/self.standard_parameters['BY_comparison_color'])))
        text_file.close()
    
    def run(self):
        """docstring for fname"""
        # cycle through trials
        for i in range(self.standard_parameters['num_trials']):
            # prepare the parameters of the following trial based on the shuffled trial array
            this_trial_parameters = self.standard_parameters.copy()
            this_trial_parameters['RG_offset'] = self.RG_offsets[i]

            these_phase_durations = self.phase_durations.copy()

            this_trial = ColorMatcherTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
            
            # run the prepared trial
            this_trial.run(ID = i)
            if self.stopped == True:
                break
        self.close()
    

