from __future__ import division
from psychopy import visual, core, misc, event, data
import numpy as np
from IPython import embed as shell
from math import *
import copy

import os, sys, time, pickle
import pygame
from pygame.locals import *
# from pygame import mixer, time

# import Quest

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

from Session import *
from RevLTrial import *
from constants import *
# from Staircase import YesNoStaircase

import appnope
appnope.nope()

class RevLSession(EyelinkSession):
    def __init__(self, subject_initials, index_number, tracker_on):
        super(RevLSession, self).__init__( subject_initials, index_number)
        
        self.background_color = (np.array(BGC)/255*2)-1

        screen = self.create_screen( size = DISPSIZE, full_screen =full_screen, physical_screen_distance = SCREENDIST, 
            background_color = self.background_color, physical_screen_size = SCREENSIZE, wait_blanking = True, screen_nr = 1 )
        # screen = self.create_screen( size = screen_res, full_screen =0, physical_screen_distance = 159.0, background_color = background_color, physical_screen_size = (70, 40) )
        event.Mouse(visible=False, win=screen)

        self.standard_parameters = standard_parameters
        self.response_button_signs = response_button_signs

        self.create_output_file_name()
        if tracker_on:
            # self.create_tracker(auto_trigger_calibration = 1, calibration_type = 'HV9')
            # if self.tracker_on:
            #     self.tracker_setup()
           # how many points do we want:
            n_points = 9

            # order should be with 5 points: center-up-down-left-right
            # order should be with 9 points: center-up-down-left-right-leftup-rightup-leftdown-rightdown 
            # order should be with 13: center-up-down-left-right-leftup-rightup-leftdown-rightdown-midleftmidup-midrightmidup-midleftmiddown-midrightmiddown
            # so always: up->down or left->right

            # creat tracker
            self.create_tracker(auto_trigger_calibration = 0, calibration_type = 'HV%d'%n_points)

            # it is setup to do a 9-point circular calibration, at reduced ecc

            # create 4 x levels:
            width = standard_parameters['eyelink_calib_size'] * DISPSIZE[1]
            x_start = (DISPSIZE[0]-width)/2
            x_end = DISPSIZE[0]-(DISPSIZE[0]-width)/2
            x_range = np.linspace(x_start,x_end,5) + standard_parameters['x_offset']  
            y_start = (DISPSIZE[1]-width)/2
            y_end = DISPSIZE[1]-(DISPSIZE[1]-width)/2
            y_range = np.linspace(y_start,y_end,5) 

            # set calibration targets    
            cal_center = [x_range[2],y_range[2]]
            cal_left = [x_range[0],y_range[2]]
            cal_right = [x_range[4],y_range[2]]
            cal_up = [x_range[2],y_range[0]]
            cal_down = [x_range[2],y_range[4]]
            cal_leftup = [x_range[1],y_range[1]]
            cal_rightup = [x_range[3],y_range[1]]
            cal_leftdown = [x_range[1],y_range[3]]
            cal_rightdown = [x_range[3],y_range[3]]            
            
            # create 4 x levels:
            width = standard_parameters['eyelink_calib_size']*0.75 * DISPSIZE[1]
            x_start = (DISPSIZE[0]-width)/2
            x_end = DISPSIZE[0]-(DISPSIZE[0]-width)/2
            x_range = np.linspace(x_start,x_end,5) + standard_parameters['x_offset']  
            y_start = (DISPSIZE[1]-width)/2
            y_end = DISPSIZE[1]-(DISPSIZE[1]-width)/2
            y_range = np.linspace(y_start,y_end,5) 

            # set calibration targets    
            val_center = [x_range[2],y_range[2]]
            val_left = [x_range[0],y_range[2]]
            val_right = [x_range[4],y_range[2]]
            val_up = [x_range[2],y_range[0]]
            val_down = [x_range[2],y_range[4]]
            val_leftup = [x_range[1],y_range[1]]
            val_rightup = [x_range[3],y_range[1]]
            val_leftdown = [x_range[1],y_range[3]]
            val_rightdown = [x_range[3],y_range[3]]   

            # get them in the right order
            if n_points == 5:
                cal_xs = np.round([cal_center[0],cal_up[0],cal_down[0],cal_left[0],cal_right[0]])
                cal_ys = np.round([cal_center[1],cal_up[1],cal_down[1],cal_left[1],cal_right[1]])
                val_xs = np.round([val_center[0],val_up[0],val_down[0],val_left[0],val_right[0]])
                val_ys = np.round([val_center[1],val_up[1],val_down[1],val_left[1],val_right[1]])
            elif n_points == 9:
                cal_xs = np.round([cal_center[0],cal_up[0],cal_down[0],cal_left[0],cal_right[0],cal_leftup[0],cal_rightup[0],cal_leftdown[0],cal_rightdown[0]])
                cal_ys = np.round([cal_center[1],cal_up[1],cal_down[1],cal_left[1],cal_right[1],cal_leftup[1],cal_rightup[1],cal_leftdown[1],cal_rightdown[1]])         
                val_xs = np.round([val_center[0],val_up[0],val_down[0],val_left[0],val_right[0],val_leftup[0],val_rightup[0],val_leftdown[0],val_rightdown[0]])
                val_ys = np.round([val_center[1],val_up[1],val_down[1],val_left[1],val_right[1],val_leftup[1],val_rightup[1],val_leftdown[1],val_rightdown[1]])                     
            #xs = np.round(np.linspace(x_edge,DISPSIZE[0]-x_edge,n_points))
            #ys = np.round([self.ywidth/3*[1,2][pi%2] for pi in range(n_points)])

            # put the points in format that eyelink wants them, which is
            # calibration_targets / validation_targets: 'x1,y1 x2,y2 ... xz,yz'
            calibration_targets = ' '.join(['%d,%d'%(cal_xs[pi],cal_ys[pi]) for pi in range(n_points)])
            # just copy calibration targets as validation for now:
            #validation_targets = calibration_targets
            validation_targets = ' '.join(['%d,%d'%(val_xs[pi],val_ys[pi]) for pi in range(n_points)])

            # point_indices: '0, 1, ... n'
            point_indices = ', '.join(['%d'%pi for pi in range(n_points)])

            # and send these targets to the custom calibration function:
            self.custom_calibration(calibration_targets=calibration_targets,
                validation_targets=validation_targets,point_indices=point_indices,
                n_points=n_points,randomize_order=True,repeat_first_target=True,)
            # reapply settings:
            self.tracker_setup()
        else:
            self.create_tracker(tracker_on = False)
        
        # trials can be set up independently of the staircases that support their parameters
        self.prepare_stims()
        self.prepare_trials()

        self.exp_start_time = 0.0

    def prepare_stims(self):

        """docstring for prepare_stims(self):"""
        self.CW_stim = visual.GratingStim(self.screen, 
                tex='sin', mask='raisedCos', pos=(0.0, 0.0), 
                size=self.standard_parameters['stim_size'], 
                sf=self.standard_parameters['stim_spatial_frequency'], 
                ori=45.0, texRes=128, color=(1.0, 1.0, 1.0),
                colorSpace='rgb', contrast=0.5, opacity=1.0,
                maskParams={'fringeWidth':0.2})
        self.CCW_stim = visual.GratingStim(self.screen, 
                tex='sin', mask='raisedCos', pos=(0.0, 0.0), 
                size=self.standard_parameters['stim_size'], 
                sf=self.standard_parameters['stim_spatial_frequency'], 
                ori=-45.0, texRes=128, color=(1.0, 1.0, 1.0),
                colorSpace='rgb', contrast=0.5, opacity=1.0,
                maskParams={'fringeWidth':0.2})

        # fixation point
        self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, 
            size=40, pos = np.array((0.0,0.0)), 
            color = self.background_color, maskParams = {'fringeWidth':0.4})
        self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, 
            size=22, pos = np.array((0.0,0.0)), 
            color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
        self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, 
            size=17, pos = np.array((0.0,0.0)), 
            color = self.background_color, opacity = 1.0, maskParams = {'fringeWidth':0.4})


    def prepare_trials(self):
        """docstring for prepare_trials(self):"""
        
        # create trials
        self.trials = []
        self.trial_counter = 0

        self.phase_durations = [
            -0.001,                                         # instruct time
            self.standard_parameters['ITI_minimum']/2.0,    # ITI
            self.standard_parameters['stim_dur'],           # stimulus time
            self.standard_parameters['ITI_minimum']/2.0,        # ITI 
            ]

        this_reward_contingency = np.random.choice([0,1], 1)
        block_durations = np.random.randint(self.standard_parameters['block_duration_minimum'], \
            self.standard_parameters['block_duration_minimum'] + self.standard_parameters['block_duration_range'], 15)
                            
        block_transitions = np.cumsum(block_durations)

        tol_range = np.array([1.0 - self.standard_parameters['total_ITI_tolerance'], \
                                1.0 + self.standard_parameters['total_ITI_tolerance']])
        iti_sum_range = tol_range * self.standard_parameters['total_nr_trials'] * self.standard_parameters['ITI_mean']

        ITIs = np.random.exponential(self.standard_parameters['ITI_mean'], self.standard_parameters['total_nr_trials'])
        while ITIs.sum() < iti_sum_range[0] or ITIs.sum() > iti_sum_range[1]:
            ITIs = np.random.exponential(self.standard_parameters['ITI_mean'], self.standard_parameters['total_nr_trials'])

        for x in range(self.standard_parameters['total_nr_trials']):
            # switch reward contingency on block transition
            if x in block_transitions:
                this_reward_contingency = 1 - this_reward_contingency

            params = self.standard_parameters


            if this_reward_contingency == 0:
                rpCW = self.standard_parameters['high_reward_probability']
                rpCCW = 1-self.standard_parameters['high_reward_probability']
                HR_orientation = 1
            elif this_reward_contingency == 1:
                rpCW = 1-self.standard_parameters['high_reward_probability']
                rpCCW = self.standard_parameters['high_reward_probability'] 
                HR_orientation = -1

            feedback_if_HR_chosen = np.random.binomial(1, self.standard_parameters['high_reward_probability'])
            position_CW = np.random.choice([-1,1], 1)

            this_ITI = ITIs[x]

            params.update(
                {   
                'reward_probability_CW': rpCW, 
                'reward_probability_CCW': rpCCW,
                'position_CW': position_CW * self.standard_parameters['stim_x_offset'],
                'position_CCW': -position_CW * self.standard_parameters['stim_x_offset'],
                'HR_orientation': HR_orientation,
                'HR_location': HR_orientation * position_CW,
                'feedback_if_HR_chosen': feedback_if_HR_chosen,
                'eye_movement_error': 0,
                'answer': 0,
                'correct': 0,
                'rt': 0,
                'reward': 0,
                'ITI': this_ITI
                }
            )

            these_phase_durations = copy.copy(self.phase_durations)
            these_phase_durations[1] = this_ITI + self.standard_parameters['ITI_minimum']/2.0
            this_trial = RevLTrial(params, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
            
            self.trials.append(this_trial)
            self.trial_counter += 1
        self.trials[0].phase_durations[1] = 12.0
        self.trials[-1].phase_durations[-1] = 12.0
        print 'total experiment duration: %3.3f' % np.array([np.array(tr.phase_durations).sum() for tr in self.trials]).sum()

    def close(self):
        super(RevLSession, self).close()        
    
    def run(self):
        """docstring for fname"""
        # cycle through trials
        for i in range(len(self.trials)):
            # run the prepared trial
            self.trials[i].run(ID = i)
            if self.stopped == True:
                break
        self.close()
    

