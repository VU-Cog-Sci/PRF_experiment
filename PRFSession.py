from __future__ import division
from psychopy import visual, core, misc, event, data
import numpy as np
# from IPython import embed as shell
from math import *

import os, sys, time, pickle
import pygame
from pygame.locals import *
# from pygame import mixer, time

# import Quest

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

from Session import *
from Staircase import ThreeUpOneDownStaircase
from PRFTrial import *
from constants import *
# set screen to square when asking for circle mask
if standard_parameters['mask_type'] == 0:
    standard_parameters['horizontal_stim_size'] = DISPSIZE[1]/DISPSIZE[0]

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

            # it is setup to do a 9 or 5 point circular calibration, at reduced ecc

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
        
        self.response_button_signs = response_button_signs

        self.scanner = scanner
        # trials can be set up independently of the staircases that support their parameters
        self.prepare_trials()
        self.nr_staircases_ecc = standard_parameters['nr_staircases_ecc']
        self.prepare_staircases()

    def prepare_staircases(self):
        # fix, color
        self.initial_values = [1,2]
        stepsizes = np.r_[np.array([1.0,1.0,0.5,0.5,0.25,0.25]), 0.25*np.ones((int(1e4)))]

        self.staircase_file_name = os.path.join(os.path.split(self.output_file)[0], self.subject_initials + '_prf_staircase.pickle')
        if os.path.exists( self.staircase_file_name ):
            with open(self.staircase_file_name) as f:
                self.staircases = pickle.load(f)
        else:
            # create staircases
            self.staircases = {}
            for i, t in enumerate(['fix','bar']):
                for j in range(self.nr_staircases_ecc):
                    self.staircases.update({t + '_%i'%j:
                                ThreeUpOneDownStaircase(initial_value = standard_parameters['quest_initial_stim_values'], 
                                                             initial_stepsize=standard_parameters['quest_stepsize'],
                                                             max_nr_trials = 5000,
                                                             stepsize_multiplication_on_reversal = standard_parameters['quest_stepsize_multiplication_on_reversal'])  
                                    })
    
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
            self.stim_bool = [1,1,1,1]
            self.direction_indices = np.array([0,2,6,4])
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
    
    def close(self):
        super(PRFSession, self).close()
        with open(self.staircase_file_name, 'w') as f:
            pickle.dump(self.staircases, f)
        # for s in self.staircases.keys():
            # print 'Staircase {}'.format(s)
            # self.staircases[s].printAsText()
        
    
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
    

