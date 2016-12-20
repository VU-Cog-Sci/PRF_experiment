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
from constants import *
from Staircase import YesNoStaircase

import appnope
appnope.nope()

class MapperSession(EyelinkSession):
    def __init__(self, subject_initials, index_number, scanner, tracker_on):
        super(MapperSession, self).__init__( subject_initials, index_number)
        
        self.background_color = (np.array(BGC)/255*2)-1

        screen = self.create_screen( size = DISPSIZE, full_screen =full_screen, physical_screen_distance = SCREENDIST, 
            background_color = self.background_color, physical_screen_size = SCREENSIZE, wait_blanking = True, screen_nr = 1 )
        # screen = self.create_screen( size = screen_res, full_screen =0, physical_screen_distance = 159.0, background_color = background_color, physical_screen_size = (70, 40) )
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
        
        # and here's the distribution of ITIs:
        unique_ITIs = {
        2: 33,
        3: 22,
        4: 10,
        5: 4,
        6: 2,
        }

        n_trials = sum(unique_ITIs.values())
        ITIs = np.zeros(n_trials)

        # randomly distribute ITI's
        ITI_order = np.arange(len(ITIs))
        np.random.shuffle(ITI_order)        
        k = 0
        for this_ITI in unique_ITIs.keys():
            ITIs[ITI_order[k:k+unique_ITIs[this_ITI]]] = this_ITI
            k += unique_ITIs[this_ITI]

        self.ITIs = np.hstack([self.standard_parameters['warming_up_n_TRs'],ITIs,self.standard_parameters['warming_up_n_TRs']])
        self.draw_stim = np.hstack([0,np.ones_like(ITIs),0])

        self.phase_durations = np.array([[
            -0.001, # instruct time
            -0.001, # wait for t at beginnning of every trial
            self.standard_parameters['TR'] * self.standard_parameters['mapper_stim_in_TR'],   #stimulation time
            self.standard_parameters['TR'] * ITI] for ITI in self.ITIs]) # ITI time

        # fixation point
        self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=40, pos = np.array((self.standard_parameters['x_offset'],0.0)), color = self.background_color, maskParams = {'fringeWidth':0.4})
        self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=22, pos = np.array((self.standard_parameters['x_offset'],0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
        self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=17, pos = np.array((self.standard_parameters['x_offset'],0.0)), color = self.background_color, opacity = 1.0, maskParams = {'fringeWidth':0.4})
        
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
    
        # this will be roughly 4 * 124 = 496, which is 8:15 minutes
        # self.exp_duration = np.sum(self.phase_durations) * len(self.trial_array)

    def close(self):
        super(MapperSession, self).close()
        with open(self.staircase_file_name, 'w') as f:
            pickle.dump(self.staircases, f)
        print 'Fix staircase mean {}, standard deviation {}'.format(self.staircases['fix'].mean(), self.staircases['fix'].sd())
        
    
    def run(self):
        """docstring for fname"""
        # cycle through trials
        for i in range(len(self.ITIs)):
            # prepare the parameters of the following trial based on the shuffled trial array
            this_trial_parameters = self.standard_parameters.copy()
            this_trial_parameters['draw_stim'] = self.draw_stim[i]

            these_phase_durations = self.phase_durations[i]
            this_trial = MapperTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
            
            # run the prepared trial
            this_trial.run(ID = i)
            if self.stopped == True:
                break
        self.close()
    

