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
from constants import *
from Staircase import YesNoStaircase

import appnope
appnope.nope()

class PRFSession(EyelinkSession):
    def __init__(self, subject_initials, index_number,scanner, tracker_on,task_type):
        super(PRFSession, self).__init__( subject_initials, index_number)

        self.background_color = (np.array(BGC)/255*2)-1
        self.task = task_type

        screen = self.create_screen( size = DISPSIZE, full_screen =full_screen, physical_screen_distance = SCREENDIST, 
            background_color = self.background_color, physical_screen_size = SCREENSIZE, wait_blanking = True, screen_nr = 1 )
        # screen = self.create_screen( size = screen_res, full_screen =0, physical_screen_distance = 159.0, background_color = background_color, physical_screen_size = (70, 40) )
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
        self.nr_staircases_ecc = 4
        self.prepare_staircases(self.nr_staircases_ecc )
        # self.prepare_sounds()

    def prepare_staircases(self,nr_staircases_ecc):


        # Color,Fix
        self.initial_values = [2.5,2.5]

        self.staircase_file_name = os.path.join(os.path.split(self.output_file)[0], self.subject_initials + '_prf_control_quest.pickle')
        if os.path.exists( self.staircase_file_name ):
            with open(self.staircase_file_name) as f:
                self.staircases = pickle.load(f)
        else:
            # create staircases
            self.staircases = {}
            for i, t in enumerate(['fix','bar']):
                for j in range(nr_staircases_ecc):
                    self.staircases.update({t + '_%i'%j:
                                Quest.QuestObject(
                                        tGuess = self.initial_values[i],  
                                        tGuessSd = self.initial_values[i]*0.5, 
                                        pThreshold = 0.83, 
                                        beta = 3.5, 
                                        delta = 0.05, 
                                        gamma = 0.0, 
                                        grain = 0.01, 
                                        range = None 
                                        ) 
                                    })
        # now simply pick one of the staircases needed for this condition
        # self.staircase = self.staircases[self.task]
    
    def prepare_trials(self):
        """docstring for prepare_trials(self):"""

        self.directions = np.linspace(0, 2.0 * pi, 8, endpoint = False)
        self.standard_parameters = standard_parameters


        # self.tasks = np.array(['bar', 'fix'])

        # orientations, bar moves towards:
        # 0: S      3: NW   6: E
        # 1: SW     4: N    7: SE
        # 2: W      5: NE

        if self.standard_parameters['practice']:
            self.stim_bool = [1,1,1,1,1,1,1,1,1,1,1]
            self.direction_indices = np.array([6,4,2,0,6,2,4,2,0,6,4])
        else:
            # nostim-top-left-bottom-right-nostim-top-left-bottom-right-nostim
            # self.stim_bool = [0,1,1,1,1,0,1,1,1,1,0]
            # self.direction_indices = np.array([0,4,2,0,6,0,4,2,0,6,0])
            # nostim-bottom-left-nostim-right-top-nostim
            self.stim_bool = [0,1,1,0,1,1,0]
            self.direction_indices = np.array([0,0,2,0,6,4,0])

        self.trial_array = np.array([[self.direction_indices[i], self.stim_bool[i]] for i in range(len(self.stim_bool))])

        # get the RG/BY ratios
        text_file_name = "data/%s_color_ratios.txt"%self.subject_initials
        assert os.path.isfile(text_file_name), 'NO COLOR RATIO TEXT FILE PRESENT!!!!!!!!'
        text_file = open(text_file_name, "r")
        RG_BY_ratio = float(text_file.readline().split('ratio: ')[-1][:-1])
        text_file.close()
        if np.isnan(RG_BY_ratio):
            RG_BY_ratio = 1
        if RG_BY_ratio > 1:
            self.standard_parameters['RG_color'] = 1
            self.standard_parameters['BY_color'] = 1/RG_BY_ratio
        else:
            self.standard_parameters['BY_color'] = 1
            self.standard_parameters['RG_color'] = 1/RG_BY_ratio

        self.phase_durations = np.array([
            -0.0001, # instruct time
            -0.0001, # wait for scan pulse
            self.standard_parameters['PRF_ITI_in_TR'] * self.standard_parameters['TR'] ])# for stim_dur in self.stim_durations])    # ITI

        # fixation point
        self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=40, pos = np.array((0.0,0.0)), color = self.background_color, maskParams = {'fringeWidth':0.4})
        self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=22, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
        self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=17, pos = np.array((0.0,0.0)), color = self.background_color, opacity = 1.0, maskParams = {'fringeWidth':0.4})
        
        # mask
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
        self.mask_stim = visual.PatchStim(self.screen, mask=mask,tex=None, size=[self.screen_pix_size[0],self.screen_pix_size[1]], pos = np.array((0.0,0.0)), color = self.screen.background_color) # 
    
    def close(self):
        super(PRFSession, self).close()
        with open(self.staircase_file_name, 'w') as f:
            pickle.dump(self.staircases, f)
        for s in self.staircases.keys():
            print 'Staircase {}, mean {}, standard deviation {}'.format(s, self.staircases[s].mean(), self.staircases[s].sd())
        
    
    def run(self):
        """docstring for fname"""
        # cycle through trials
        for i in range(len(self.trial_array)):
            # prepare the parameters of the following trial based on the shuffled trial array
            this_trial_parameters = self.standard_parameters.copy()
            this_trial_parameters['orientation'] = self.directions[self.trial_array[i,0]]
            this_trial_parameters['stim_bool'] = self.trial_array[i,1]
            this_trial_parameters['task'] = {'fix':0,'bar':1}[self.task] 

            # these_phase_durations = self.phase_durations.copy()
            these_phase_durations = self.phase_durations


            this_trial = PRFTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
            
            # run the prepared trial
            this_trial.run(ID = i)
            if self.stopped == True:
                break
        self.close()
    

