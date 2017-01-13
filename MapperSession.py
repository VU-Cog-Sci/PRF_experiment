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
from MapperTrial import *
from standard_parameters import *
from Staircase import YesNoStaircase

import appnope
appnope.nope()

class MapperSession(EyelinkSession):
    def __init__(self, subject_initials, index_number, scanner, tracker_on):
        super(MapperSession, self).__init__( subject_initials, index_number)
        
        screen=self.create_screen( size = screen_res, full_screen = 0, physical_screen_distance = 159.0, background_color = background_color, physical_screen_size = (70, 40) )
        event.Mouse(visible=False, win=screen)

        self.standard_parameters = standard_parameters
        self.response_button_signs = response_button_signs

        text_file_name = "data/%s_color_ratios.txt"%self.subject_initials
        assert os.path.isfile(text_file_name), 'NO COLOR RATIO TEXT FILE PRESENT!!!!!!!!'
        text_file = open(text_file_name, "r")
        RG_BY_ratio = float(text_file.readline().split('ratio: ')[-1][:-1])
        text_file.close()
        if RG_BY_ratio > 1:
            self.standard_parameters['RG_color'] = 1
            self.standard_parameters['BY_color'] = 1/RG_BY_ratio
        else:
            self.standard_parameters['BY_color'] = 1
            self.standard_parameters['RG_color'] = 1/RG_BY_ratio


        # text_file_name = "data/%s_speed_ratios.txt"%self.subject_initials
        # assert os.path.isfile(text_file_name), 'NO SPEED RATIO TEXT FILE PRESENT!!!!!!!!'
        # text_file = open(text_file_name, "r")
        # self.fast_ratio = float(text_file.readline().split('ratio: ')[-1][:-1])
        # self.slow_ratio = 1-self.fast_ratio
        self.fast_ratio = self.slow_ratio = 0.5

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
        self.prepare_staircases()

        self.ready_for_next_pulse = True
        self.exp_start_time = 0.0

        # setup fix transient and redraws in session to let it continuously run. This happens in multitudes of 'time_steps', which is equal to the redraw steps in the PRF experiment.
        self.time_steps = self.standard_parameters['TR']/self.standard_parameters['redraws_per_TR']
        self.transient_occurrences = np.round(np.cumsum(np.random.exponential(self.standard_parameters['task_rate'], size = 20000) + self.standard_parameters['minimum_pulse_gap']) * (1/self.time_steps)) / (1/self.time_steps)



    def prepare_staircases(self):
        # staircases
        self.initial_value = 2 # for self.unique_tasks, 
        self.staircase_file_name = os.path.join(os.path.split(self.output_file)[0], self.subject_initials + '_mapper_quest.pickle')
        if os.path.exists( self.staircase_file_name ):
            with open(self.staircase_file_name) as f:
                self.staircases = pickle.load(f)
        else:
            # create staircases
            self.staircases={}
            self.staircases.update({'fix':
                        Quest.QuestObject(
                                tGuess = self.initial_value, 
                                tGuessSd = self.initial_value * 0.35, 
                                pThreshold = 0.83, 
                                beta = 3.5, 
                                delta = 0.01, 
                                gamma = 0.0, 
                                grain = 0.01, 
                                range = None 
                                ) 
                            })

    
    def prepare_trials(self):
        """docstring for prepare_trials(self):"""
        
        # create random m-sequence for the 5 trial types of length (5^3)-1 = 124. I then add the first trial type to the end of the array, so that all trial types have even occurences
        from psychopy.contrib import mseq
        self.tasks = np.array(['fix_no_stim','no_color_no_speed','yes_color_no_speed','no_color_yes_speed','yes_color_yes_speed'])
        self.trial_array = np.hstack([[0],mseq.mseq(5,3,1,np.random.randint(200))]) # base (number of trial types), power (sequence length is base^power-1), shift (to shift last values of sequence to first), random sequence out of the 200 possibilities
            
        self.phase_durations = np.array([
            -0.001, # instruct time
            -0.001, # wait for t at beginnning of every trial
            self.standard_parameters['TR'] * self.standard_parameters['mapper_stim_in_TR'],   #stimulation time
            self.standard_parameters['TR'] * self.standard_parameters['mapper_ITI_in_TR'] ]) # ITI time

        # stimuli
        self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=12.5, pos = np.array((0.0,0.0)), color = (0,0,0), maskParams = {'fringeWidth':0.4})
        self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=17.5, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
        self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=9.0, pos = np.array((0.0,0.0)), color = (0,0,0), opacity = 1.0, maskParams = {'fringeWidth':0.4})

        screen_width, screen_height = self.screen_pix_size
        
        ecc_mask = filters.makeMask(matrixSize = 2048, shape='raisedCosine', radius=self.standard_parameters['stim_size'] * self.screen_pix_size[1] / self.screen_pix_size[0], center=(0.0, 0.0), range=[1, -1], fringeWidth=0.1 )
        self.mask_stim = visual.PatchStim(self.screen, mask=ecc_mask,tex=None, size=(self.screen_pix_size[0], self.screen_pix_size[0]), pos = np.array((0.0,0.0)), color = self.screen.background_color) # 
    
        # this will be roughly 4 * 124 = 496, which is 8:15 minutes
        self.exp_duration = np.sum(self.phase_durations) * len(self.trial_array)

    def close(self):
        super(MapperSession, self).close()
        with open(self.staircase_file_name, 'w') as f:
            pickle.dump(self.staircases, f)
        print 'Fix staircase mean {}, standard deviation {}'.format(self.staircases['fix'].mean(), self.staircases['fix'].sd())
        
    
    def run(self):
        """docstring for fname"""
        # cycle through trials
        for i in range(len(self.trial_array)):
            # prepare the parameters of the following trial based on the shuffled trial array
            this_trial_parameters = self.standard_parameters.copy()
            this_trial_parameters['task'] = self.trial_array[i]

            these_phase_durations = self.phase_durations.copy()
            this_trial = MapperTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
            
            # run the prepared trial
            this_trial.run(ID = i)
            if self.stopped == True:
                break
        self.close()
    

