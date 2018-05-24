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
		
        self.fix_sp = fix_sp


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

            x_ratio_covered = (standard_parameters['eyetracking_amplitude'])/(DISPSIZE[0]/self.pixels_per_degree)
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
                n_points=n_points,randomize_order=True,repeat_first_target=True)
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

        if self.fix_sp == 'n':
            # max_ecc = self.standard_parameters['target_max_ecc']
            max_ecc = self.standard_parameters['sp_path_amplitude']/4
        elif self.fix_sp == 'y':
            max_ecc = self.standard_parameters['sp_path_amplitude']/2
      
        # define range of x positions
        x_test_positions = np.linspace(-max_ecc, max_ecc, self.standard_parameters['n_targets']/4)

        # double x positions, to add above and below positions
        x_test_positions_rep = np.tile(x_test_positions,2)
        y_test_positions = np.concatenate((-1 * np.ones(x_test_positions.shape[0]), np.ones(x_test_positions.shape[0])))

        # double the whole thing so we can add eye dir 
        x_test_positions_tiled = np.tile(x_test_positions_rep, 2)
        y_test_positions_tiled = np.tile(y_test_positions, 2)

        # now add eye dir
        if self.fix_sp=='n':
            eye_dir = np.concatenate([np.ones(int(x_test_positions_tiled.shape[0]/2))*-1,np.ones(int(x_test_positions_tiled.shape[0]/2))])
        else:
            eye_dir = np.zeros(self.standard_parameters['n_targets'])
           
        # now let's create a random trial order 
        self.trial_order = np.arange(self.standard_parameters['n_targets'])
        np.random.shuffle(self.trial_order)

        # and apply
        x_test_positions= x_test_positions_tiled[self.trial_order]
        y_test_positions = y_test_positions_tiled[self.trial_order]
        eye_dir = eye_dir[self.trial_order]  

        # now for the ITIs
        precueITIs = np.load('ITIs/precueITIs.npy') #np.random.exponential(self.standard_parameters['mean_iti'], self.standard_parameters['n_targets']) + self.standard_parameters['min_iti']
        postcueITIs = np.load('ITIs/postcueITIs.npy') #np.random.exponential(self.standard_parameters['mean_iti'], self.standard_parameters['n_targets']) + self.standard_parameters['min_iti']
        # and separately shuffle the ITIs
        np.random.shuffle(precueITIs)
        np.random.shuffle(postcueITIs)

        # now add the first and last empty trials:
        x_test_positions = np.hstack([-1e3,x_test_positions,-1e3]) #-1e3 means off the screen)
        y_test_positions = np.hstack([-1e3,y_test_positions,-1e3]) #-1e3 means off the screen)
        precueITIs = np.hstack([self.standard_parameters['warming_up_period'],ITIs,self.standard_parameters['warming_up_period']])
        postcueITIs = np.hstack([0,ITIs,0])
        eye_dir = np.hstack([0,eye_dir,0])        

        # phase overview
        # phase 0: wait for t on first trial
        # phase 1: exponential wait interval
        # phase 2: presentation of saccade cue
        # phase 3: exponential response window (starts with stimulus presentation)
        # phae 4: presentation of return saccade cue

        # define all durations per trial
        self.phase_durations = np.array([[
            -0.0001,                                                                 # phase 0 only in trial 0
            precueITIs[t],                                                         # phase 1 wait time at fixation
            self.standard_parameters['target_delay'],             # phase 2 cue presentation
            self.standard_parameters['offset_delay'],              # phase 3 target presentation, cue presentation
            postcueITIs[t],                                                        # phase 4  all stimuli turn off during this duration
            # self.standard_parameters['return_cue_dur']        # phase 4
            ] for t in range(self.standard_parameters['n_targets'])] )   

        print 'run will last %2f seconds (%.2f minutes)'%(np.sum(self.phase_durations),np.sum(self.phase_durations)/60)

        self.ref_left = visual.Rect(self.screen, 
                    width = self.standard_parameters['ref_stim_width']*self.pixels_per_degree,  
                    height = self.standard_parameters['ref_stim_height']*self.pixels_per_degree, 
                    lineColor = self.stim_color,
                    fillColor = self.stim_color)

        self.ref_right = visual.Rect(self.screen, 
                    width = self.standard_parameters['ref_stim_width']*self.pixels_per_degree,  
                    height = self.standard_parameters['ref_stim_height']*self.pixels_per_degree, 
                    lineColor = self.stim_color,
                    fillColor = self.stim_color)

        self.fixation_center = visual.PatchStim(self.screen,
	mask='raisedCos',
	tex=None, 
	size=self.standard_parameters['sp_target_size']*self.pixels_per_degree, 
	pos = np.array((0.0,0.0)), 
	color = self.stim_color, 
	opacity = 1.0, 
	maskParams = {'fringeWidth':0.4})

        self.saccade_cue = visual.Rect(self.screen, 
                    height = 0.05*self.pixels_per_degree,  
                    width = 0.2*self.pixels_per_degree, 
                    lineColor = self.stim_color,
                    fillColor = self.stim_color)
   
        # self.cue_right_stim = visual.Polygon(self.screen,
        #     edges = 3,
        #     radius = self.standard_parameters['sp_target_size']*self.pixels_per_degree/2, 
        #     fillColor = self.stim_color,
        #     lineColor = self.stim_color,
        #     ori = 90,
        #     opacity = 1.0, 
        #     pos = np.array((0.0,0.0)), 
        #     )

        # self.cue_left_stim = visual.Polygon(self.screen,
        #     edges = 3,
        #     radius = self.standard_parameters['sp_target_size']*self.pixels_per_degree/2, 
        #     fillColor = self.stim_color,
        #     lineColor = self.stim_color,
        #     ori = 270,
        #     opacity = 1.0, 
        #     pos = np.array((0.0,0.0)), 
        #     )

        # self.cue_cent_stim = visual.Polygon(self.screen,
        #     edges = 4,
        #     radius = self.standard_parameters['sp_target_size']*self.pixels_per_degree/2, 
        #     fillColor = self.stim_color,
        #     lineColor = self.stim_color,
        #     ori = 0,
        #     opacity = 1.0, 
        #     pos = np.array((0.0,0.0)), 
        #     )

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

        # add stuff to standard parameters so it is saved afterwards:
        self.standard_parameters['pixels_per_degree'] = self.pixels_per_degree

        # now create trial loop
        self.all_trials = []
        for i in range(self.standard_parameters['n_targets']):#self.trial_order:

            this_trial_parameters=self.standard_parameters
            this_trial_parameters{
                                    # add trial varying params:
                                    'x_pos': x_test_positions[i],
                                    'y_order': y_test_positions[i],
                                    'eye_dir': eye_dir[i],
                                    'answer': self.standard_parameters['default_answer'], # fill in default answer to initiate answer variable
                                    'fixate':(self.fix_sp=='y'),
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
    

