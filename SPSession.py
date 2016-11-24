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
from SPTrial import *
from constants import *


try:
    import appnope
    appnope.nope()
except:
    print 'APPNOPE NOT ACTIVE!'

class SPSession(EyelinkSession):
    def __init__(self, subject_initials, index_number,scanner, tracker_on):
        super(SPSession, self).__init__( subject_initials, index_number)
		
        self.background_color = (np.array(BGC)/255*2)-1
        self.stim_color = (np.array(FGC)/255*2)-1
		
        screen = self.create_screen( size = DISPSIZE, full_screen =full_screen, physical_screen_distance = SCREENDIST, 
            background_color = self.background_color, physical_screen_size = SCREENSIZE, wait_blanking = False, screen_nr = 1 )
        event.Mouse(visible=False, win=screen)

        # define the effective screen dimensions for stimulus presentation
        self.ywidth = (1-standard_parameters['sp_path_elevation'])*DISPSIZE[1]*2

        self.create_output_file_name()
        if tracker_on:
            
            # how many points do we want:
            n_points = 5

            # creat tracker
            self.create_tracker(auto_trigger_calibration = 0, calibration_type = 'HV%d'%n_points)
            # set the background and foreground to what we want:
            # self.tracker.target_foreground_color(0,0,0)
            # self.tracker.target_background_color(255,255,255)

            # create the calibration targets:
            # note: 0,0 is the upper left corner of the screen
            x_ratio_covered = standard_parameters['sp_path_amplitude']/(DISPSIZE[0]/self.pixels_per_degree)
            x_edge = (1-x_ratio_covered)*DISPSIZE[0]/2*0.5
            xs = np.round(np.linspace(x_edge,DISPSIZE[0]-x_edge,n_points))
            ys = np.round([self.ywidth/3*[1,2][pi%2] for pi in range(n_points)])

            # put the points in format that eyelink wants them, which is
            # calibration_targets / validation_targets: 'x1,y1 x2,y2 ... xz,yz'
            calibration_targets = ' '.join(['%d,%d'%(xs[pi],ys[pi]) for pi in range(n_points)])
            # just copy calibration targets as validation for now:
            validation_targets = calibration_targets
            # point_indices: '0, 1, ... n'
            point_indices = ', '.join(['%d'%pi for pi in range(n_points)])

            # and send these targets to the custom calibration function:
            self.custom_calibration(calibration_targets=calibration_targets,
                validation_targets=validation_targets,point_indices=point_indices,
                n_points=n_points,randomize_order=False,repeat_first_target=False,)
            # reapply settings:
            self.tracker_setup()
        else:
            self.create_tracker(tracker_on = False)
        
        self.response_button_signs = response_button_signs

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

        # combining all 5 positions gives 5x5=25 possible location combinations
        x_test_positions = np.array(np.meshgrid(self.standard_parameters['test_stim_positions'], self.standard_parameters['test_stim_positions'])).T.reshape((-1,2))
        x1, x2 = x_test_positions[:,0], x_test_positions[:,1]

        # y position is above or below fp
        y_test_positions = np.concatenate((-1 * np.ones(x_test_positions.shape[0]), np.ones(x_test_positions.shape[0])))

        # tile them 4 times, so that we have 25*4=100 trials
        x_test_positions_tiled = np.array([np.tile(x1, 4), np.tile(x2, 4)]).T
        y_test_positions_tiled = np.tile(y_test_positions, 2)

        # ITI will be minimal ITI duration for first 50, and minimal ITI duration + 1 for last 50 trials:
        ITIs = np.concatenate([np.ones(x_test_positions_tiled.shape[0]/2)*self.standard_parameters['minimal_iti'], 
                               np.ones(x_test_positions_tiled.shape[0]/2)*self.standard_parameters['minimal_iti']+1])

        # add per-direction exponentially distributed random ITIs, 
        # while keeping the evenness of the ITIs the same (by only adding even intervals)
        for direction in [0,1]:
            direction_order = np.arange(direction * 50, (direction+1) * 50)
            np.random.shuffle(direction_order)
            # now approach exponential ITI distribution:
            ITIs[direction_order[:12]] += 2   # 12 trials
            ITIs[direction_order[12:18]] += 4 # 6 trials
            ITIs[direction_order[18:21]] += 6 #  trials
            ITIs[direction_order[21:22]] += 8 # 2 trials
                                              # 54 remaining
            # this should yield:
            # 2 TRs: 27 (0+2)
            # 3 TRs: 27 (0+3)
            # 4 TRs: 12 (2+2)
            # 5 TRs: 12 (2+3) 
            # 6 TRs: 6  (4+2)
            # 7 TRs: 6  (4+3)
            # 8 TRs: 3  (6+2)
            # 9 TRs: 3  (6+3)
            # 10 TRs: 1 (8+2)
            # 11 TRs: 1 (8+3)

        # If a trial_order_file exists, read the trial order from there, otherwise create it.
        # An identical trial_order between runs creates the opportunity to average runs if so desired
        import inspect
        exp_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        fn = os.path.join(exp_dir,'trial_order.npy')
        if os.path.isfile(fn):
            self.trial_order = np.load(fn)
            # set eye_dir according to the cumsums
            # sort ITIs
            ITIs_in_order = ITIs[self.trial_order]
            cum_ITIs = np.cumsum(ITIs_in_order)
            # trials to the right
            eye_dir = (cum_ITIs%2==0)
        else:
            # create random trial order as often such that everything is balanced
            balanced = False # probably unbalanced first time so let's just enter the loop
            while balanced == False:
                eye_dir_balanced = False; y_order_balanced = False

                # define new random trial order
                self.trial_order = np.arange(ITIs.shape[0])
                np.random.shuffle(self.trial_order)

                # sort ITIs
                ITIs_in_order = ITIs[self.trial_order]
                cum_ITIs = np.cumsum(ITIs_in_order)
                # trials to the right
                eye_dir = (cum_ITIs%2==0)
                right_trials = (eye_dir==1)
                if np.sum(right_trials)==50:
                    eye_dir_balanced = True
                # now from those right trials, half (25 out of 50) should have y_pos of 1
                y_positions_in_order = y_test_positions_tiled[self.trial_order]
                lower_first = (y_positions_in_order==-1)
                if (right_trials*lower_first).sum() == 25:
                    y_order_balanced = True
                # if this is the case, then also the left trials are balanced in their y-order
                balanced = eye_dir_balanced * y_order_balanced

            # save the self.trial_order
            np.save(fn,self.trial_order)
            # write protect it so it can only be deleted after specifically altering rights
            os.chmod(fn,0444)

        # define all durations per trial
        self.phase_durations = np.array([[
            -0.0001, # instruct time, skipped in all trials but the first (wait for t)
            ITI * self.standard_parameters['TR'], # smooth pursuit before stim
            self.standard_parameters['TR'], # smooth pursuit after stim 1
            self.standard_parameters['TR'] # smooth pursuit after stim 2
            ] for ITI in ITIs] )    
        
        # fixation point
        # self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=12.5, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
        # self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=22.5, pos = np.array((0.0,0.0)), color = (0.0,0.0,0.0), maskParams = {'fringeWidth':0.4})
        # self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=9.0, pos = np.array((0.0,0.0)), color = (1.0,1.0,1.0), opacity = 1.0, maskParams = {'fringeWidth':0.4})

        # self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=35, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
        # self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=45, pos = np.array((0.0,0.0)), color = (0.0,0.0,0.0), maskParams = {'fringeWidth':0.4})
        # self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=50, pos = np.array((0.0,0.0)), color = (1.0,1.0,1.0), opacity = 1.0, maskParams = {'fringeWidth':0.4})
        self.fixation = visual.PatchStim(self.screen,
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
        self.test_stim_1 = visual.Rect(self.screen, 
                            width = self.standard_parameters['test_stim_width']*self.pixels_per_degree,  
                            height = self.standard_parameters['test_stim_height']*self.pixels_per_degree, 
                            lineColor = self.stim_color,
                            fillColor = self.stim_color)

        self.test_stim_2 = visual.Rect(self.screen, 
                            width = self.standard_parameters['test_stim_width']*self.pixels_per_degree, 
                            height = self.standard_parameters['test_stim_height']*self.pixels_per_degree, 
                            lineColor = self.stim_color,
                            fillColor = self.stim_color)

        self.start_time = 0.0
        self.cumulative_phase_durations = np.cumsum(np.r_[0,self.phase_durations[self.trial_order,1:].ravel()][:-1]).reshape((self.phase_durations.shape[0], -1))

        self.all_trials = []
        for i in self.trial_order:

            # this_trial_parameters = copy.copy(standard_parameters)
            this_trial_parameters={
                                    'x_pos_1': x_test_positions_tiled[i,0], 
                                    'x_pos_2': x_test_positions_tiled[i,1], 
                                    'y_order': y_test_positions_tiled[i],
                                    'eye_dir': eye_dir[i],
                                    'ITI': ITIs[i],
                                    'TR': self.standard_parameters['TR'],
                                    'sp_amplitude':self.standard_parameters['sp_path_amplitude'],
                                    'test_stim_y_offset':self.standard_parameters['test_stim_y_offset'],
                                    'sp_path_elevation':self.standard_parameters['sp_path_elevation'],
                                    'sp_path_temporal_frequency':self.standard_parameters['sp_path_temporal_frequency'],
                                     }

            self.all_trials.append(SPTrial(this_trial_parameters, phase_durations = self.phase_durations[i], session = self, screen = self.screen, tracker = self.tracker))

    
    def close(self):
        super(SPSession, self).close()        
    
    def run(self):
        """docstring for fname"""
        # cycle through trials
        for i, trial in enumerate(self.all_trials):
            # run the prepared trial
            trial.run(ID = i)
            if self.stopped == True:
                break
        self.close()
    

