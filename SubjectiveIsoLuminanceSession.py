from psychopy import visual, core, misc, event
import numpy as np
from IPython import embed as shell
from math import *

import os, sys, time, pickle
import pygame
from pygame.locals import *
# from pygame import mixer, time


sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

from Session import *
from SubjectiveIsoLuminanceTrial import *
from standard_parameters import *

import appnope
appnope.nope()

class SubjectiveIsoLuminanceSession(EyelinkSession):
	def __init__(self, subject_initials, index_number, scanner, tracker_on):
		super(SubjectiveIsoLuminanceSession, self).__init__( subject_initials, index_number)
		
		self.create_screen( size = screen_res, full_screen = 0, physical_screen_distance = 159.0, background_color = background_color, physical_screen_size = (70, 40) )

		self.standard_parameters = {
		'period': 30,
		'num_trials' : 5,
		'redraws_per_stim': 4,
		'stim_size': 1000
		}

		self.create_output_file_name()
		if tracker_on:
			self.create_tracker(auto_trigger_calibration = 1, calibration_type = 'HV9')
		else:
			self.create_tracker(tracker_on = False)
		
		self.scanner = scanner
		# trials can be set up independently of the staircases that support their parameters
		self.prepare_trials()
		self.exp_start_time = 0.0

		self.color_step = 0.05

	def prepare_trials(self):
		"""docstring for prepare_trials(self):"""
		
		self.RG_start_offsets = np.random.rand(self.standard_parameters['num_trials'])/10
		self.BY_start_offsets = np.random.rand(self.standard_parameters['num_trials'])/10

		self.phase_durations = np.array([-0.0001,-0.0001, 1.00, self.standard_parameters['period'], 0.001])

		# stimuli
		self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=12.5, pos = np.array((0.0,0.0)), color = (0,0,0), maskParams = {'fringeWidth':0.4})
		self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=17.5, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
		self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=5.0, pos = np.array((0.0,0.0)), color = (0,0,0), opacity = 1.0, maskParams = {'fringeWidth':0.4})

		screen_width, screen_height = self.screen_pix_size
	
	def close(self):
		super(SubjectiveIsoLuminanceSession, self).close()
	
	def run(self):
		"""docstring for fname"""
		# cycle through trials
		for i in range(self.standard_parameters['num_trials']):
			# prepare the parameters of the following trial based on the shuffled trial array
			this_trial_parameters = self.standard_parameters.copy()
			this_trial_parameters['RG_offset'] = self.RG_start_offsets[i]
			this_trial_parameters['BY_offset'] = self.RG_start_offsets[i]

			these_phase_durations = self.phase_durations.copy()
			if i == 0:
				these_phase_durations[1] = initial_wait_time

			this_trial = SubjectiveIsoLuminanceTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
			
			# run the prepared trial
			this_trial.run(ID = i)
			if self.stopped == True:
				break
		self.close()
	

