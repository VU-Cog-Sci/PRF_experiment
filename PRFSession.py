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

import appnope
appnope.nope()

class PRFSession(EyelinkSession):
	def __init__(self, subject_initials, index_number,scanner, tracker_on):
		super(PRFSession, self).__init__( subject_initials, index_number)
		
		background_color = (np.array(BGC)/255*2)-1
		screen = self.create_screen( size = DISPSIZE, full_screen =FULLSCREEN, physical_screen_distance = SCREENDIST, background_color = background_color, physical_screen_size = (SCREENSIZE) )
		event.Mouse(visible=False, win=screen)
		self.standard_parameters = standard_parameters

		self.create_output_file_name(task='prf')
		if tracker_on:
			self.create_tracker(auto_trigger_calibration = 1, calibration_type = 'HV9')
			if self.tracker_on:
				self.tracker_setup()
		else:
			self.create_tracker(tracker_on = False)
		
   #      if tracker_on:
            
   #          # how many points do we want:
   #          n_points = 9

			# # order should be with 5 points: center-up-down-left-right
			# # order should be with 9 points: center-up-down-left-right-leftup-rightup-leftdown-rightdown 
			# # order should be with 13: center-up-down-left-right-leftup-rightup-leftdown-rightdown-midleftmidup-midrightmidup-midleftmiddown-midrightmiddown
			# # so always: up->down or left->right
   #          # creat tracker
   #          self.create_tracker(auto_trigger_calibration = 0, calibration_type = 'HV%d'%n_points)
   #          # set the background and foreground to what we want:
   #          # self.tracker.target_foreground_color(0,0,0)
   #          # self.tracker.target_background_color(255,255,255)

   #          # create the calibration targets:
   #          # note: 0,0 is the upper left corner of the screen

   #          ecc = standard_parameters['calibration_ecc'] * self.pixels_per_degree

   #          # x_ratio_covered = standard_parameters['eyetracking_amplitude']/(DISPSIZE[0]/self.pixels_per_degree)
   #          # x_edge = (1-x_ratio_covered)*DISPSIZE[0]/2

   #          # max y will be (y_portion-1)/y_portion of screen height, and min y 1/y_portion
   #          y_portion = 5
			
   #          # set calibration targets
   #          cal_center_x = DISPSIZE[0]/2
   #          cal_right_x = DISPSIZE[0]+ecc
   #          cal_left_x = DISPSIZE[0]-ecc
   #          cal_center_y = DISPSIZE[1]# self.ymid
   #          cal_up_y = DISPSIZE[0]-ecc
   #          cal_down_y = self.ywidth/y_portion*(y_portion-1)
            
   #          cal_center = [cal_center_x,cal_center_y]
   #          cal_left = [cal_left_x,cal_center_y]
   #          cal_right = [cal_right_x,cal_center_y]
   #          cal_up = [cal_center_x,cal_up_y]
   #          cal_down = [cal_center_x,cal_down_y]
   #          cal_leftup = [cal_left_x,cal_up_y]
   #          cal_rightup = [cal_right_x,cal_up_y]
   #          cal_leftdown = [cal_left_x,cal_down_y]
   #          cal_rightdown = [cal_right_x,cal_down_y]			
            
   #          # set validation targets			
   #          val_center_x = DISPSIZE[0]/2
   #          val_right_x = DISPSIZE[0]-(x_edge*2)
   #          val_left_x = x_edge*2
   #          val_center_y = self.ywidth/2
   #          val_up_y = self.ywidth/y_portion*2
   #          val_down_y =  self.ywidth-self.ywidth/y_portion*2	
            
   #          val_center = [val_center_x,val_center_y]
   #          val_left = [val_left_x,val_center_y]
   #          val_right = [val_right_x,val_center_y]
   #          val_up = [val_center_x,val_up_y]
   #          val_down = [val_center_x,val_down_y]
   #          val_leftup = [val_left_x,val_up_y]
   #          val_rightup = [val_right_x,val_up_y]
   #          val_leftdown = [val_left_x,val_down_y]
   #          val_rightdown = [val_right_x,val_down_y]	
            
   #          # get them in the right order
   #          if n_points == 5:
   #              cal_xs = np.round([cal_center[0],cal_up[0],cal_down[0],cal_left[0],cal_right[0]])
   #              cal_ys = np.round([cal_center[1],cal_up[1],cal_down[1],cal_left[1],cal_right[1]])
   #              val_xs = np.round([val_center[0],val_up[0],val_down[0],val_left[0],val_right[0]])
   #              val_ys = np.round([val_center[1],val_up[1],val_down[1],val_left[1],val_right[1]])
   #          elif n_points == 9:
   #              cal_xs = np.round([cal_center[0],cal_up[0],cal_down[0],cal_left[0],cal_right[0],cal_leftup[0],cal_rightup[0],cal_leftdown[0],cal_rightdown[0]])
   #              cal_ys = np.round([cal_center[1],cal_up[1],cal_down[1],cal_left[1],cal_right[1],cal_leftup[1],cal_rightup[1],cal_leftdown[1],cal_rightdown[1]])			
   #              val_xs = np.round([val_center[0],val_up[0],val_down[0],val_left[0],val_right[0],val_leftup[0],val_rightup[0],val_leftdown[0],val_rightdown[0]])
   #              val_ys = np.round([val_center[1],val_up[1],val_down[1],val_left[1],val_right[1],val_leftup[1],val_rightup[1],val_leftdown[1],val_rightdown[1]])						
   #          #xs = np.round(np.linspace(x_edge,DISPSIZE[0]-x_edge,n_points))
   #          #ys = np.round([self.ywidth/3*[1,2][pi%2] for pi in range(n_points)])

   #          # put the points in format that eyelink wants them, which is
   #          # calibration_targets / validation_targets: 'x1,y1 x2,y2 ... xz,yz'
   #          calibration_targets = ' '.join(['%d,%d'%(cal_xs[pi],cal_ys[pi]) for pi in range(n_points)])
   #          # just copy calibration targets as validation for now:
   #          #validation_targets = calibration_targets
   #          validation_targets = ' '.join(['%d,%d'%(val_xs[pi],val_ys[pi]) for pi in range(n_points)])

   #          # point_indices: '0, 1, ... n'
   #          point_indices = ', '.join(['%d'%pi for pi in range(n_points)])

   #          # and send these targets to the custom calibration function:
   #          self.custom_calibration(calibration_targets=calibration_targets,
   #              validation_targets=validation_targets,point_indices=point_indices,
   #              n_points=n_points,randomize_order=True,repeat_first_target=True,)
   #          # reapply settings:
   #          self.tracker_setup()
   #      else:
   #          self.create_tracker(tracker_on = False)

		self.response_button_signs = response_button_signs

		self.scanner = scanner
		self.standard_parameters['scanner'] = scanner
		# trials can be set up independently of the staircases that support their parameters
		self.prepare_trials()
		self.stim_value = 0
		self.ready_for_next_pulse = True
		print self.pixels_per_degree

		self.time_steps = self.standard_parameters['fix_time_steps']
		self.transient_occurrences = np.round(np.cumsum(np.random.exponential(self.standard_parameters['task_rate'], size = 20000) + self.standard_parameters['minimum_pulse_gap']) * (1/self.time_steps)) / (1/self.time_steps)

	def prepare_trials(self):
		"""docstring for prepare_trials(self):"""

		self.directions = np.linspace(0, 2.0 * pi, 8, endpoint = False)

		# self.tasks = np.array(['Color', 'Speed', 'Fix', 'Fix_no_stim'])
		# self.task_instructions = ['Color', 'Speed', 'Fix', 'Fix']	

		self.tasks = np.array(['Fix', 'Fix_no_stim'])
		self.task_instructions = ['Fix', 'Fix']

		self.num_elements = np.ones(len(self.tasks)) * self.standard_parameters['num_elements']
		
		if self.standard_parameters['practice']:
			self.subtasks = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			self.subdirections = [0,1,5,4,7,6,3,2,0,1,5,4,7,6,3,2,]
		else:
			self.subtasks =      [1,0,1,0,0,1,0,0,1,0,0,1,0,1]
			self.subdirections = [0,0,0,1,6,0,7,4,0,3,2,0,5,0]

		self.trial_array = np.array([[self.subdirections[i], self.subtasks[i]] for i in range(len(self.subtasks))])

		# self.trial_array = []
		# for d in range(len(self.directions)):
		# 	for t in range(len(self.tasks[self.tasks != 'Fix_no_stim'])):
		# 		self.trial_array.append([d, t])
		# for fnsti in range(self.standard_parameters['num_fns_trials']):
		# 	self.trial_array.append([0,np.arange(len(self.tasks))[self.tasks == 'Fix_no_stim']])
		# self.trial_array = np.array(self.trial_array)
		# # np.random.shuffle(self.trial_array)

		# self.trial_array = np.array([[3,0],[6,1],[1,2]])
		

		# text_file_name = "data/%s_color_ratios.txt"%self.subject_initials
		# assert os.path.isfile(text_file_name), 'NO COLOR RATIO TEXT FILE PRESENT!!!!!!!!'
		# text_file = open(text_file_name, "r")
		# RG_BY_ratio = float(text_file.readline().split('ratio: ')[-1][:-1])
		# RG_BY_ratio = float(text_file.readline().split('ratio: ')[-1][:-1])
		# text_file.close()
		RG_BY_ratio = 1
		if RG_BY_ratio > 1:
			self.standard_parameters['RG_color'] = 1
			self.standard_parameters['BY_color'] = 1/RG_BY_ratio
		else:
			self.standard_parameters['BY_color'] = 1
			self.standard_parameters['RG_color'] = 1/RG_BY_ratio

		self.fast_ratio = self.slow_ratio = 0.5
	
		self.phase_durations = np.array([
			-0.0001, # instruct time
			-0.0001, # present instruction auditorily #note : this was previously erroneously 1 second.
			-0.0001, # wait for scan pulse
			self.standard_parameters['PRF_period_in_TR'] * self.standard_parameters['TR'], # present stimulus
			self.standard_parameters['PRF_ITI_in_TR'] * self.standard_parameters['TR'] ])	# ITI

		self.phase_durations_fns = np.array([
			-0.0001, # instruct time
			-0.0001, # present instruction auditorily #note : this was previously erroneously 1 second.
			-0.0001, # wait for scan pulse
			self.standard_parameters['fns_period_in_TR'] * self.standard_parameters['TR'], # present stimulus
			self.standard_parameters['PRF_ITI_in_TR'] * self.standard_parameters['TR'] ])	# ITI

		fix_size = self.standard_parameters['fix_size'] * self.pixels_per_degree
		fix_rim_size = self.standard_parameters['fix_size'] * self.pixels_per_degree * 1.33
		fix_outer_rim_size = self.standard_parameters['fix_size'] * self.pixels_per_degree * 2
		# fixation point
		self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=fix_rim_size, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
		self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=fix_outer_rim_size, pos = np.array((0.0,0.0)), color = self.screen.background_color, maskParams = {'fringeWidth':0.4})
		self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=fix_size, pos = np.array((0.0,0.0)), color = self.screen.background_color, opacity = 1.0, maskParams = {'fringeWidth':0.4})
		
		stim_ratio = (self.standard_parameters['max_ecc']*2) * self.pixels_per_degree / self.screen_pix_size[1]
		ecc_mask = filters.makeMask(matrixSize = 2048, shape='raisedCosine', radius=stim_ratio*self.screen_pix_size[1]/self.screen_pix_size[0], center=(0.0, 0.0), range=[1, -1], fringeWidth=0.1 )
		self.mask_stim = visual.PatchStim(self.screen, mask=ecc_mask,tex=None, size=(self.screen_pix_size[0], self.screen_pix_size[0]), pos = np.array((0.0,0.0)), color = self.screen.background_color) # 
	
	def close(self):
		super(PRFSession, self).close()
	
	def run(self):
		"""docstring for fname"""
		# cycle through trials
		for i in range(len(self.trial_array)):
			# prepare the parameters of the following trial based on the shuffled trial array
			this_trial_parameters = self.standard_parameters.copy()
			this_trial_parameters['orientation'] = self.directions[self.trial_array[i,0]]
			this_trial_parameters['task_index'] = self.trial_array[i,1]

			if this_trial_parameters['task_index'] == 0:
				these_phase_durations = self.phase_durations.copy()
			elif this_trial_parameters['task_index'] == 1:
				these_phase_durations = self.phase_durations_fns.copy()

			this_trial = PRFTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
			
			# run the prepared trial
			this_trial.run(ID = i)
			if self.stopped == True:
				break
		self.close()
	

