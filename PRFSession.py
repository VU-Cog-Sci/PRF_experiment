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
from standard_parameters import *
from Staircase import YesNoStaircase

import appnope
appnope.nope()



class PRFSession(EyelinkSession):
	def __init__(self, subject_initials, index_number,scanner, tracker_on):
		super(PRFSession, self).__init__( subject_initials, index_number)

		self.create_screen( size = screen_res, full_screen = 0, physical_screen_distance = 159.0, background_color = background_color, physical_screen_size = (70, 40) )

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
		self.prepare_staircases()
		self.prepare_sounds()

	def prepare_sounds(self):
		for ut in self.unique_tasks:
			self.read_sound_file('sounds/%s.wav'%ut.lower())
		
	def prepare_staircases(self):
		# staircases
		# Quest(tGuess,tGuessSd,pThreshold,beta,delta,gamma,grain=0.01,range=None)
		self.nr_staircases_ecc = 4
		# self.initial_values = [0.25, 2, 0.2] # for self.unique_tasks, 
		self.initial_values = [0.25, 4, 0.2] # for self.unique_tasks, 

		self.staircase_file_name = os.path.join(os.path.split(self.output_file)[0], self.subject_initials + '_prf_quest.pickle')
		if os.path.exists( self.staircase_file_name ):
			with open(self.staircase_file_name) as f:
				self.staircases = pickle.load(f)
		else:
			# create staircases
			self.staircases = {}
			for i, t in enumerate(self.unique_tasks):
				for j in range(self.nr_staircases_ecc):
					self.staircases.update({t + '_%i'%j:
								Quest.QuestObject(
										tGuess = self.initial_values[i], 
										tGuessSd = self.initial_values[i] * 3.0, 
										pThreshold = 0.85, 
										beta = 3.5, 
										delta = 0.01, 
										gamma = 0.0, 
										grain = 0.01, 
										range = None 
										) 
									})
	
	def prepare_trials(self):
		"""docstring for prepare_trials(self):"""
		# 8 directions, 7 tasks
		self.directions = np.linspace(0, 2.0 * pi, 8, endpoint = False)
		self.tasks = ['speed']
		self.task_instructions = ['Speed']
		# self.tasks = ['color', 'speed', 'color', 'speed', 'fix', 'fix', 'fix_no_stim']
		# self.task_instructions = ['Color', 'Speed', 'Color', 'Speed', 'Fix', 'Fix', 'Fix']	
		self.standard_parameters = standard_parameters

		self.num_elements = np.ones(len(self.task_instructions)) * self.standard_parameters['num_elements']
		self.unique_tasks = ['Color', 'Speed', 'Fix']
		
		self.trial_array = []
		for d in range(len(self.directions)):
			for t in range(len(self.tasks)):
				self.trial_array.append([d, t])
		self.trial_array = np.array(self.trial_array)
		np.random.shuffle(self.trial_array)
		

		text_file_name = "data/%s_color_ratios.txt"%self.subject_initials
		if os.path.isfile(text_file_name):
			text_file = open(text_file_name, "r")
			RG_BY_ratio = float(text_file.readline().split('ratio: ')[-1][:-1])
			text_file.close()
			self.standard_parameters['RG_BY_ratio'] = RG_BY_ratio
		else:
			self.standard_parameters['RG_BY_ratio'] = 1

		self.phase_durations = np.array([-0.0001,-0.0001, 1.00, self.standard_parameters['period'], 0.001])

		# stimuli
		self.fixation_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=12.5, pos = np.array((0.0,0.0)), color = (0,0,0), maskParams = {'fringeWidth':0.4})
		self.fixation_outer_rim = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=17.5, pos = np.array((0.0,0.0)), color = (-1.0,-1.0,-1.0), maskParams = {'fringeWidth':0.4})
		self.fixation = visual.PatchStim(self.screen, mask='raisedCos',tex=None, size=5.0, pos = np.array((0.0,0.0)), color = (0,0,0), opacity = 1.0, maskParams = {'fringeWidth':0.4})

		screen_width, screen_height = self.screen_pix_size
		
		ecc_mask = filters.makeMask(matrixSize = 2048, shape='raisedCosine', radius=self.standard_parameters['stim_size'] * self.screen_pix_size[1] / self.screen_pix_size[0], center=(0.0, 0.0), range=[1, -1], fringeWidth=0.1 )
		self.mask_stim = visual.PatchStim(self.screen, mask=ecc_mask,tex=None, size=(self.screen_pix_size[0], self.screen_pix_size[0]), pos = np.array((0.0,0.0)), color = self.screen.background_color) # 
	
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
			this_trial_parameters['task_index'] = self.trial_array[i,1]
			# this_trial_parameters['task_instruction'] = self.task_instructions[self.trial_array[i,1]]
			# this_trial_parameters['task'] = self.tasks[self.trial_array[i,1]]
			this_trial_parameters['unique_task'] = self.unique_tasks.index(self.task_instructions[self.trial_array[i,1]])
			this_trial_parameters['num_elements'] = self.num_elements[self.trial_array[i,1]]

			these_phase_durations = self.phase_durations.copy()
			if i == 0:
				these_phase_durations[1] = initial_wait_time

			this_trial = PRFTrial(this_trial_parameters, phase_durations = these_phase_durations, session = self, screen = self.screen, tracker = self.tracker)
			
			# run the prepared trial
			this_trial.run(ID = i)
			if self.stopped == True:
				break
		self.close()
	

