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
from SpeedMatcherTrial import *
from standard_parameters import *
from Staircase import YesNoStaircase

import appnope
appnope.nope()

class SpeedMatcherSession(EyelinkSession):
	def __init__(self, subject_initials, index_number, scanner, tracker_on):
		super(SpeedMatcherSession, self).__init__( subject_initials, index_number)
		
		self.create_screen( size = screen_res, full_screen = 0, physical_screen_distance = 159.0, background_color = background_color, physical_screen_size = (70, 40) )

		self.standard_parameters = standard_parameters

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
		self.all_speed_values = []
		self.exp_start_time = 0.0
		self.speed_ratio_step = 0.02

	
	def prepare_trials(self):
		"""docstring for prepare_trials(self):"""
		
		self.speed_offsets = (np.random.rand(self.standard_parameters['num_trials']))

		self.phase_durations = np.array([-0.0001,-0.0001, 1.00, self.standard_parameters['period'], 0.001])
		
		# stimuli
		self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=12.5, pos = np.array((0.0,0.0)), color = (0,0,0), maskParams = {'fringeWidth':0.4})
		self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=17.5, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
		self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=5.0, pos = np.array((0.0,0.0)), color = (0,0,0), opacity = 1.0, maskParams = {'fringeWidth':0.4})

		screen_width, screen_height = self.screen_pix_size
		
		ecc_mask = filters.makeMask(matrixSize = 2048, shape='raisedCosine', radius=self.standard_parameters['stim_size'] * self.screen_pix_size[1] / self.screen_pix_size[0], center=(0.0, 0.0), range=[1, -1], fringeWidth=0.1 )
		self.mask_stim = visual.PatchStim(self.screen, mask=ecc_mask,tex=None, size=(self.screen_pix_size[0], self.screen_pix_size[0]), pos = np.array((0.0,0.0)), color = self.screen.background_color) # 
	
	def close(self):
		super(SpeedMatcherSession, self).close()
		text_file = open("data/%s_speed_ratios.txt"%self.subject_initials, "w")
		text_file.write('Mean speed ratio: %.2f\nStdev speed ratio: %.2f'%(np.mean(np.array(self.all_speed_values)),np.std(np.array(self.all_speed_values))))
		text_file.close()
	
	def run(self):
		"""docstring for fname"""
		# cycle through trials
		for i in range(self.standard_parameters['num_trials']):
			# prepare the parameters of the following trial based on the shuffled trial array
			this_trial_parameters = self.standard_parameters.copy()
			this_trial_parameters['speed_offset'] = self.speed_offsets[i]

			these_phase_durations = self.phase_durations.copy()
			if i == 0:
				these_phase_durations[1] = initial_wait_time

			this_trial = SpeedMatcherTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
			
			# run the prepared trial
			this_trial.run(ID = i)
			if self.stopped == True:
				break
		self.close()
	

