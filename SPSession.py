from __future__ import division
from psychopy import visual, core, misc, event
import numpy as np
# from IPython import embed as shell
from math import *

import os, sys, time, pickle
import pygame
from pygame.locals import *
# from pygame import mixer, time

import Quest

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

from Session import *
from PRFTrial import *
from standard_parameters import *

import appnope
appnope.nope()

class SPSession(EyelinkSession):
    def __init__(self, subject_initials, index_number,scanner, tracker_on):
        super(SPSession, self).__init__( subject_initials, index_number)

        screen = self.create_screen( size = screen_res, full_screen =1, physical_screen_distance = 225.0, background_color = background_color, physical_screen_size = (70, 40) )
        event.Mouse(visible=False, win=screen)

        self.create_output_file_name()
        if tracker_on:
            self.create_tracker(auto_trigger_calibration = 1, calibration_type = 'HV9')
            if self.tracker_on:
                self.tracker_setup()
        else:
            self.create_tracker(tracker_on = False)
        
        self.response_button_signs = response_button_signs

        self.scanner = scanner
        # trials can be set up independently of the staircases that support their parameters
        self.prepare_trials()
        self.prepare_sounds()

    def prepare_sounds(self):
        for ut in np.unique(self.task_instructions):
            self.read_sound_file('sounds/%s.wav'%ut.lower())
            
    def prepare_trials(self):
        """docstring for prepare_trials(self):"""

        self.standard_parameters = standard_parameters

        x_test_positions = np.array(np.meshgrid(self.standard_parameters['test_stim_positions'], self.standard_parameters['test_stim_positions'])).T.reshape((-1,2))
        x1, x2 = x_test_positions[:,0], x_test_positions[:,1]

        y_test_positions = np.concatenate((-1 * np.ones(x_test_positions.shape[0]), np.ones(x_test_positions.shape[0])))

        x_test_positions = np.array([np.repeat(x1, 4), np.repeat(x2, 4)]).T
        y_test_positions = np.repeat(y_test_positions, 2)

        self.trial_array = np.array([[self.subdirections[i], self.subtasks[i]] for i in range(len(self.subtasks))])

        self.trial_order = np.arange(y_test_positions.shape[0])
        np.random.shuffle(self.trial_order)

        # stopped here. 
        inter_trial_intervals = 

    
        self.phase_durations = np.array([
            -0.0001, # instruct time, skipped in all trials but the first
            0.5, # smooth pursuit
            0.5 / self.standard_parameters['sp_path_temporal_frequency'], # play the sound for 'upcoming stimulus'
            0.5 / self.standard_parameters['sp_path_temporal_frequency'], # present stimulus 1 at onset of this phase
            0.5 / self.standard_parameters['sp_path_temporal_frequency'], # present stimulus 2 at onset of this phase
            self.standard_parameters['minimal_iti'] 
            ] )    

        # fixation point
        self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=12.5, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
        self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=22.5, pos = np.array((0.0,0.0)), color = (0.0,0.0,0.0), maskParams = {'fringeWidth':0.4})
        self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=9.0, pos = np.array((0.0,0.0)), color = (1.0,1.0,1.0), opacity = 1.0, maskParams = {'fringeWidth':0.4})
        
        self.test_stim_1 = visual.Rect(self.screen, 
                            width = self.standard_parameters['sp_path_temporal_frequency'], 
                            height = self.standard_parameters['test_stim_height'], 
                            color = self.standard_parameters['test_stim_1_color'])
        self.test_stim_2 = visual.Rect(self.screen, 
                            width = self.standard_parameters['sp_path_temporal_frequency'], 
                            height = self.standard_parameters['test_stim_height'], 
                            color = self.standard_parameters['test_stim_2_color'])

    
    def close(self):
        super(SPSession, self).close()        
    
    def run(self):
        """docstring for fname"""
        # cycle through trials
        for i in range(len(self.trial_array)):
            # prepare the parameters of the following trial based on the shuffled trial array
            this_trial_parameters = self.standard_parameters.copy()

            these_phase_durations = self.phase_durations.copy()

            this_trial = PRFTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
            
            # run the prepared trial
            this_trial.run(ID = i)
            if self.stopped == True:
                break
        self.close()
    

