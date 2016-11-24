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
from HRFMapperTrial import *
from constants import *


try:
    import appnope
    appnope.nope()
except:
    print 'APPNOPE NOT ACTIVE!'

class HRFMapperSession(EyelinkSession):
    def __init__(self, subject_initials, index_number,scanner, tracker_on):
        super(HRFMapperSession, self).__init__( subject_initials, index_number)
		
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

        checker_y_loc = np.hstack([1e3,np.tile([1,-1],self.standard_parameters['HRF_mapper_n_trials']/2),1e3]) * (self.ywidth/4)
        trial_durations = np.hstack([self.standard_parameters['warming_up_n_TRs'],np.tile([1,1],self.standard_parameters['HRF_mapper_n_trials']/2)* self.standard_parameters['HRF_mapper_period_in_TR'],self.standard_parameters['warming_up_n_TRs']]) 

        # define all durations per trial
        self.phase_durations = np.array([[
            -0.0001, # instruct time, skipped in all trials but the first (wait for t)
            trial_durations[i]*self.standard_parameters['TR'], # smooth pursuit before stim
            ] for i in range(len(trial_durations))] )    
        
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
			pos = [0,self.screen.size[1]*self.standard_parameters['sp_path_elevation']-self.screen.size[1]/2], 
			color = self.stim_color, 
			opacity = 1.0, 
			maskParams = {'fringeWidth':0.4})

        # the checkerboards:
        n_squares_x = np.round((self.standard_parameters['sp_path_amplitude'])/self.standard_parameters['square_width_deg'])
        n_squares_y = np.round(self.ywidth/2/self.pixels_per_degree/self.standard_parameters['square_width_deg'])
        self.stim1 = visual.GratingStim(self.screen, 
            tex = np.tile(np.tile([[-1,1],[1,-1]],n_squares_y).T,n_squares_x),
            size = [self.standard_parameters['sp_path_amplitude']*self.pixels_per_degree,self.ywidth/2],
            color = (1,1,1))
        self.stim2 = visual.GratingStim(self.screen, 
            tex = np.tile(np.tile([[1,-1],[-1,1]],n_squares_y).T,n_squares_x),
            size = [self.standard_parameters['sp_path_amplitude']*self.pixels_per_degree,self.ywidth/2],
            color = (1,1,1))

        self.start_time = 0.0
        # self.cumulative_phase_durations = np.cumsum(np.r_[0,self.phase_durations[self.trial_order,1:].ravel()][:-1]).reshape((self.phase_durations.shape[0], -1))
        self.cumulative_phase_durations = np.cumsum(np.r_[0,self.phase_durations[:,1:].ravel()][:-1]).reshape((self.phase_durations.shape[0], -1))

        self.all_trials = []
        for i in range(len(trial_durations)):#self.trial_order:

            this_trial_parameters={
                                    # trial varying params
                                    'trial_duration':trial_durations[i],
                                    'stim_y':checker_y_loc[i],

                                    # these params don't vary over trials:
                                    'TR': self.standard_parameters['TR'],
                                    'test_stim_y_offset':self.standard_parameters['test_stim_y_offset'],
                                    'sp_path_elevation':self.standard_parameters['sp_path_elevation'],
                                    'sp_path_temporal_frequency':self.standard_parameters['sp_path_temporal_frequency'],
                                    'warming_up_n_TRs':self.standard_parameters['warming_up_n_TRs'],
                                    'nframes':self.standard_parameters['nframes']
                                    'square_width_deg':self.standard_parameters['square_width_deg']
                                     }

            self.all_trials.append(HRFMapperTrial(this_trial_parameters, phase_durations = self.phase_durations[i], session = self, screen = self.screen, tracker = self.tracker))

    
    def close(self):
        super(HRFMapperSession, self).close()        
    
    def run(self):
        """docstring for fname"""
        # cycle through trials
        for i, trial in enumerate(self.all_trials):
            # run the prepared trial
            trial.run(ID = i)
            if self.stopped == True:
                break
        self.close()
    

