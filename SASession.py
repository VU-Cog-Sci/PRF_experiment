from __future__ import division
from psychopy import visual, core, misc, event
import numpy as np
# from IPython import embed as shell
from math import *

import os, sys, time, pickle
import pygame
from pygame.locals import *
import copy
# from pygame import mixer, time

#import Quest

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

from Session import *
from SATrial import *
from constants import *


try:
    import appnope
    appnope.nope()
except:
    print 'APPNOPE NOT ACTIVE!'

class SASession(EyelinkSession):
    def __init__(self, subject_initials, index_number,scanner, tracker_on,fix_sp):
        super(SASession, self).__init__( subject_initials, index_number)
		
        self.background_color = (np.array(BGC)/255*2)-1
        self.stim_color = (np.array(FGC)/255*2)-1
		
        if fix_sp == 'y':
            standard_parameters['sp_path_amplitude'] = 0

        screen = self.create_screen( size = DISPSIZE, full_screen =full_screen, physical_screen_distance = SCREENDIST, 
            background_color = self.background_color, physical_screen_size = SCREENSIZE, wait_blanking = True, screen_nr = 1 )
        event.Mouse(visible=False, win=screen)

        # define the effective screen dimensions for stimulus presentation
        self.ywidth = (1-standard_parameters['sp_path_elevation'])*DISPSIZE[1]*2
		
        self.create_output_file_name()
        if tracker_on:
            
            # how many points do we want:
            n_points = 9

			# order should be with 5 points: center-up-down-left-right
			# order should be with 9 points: center-up-down-left-right-leftup-rightup-leftdown-rightdown 
			# order should be with 13: center-up-down-left-right-leftup-rightup-leftdown-rightdown-midleftmidup-midrightmidup-midleftmiddown-midrightmiddown
			# so always: up->down or left->right
            # creat tracker
            self.create_tracker(auto_trigger_calibration = 0, calibration_type = 'HV%d'%n_points)
            # set the background and foreground to what we want:
            # self.tracker.target_foreground_color(0,0,0)
            # self.tracker.target_background_color(255,255,255)

            # create the calibration targets:
            # note: 0,0 is the upper left corner of the screen

            x_ratio_covered = standard_parameters['eyetracking_amplitude']/(DISPSIZE[0]/self.pixels_per_degree)
            x_edge = (1-x_ratio_covered)*DISPSIZE[0]/2

            # max y will be (y_portion-1)/y_portion of screen height, and min y 1/y_portion
            y_portion = 5
			
            # set calibration targets
            cal_center_x = DISPSIZE[0]/2
            cal_right_x = DISPSIZE[0]-x_edge
            cal_left_x = x_edge
            cal_center_y = self.ywidth/2# self.ymid
            cal_up_y = self.ywidth/y_portion
            cal_down_y = self.ywidth/y_portion*(y_portion-1)
            
            cal_center = [cal_center_x,cal_center_y]
            cal_left = [cal_left_x,cal_center_y]
            cal_right = [cal_right_x,cal_center_y]
            cal_up = [cal_center_x,cal_up_y]
            cal_down = [cal_center_x,cal_down_y]
            cal_leftup = [cal_left_x,cal_up_y]
            cal_rightup = [cal_right_x,cal_up_y]
            cal_leftdown = [cal_left_x,cal_down_y]
            cal_rightdown = [cal_right_x,cal_down_y]			
            
            # set validation targets			
            val_center_x = DISPSIZE[0]/2
            val_right_x = DISPSIZE[0]-(x_edge*2)
            val_left_x = x_edge*2
            val_center_y = self.ywidth/2
            val_up_y = self.ywidth/y_portion*2
            val_down_y =  self.ywidth-self.ywidth/y_portion*2	
            
            val_center = [val_center_x,val_center_y]
            val_left = [val_left_x,val_center_y]
            val_right = [val_right_x,val_center_y]
            val_up = [val_center_x,val_up_y]
            val_down = [val_center_x,val_down_y]
            val_leftup = [val_left_x,val_up_y]
            val_rightup = [val_right_x,val_up_y]
            val_leftdown = [val_left_x,val_down_y]
            val_rightdown = [val_right_x,val_down_y]	
            
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
        

        self.scanner = scanner
        # trials can be set up independently of the staircases that support their parameters
        self.prepare_trials()
        # self.prepare_sounds()

    # def prepare_sounds(self):
    #     for ut in np.unique(self.task_instructions):
    #         self.read_sound_file('sounds/%s.wav'%ut.lower())
            
    def prepare_trials(self):
        """docstring for prepare_trials(self):"""

        self.standard_parameters = standard_parameters

        # shell()
        x_test_positions = np.linspace(-self.standard_parameters['target_max_ecc'], self.standard_parameters['target_max_ecc'], self.standard_parameters['n_targets'])
        # pop the 0 position
        # x_test_positions = np.delete(x_test_positions,self.standard_parameters['n_targets']/2)

        # double x positions, to add above and below positions
        x_test_positions_rep = np.tile(x_test_positions,2)
        y_test_positions = np.concatenate((-1 * np.ones(x_test_positions.shape[0]), np.ones(x_test_positions.shape[0])))

        # double the whole thing so we can add eye dir 
        x_test_positions_tiled = np.tile(x_test_positions_rep, 2)
        y_test_positions_tiled = np.tile(y_test_positions, 2)

        # now add eye dir
        eye_dir = np.concatenate([np.ones(int(x_test_positions_tiled.shape[0]/2)),np.zeros(int(x_test_positions_tiled.shape[0]/2))])

        # now duplicate the whole thing for multiple trials
        x_test_positions_tiled = np.tile(x_test_positions_tiled,self.standard_parameters['n_target_reps'])
        y_test_positions_tiled = np.tile(y_test_positions_tiled,self.standard_parameters['n_target_reps'])
        eye_dir = np.tile(eye_dir,self.standard_parameters['n_target_reps'])

        self.trial_order = np.arange(eye_dir.shape[0])

        # shuffle the trial order untill the first eye dir is 0:
        while True:
            
            # now let's create a random trial order 
            np.random.shuffle(self.trial_order)

            # and apply
            x_test_positions_tiled_shuffled = x_test_positions_tiled[self.trial_order]
            y_test_positions_tiled_shuffled = y_test_positions_tiled[self.trial_order]
            eye_dir_shuffled = eye_dir[self.trial_order]

            # now check if first eye dir is 0:
            if eye_dir_shuffled[0] == 0:
                break
                
        ITIs = np.zeros(len(self.trial_order))#*self.standard_parameters['minimal_iti']

        if self.standard_parameters['n_targets'] == 3:
            # and here's the distribution of ITIs:
            unique_ITIs = {
            0: 6*self.standard_parameters['n_target_reps'],
            1: 3*self.standard_parameters['n_target_reps'],
            2: 2*self.standard_parameters['n_target_reps'],
            3: 1*self.standard_parameters['n_target_reps'],
            }

        if self.standard_parameters['n_targets'] == 5:
            # and here's the distribution of ITIs:
            unique_ITIs = {
            1: 9*self.standard_parameters['n_target_reps'],
            2: 5*self.standard_parameters['n_target_reps'],
            3: 3*self.standard_parameters['n_target_reps'],
            4: 2*self.standard_parameters['n_target_reps'],
            5: 1*self.standard_parameters['n_target_reps'],
            }

        if self.standard_parameters['n_targets'] == 8:
            # and here's the distribution of ITIs:
            unique_ITIs = {
            0: 13*self.standard_parameters['n_target_reps'],
            1: 9*self.standard_parameters['n_target_reps'],
            2: 6*self.standard_parameters['n_target_reps'],
            3: 3*self.standard_parameters['n_target_reps'],
            4: 1*self.standard_parameters['n_target_reps'],
            }

        # randomly distribute ITI's over the trial combinations:
        ITI_order = np.arange(len(ITIs))
        np.random.shuffle(ITI_order)        
        k = 0
        for this_ITI in unique_ITIs.keys():
            ITIs[ITI_order[k:k+unique_ITIs[this_ITI]]] = this_ITI
            k += unique_ITIs[this_ITI]

        # and add or subtract 1 when a switch in eye dir is required:
        n_switches = 0
        for ti, this_eye_dir in enumerate(eye_dir_shuffled):
            ITI_cumsum = np.sum(ITIs[:ti])
            current_direction = ITI_cumsum%2
            if current_direction != this_eye_dir: # this cannot happen on first trial as eye dir on first trial was set to 0 (and ITI cumsum is always 0 there)
                ITIs[ti-1] += [-1,1][n_switches%2] # change ITI from previous trial, as this affects current flash direction
                n_switches += 1

        ITIs += self.standard_parameters['minimal_iti']

        # the total number of TRs can now be one less or more depending on whether there were uneven or even n_switches
        # thus add 1 TR when n_switches are uneven:
        padd_TR = n_switches%2

        print 'run will last %d TRs'%(np.sum(ITIs)+padd_TR)

        # now add the first and last empty trials:
        x_test_positions_tiled_shuffled = np.hstack([-1e3,x_test_positions_tiled_shuffled,-1e3]) #-1e3 means off the screen)
        y_test_positions_tiled_shuffled = np.hstack([-1e3,y_test_positions_tiled_shuffled,-1e3]) #-1e3 means off the screen)
        ITIs = np.hstack([self.standard_parameters['warming_up_n_TRs'],ITIs,self.standard_parameters['warming_up_n_TRs']+padd_TR])
        eye_dir_shuffled = np.hstack([0,eye_dir_shuffled,0])


        # define all durations per trial
        self.phase_durations = np.array([[
            -0.0001, # wait for t on first trial if in scanner
            self.standard_parameters['fp_dim_delay'],
            ITIs[t] * self.standard_parameters['TR'] - self.standard_parameters['fp_dim_delay'], # ITI in TRs
            ] for t in range(len(ITIs))] )   


        # fixation point
        # self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=12.5, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
        # self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=22.5, pos = np.array((0.0,0.0)), color = (0.0,0.0,0.0), maskParams = {'fringeWidth':0.4})
        # self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=9.0, pos = np.array((0.0,0.0)), color = (1.0,1.0,1.0), opacity = 1.0, maskParams = {'fringeWidth':0.4})

        # self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=35, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
        # self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=45, pos = np.array((0.0,0.0)), color = (0.0,0.0,0.0), maskParams = {'fringeWidth':0.4})
        # self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=50, pos = np.array((0.0,0.0)), color = (1.0,1.0,1.0), opacity = 1.0, maskParams = {'fringeWidth':0.4})

        self.fixation_left = visual.PatchStim(self.screen,
            mask='raisedCos',
            tex=None, 
            size=self.standard_parameters['sp_target_size']*self.pixels_per_degree, 
            pos = np.array((0.0,0.0)), 
            color = self.stim_color, 
            opacity = 1.0, 
            maskParams = {'fringeWidth':0.4})

        self.fixation_right = visual.PatchStim(self.screen,
            mask='raisedCos',
            tex=None, 
            size=self.standard_parameters['sp_target_size']*self.pixels_per_degree, 
            pos = np.array((0.0,0.0)), 
            color = self.stim_color, 
            opacity = 1.0, 
            maskParams = {'fringeWidth':0.4})

        self.fixation_center = visual.PatchStim(self.screen,
			mask='raisedCos',
			tex=None, 
			size=self.standard_parameters['sp_target_size']*self.pixels_per_degree, 
			pos = np.array((0.0,0.0)), 
			color = self.stim_color, 
			opacity = 1.0, 
			maskParams = {'fringeWidth':0.4})

        self.saccade_target = visual.PatchStim(self.screen,
            mask='raisedCos',
            tex=None, 
            size=self.standard_parameters['sp_target_size']*self.pixels_per_degree, 
            pos = np.array((0.0,0.0)), 
            color = self.stim_color, 
            opacity = 1.0, 
            maskParams = {'fringeWidth':0.4})

        # now define the test stim sizes dependent on screen size available:
        if self.standard_parameters['test_stim_height'] == 0:
            self.standard_parameters['test_stim_height'] = self.ywidth/4/self.pixels_per_degree
        if self.standard_parameters['test_stim_y_offset'] == 0:
            self.standard_parameters['test_stim_y_offset'] = self.ywidth/4/self.pixels_per_degree
        self.test_stim = visual.Rect(self.screen, 
                            width = self.standard_parameters['test_stim_width']*self.pixels_per_degree,  
                            height = self.standard_parameters['test_stim_height']*self.pixels_per_degree, 
                            lineColor = self.stim_color,
                            fillColor = self.stim_color)

        self.start_time = 0.0
        # self.cumulative_phase_durations = np.cumsum(np.r_[0,self.phase_durations[self.trial_order,1:].ravel()][:-1]).reshape((self.phase_durations.shape[0], -1))
        self.cumulative_phase_durations = np.cumsum(np.r_[0,self.phase_durations[:,1:].ravel()][:-1]).reshape((self.phase_durations.shape[0], -1))

        self.all_trials = []
        for i in range(len(eye_dir_shuffled)):#self.trial_order:

            this_trial_parameters={
                                    # trial varying params:
                                    'x_pos': x_test_positions_tiled_shuffled[i],
                                    'y_order': y_test_positions_tiled_shuffled[i],
                                    'eye_dir': eye_dir_shuffled[i],
                                    'ITI': ITIs[i], # this should not be _shuffled
                                    'answer': self.standard_parameters['default_answer'],
                                    'fp_dim_dur':self.standard_parameters['fp_dim_dur'],

                                    # these params don't vary over trials:
                                    'TR': self.standard_parameters['TR'],
                                    'sp_path_amplitude':self.standard_parameters['sp_path_amplitude'],
                                    'test_stim_y_offset':self.standard_parameters['test_stim_y_offset'],
                                    'sp_path_elevation':self.standard_parameters['sp_path_elevation'],
                                    'sp_path_temporal_frequency':self.standard_parameters['sp_path_temporal_frequency'],
                                    'warming_up_n_TRs':self.standard_parameters['warming_up_n_TRs']
                                    }

            self.all_trials.append(SATrial(this_trial_parameters, phase_durations = self.phase_durations[i], session = self, screen = self.screen, tracker = self.tracker))

    
    def close(self):
        super(SASession, self).close()        
    
    def run(self):
        """docstring for fname"""
        # cycle through trials
        for i, trial in enumerate(self.all_trials):
            # run the prepared trial
            trial.run(ID = i)
            if self.stopped == True:
                break
        self.close()
    

