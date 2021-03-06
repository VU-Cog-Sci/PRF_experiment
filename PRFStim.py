from __future__ import division
from psychopy import visual, core, misc, event, filters
import numpy as np
from scipy.signal import convolve2d
from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


class PRFStim(object):
	def __init__(self, screen, trial, session, orientation):
		# parameters
		self.num_elements = session.standard_parameters['num_elements']
		self.trial = trial
		self.session = session
		self.screen = screen
		self.size_pix = session.standard_parameters['stim_size'] * session.screen_pix_size[1]
		self.bar_width_ratio = session.standard_parameters['bar_width_ratio']
		self.orientation = orientation	# convert to radians immediately, and use to calculate rotation matrix
		self.rotation_matrix = np.matrix([[cos(self.orientation), -sin(self.orientation)],[sin(self.orientation), cos(self.orientation)]])
		self.period = session.standard_parameters['PRF_period_in_TR'] * session.standard_parameters['TR']
		self.refresh_frequency = session.standard_parameters['redraws_per_TR'] / session.standard_parameters['TR']
		self.task_rate = session.standard_parameters['task_rate']

		self.RG_color=session.standard_parameters['RG_color']
		self.BY_color=session.standard_parameters['BY_color']

		self.fast_speed = session.standard_parameters['fast_speed']
		self.slow_speed = session.standard_parameters['slow_speed']

		self.full_width = self.size_pix * (1.0 * self.bar_width_ratio + 1.0)
		self.midpoint = 0 * self.full_width - 0.5 * self.full_width

		self.phase = 0
		# bookkeeping variables
		self.eccentricity_bin = -1
		self.redraws = 0
		self.frames = 0
		self.last_stimulus_present_for_task = 0
		
		# construct timecourses of tasks
		# task_rate is in task_rate seconds per occurrence. we add 2x refresh frequency to avoid transients in the first second(s) and those following too quickly, and add an insane number to avoid tasks in the last second(s). 
		self.transient_occurrences = np.round(np.cumsum(np.random.exponential(self.task_rate * self.refresh_frequency, size = (len(self.session.tasks), 20)) + self.session.standard_parameters['minimum_pulse_gap']*self.refresh_frequency, axis = 1))
		self.transient_occurrences[self.transient_occurrences > (self.period * self.refresh_frequency - self.session.standard_parameters['TR'] * self.refresh_frequency)] += 500000
		self.transient_occurrences[self.transient_occurrences < (self.session.standard_parameters['TR'] * 2 * self.refresh_frequency)] += 500000

		# psychopy stimuli
		self.populate_stimulus()

		# make this stimulus array a session variable, in order to have to create it only once...
		if not hasattr(session, 'element_array'):
			self.session.element_array = visual.ElementArrayStim(screen, nElements = self.num_elements, sizes = self.element_sizes, sfs = self.element_sfs, xys = self.element_positions, colors = self.colors, colorSpace = 'rgb') 

		# set this to its default no-answer necessary value of None - this is tested for in PRFTrial when incorporating responses
		self.last_sampled_staircase = None

	def convert_quest_sample(self,quest_sample):

		return 1 - (1/(np.e**quest_sample+1))
	
	def populate_stimulus(self):

		# what eccentricity bin are we in? phase runs from 0 to 1, so we take the ecc on a linear scale for now
		self.eccentricity_bin = floor(np.abs(self.phase-0.5) * 2.0 * self.session.nr_staircases_ecc)

		self.fix_gray_value = (0,0,0)

		RG_ratio = 0.5
		BY_ratio = 0.5
		fast_ratio = self.session.fast_ratio
		slow_ratio = self.session.slow_ratio

		for i, task in enumerate(self.session.tasks):

			if self.redraws in list(self.transient_occurrences[i]):

				# now fill in this value into the different cues/tasks whatever, supplement this with a quest staircase...
				if self.session.tasks[i] == 'Color':

					color_quest_sample = self.session.staircases[self.session.tasks[i] + '_%i'%self.eccentricity_bin].quantile()
					color_1_ratio = self.convert_quest_sample(color_quest_sample)
					color_2_ratio = 1-color_1_ratio

					self.present_color_task_sign = np.random.choice([-1,1])
					if self.present_color_task_sign == -1:
						RG_ratio = color_1_ratio
						BY_ratio = color_2_ratio
					elif self.present_color_task_sign == 1:
						RG_ratio = color_2_ratio
						BY_ratio = color_1_ratio

					log_msg = 'signal in feature: %s ecc bin: %i phase: %1.3f value: %f at %f ' % (self.session.tasks[i], self.eccentricity_bin, self.phase, color_quest_sample, self.session.clock.getTime())

				elif self.session.tasks[i] == 'Speed':

					speed_quest_sample = self.session.staircases[self.session.tasks[i] + '_%i'%self.eccentricity_bin].quantile()
					speed_1_ratio = self.convert_quest_sample(speed_quest_sample)
					speed_2_ratio = 1-speed_1_ratio

					self.present_speed_task_sign = np.random.choice([-1,1])
					if self.present_speed_task_sign == -1:
						slow_ratio = speed_1_ratio
						fast_ratio = speed_2_ratio
					elif self.present_speed_task_sign == 1:
						slow_ratio = speed_2_ratio
						fast_ratio = speed_1_ratio

					log_msg = 'signal in feature: %s ecc bin: %i phase: %1.3f value: %f at %f ' % (self.session.tasks[i], self.eccentricity_bin, self.phase, speed_quest_sample, self.session.clock.getTime())

				elif (self.session.tasks[i] == 'Fix') * (self.session.tasks[self.trial.parameters['task_index']] != 'Fix_no_stim'):

					fix_quest_sample = self.session.staircases[self.session.tasks[i] + '_%i'%self.eccentricity_bin].quantile()
					fix_value = (self.convert_quest_sample(fix_quest_sample) - 0.5) * 2.0
					self.present_fix_task_sign = np.random.choice([-1,1])
					self.fix_gray_value = np.ones(3) * fix_value * self.present_fix_task_sign

					log_msg = 'signal in feature: %s ecc bin: %i phase: %1.3f value: %f at %f ' % (self.session.tasks[i], self.eccentricity_bin, self.phase, fix_quest_sample, self.session.clock.getTime())

				elif (self.session.tasks[i] == 'Fix_no_stim') * (self.session.tasks[self.trial.parameters['task_index']] == 'Fix_no_stim'):

					fns_quest_sample = self.session.staircases[self.session.tasks[i]].quantile()
					fns_value = (self.convert_quest_sample(fns_quest_sample) - 0.5) * 2.0
					self.present_fns_task_sign = np.random.choice([-1,1])
					self.fix_gray_value = np.ones(3) * fns_value * self.present_fns_task_sign

					log_msg = 'signal in feature: %s value: %f at %f ' % (self.session.tasks[i], fns_quest_sample, self.session.clock.getTime())

				if 'log_msg' in locals():
					if self.session.tracker:
						self.session.tracker.log( log_msg )
					self.trial.events.append( log_msg )
					print log_msg
				
				# tell the subject he/she has something to do, for the task-relevant shizzle that gets shown during this stimulus refresh.
				if i == self.trial.parameters['task_index']:
					self.session.play_sound()
					if self.session.tasks[i] != 'Fix_no_stim':
						self.last_sampled_staircase = self.session.tasks[i] + '_%i'%self.eccentricity_bin
					else:
						self.last_sampled_staircase = self.session.tasks[i] 

		# Now set the actual stimulus parameters
		self.colors = np.concatenate((np.ones((np.round(self.num_elements*RG_ratio/2.0),3)) * np.array([1,-1,0]) * self.RG_color,  # red/green - red
									np.ones((np.round(self.num_elements*RG_ratio/2.0),3)) * np.array([-1,1,0]) * self.RG_color,  # red/green - green
									np.ones((np.round(self.num_elements*BY_ratio/2.0),3)) * np.array([-1,-1,1]) * self.BY_color,  # blue/yellow - blue
									np.ones((np.round(self.num_elements*BY_ratio/2.0),3)) * np.array([1,1,-1]) * self.BY_color))  # blue/yellow - yellow
		np.random.shuffle(self.colors)

		self.element_speeds = np.concatenate((np.ones(np.round(self.num_elements*fast_ratio)) * self.session.standard_parameters['fast_speed'],
											np.ones(np.round(self.num_elements*slow_ratio)) * self.session.standard_parameters['slow_speed']))
		np.random.shuffle(self.element_speeds)


		self.element_positions = np.random.rand(self.num_elements, 2) * np.array([self.size_pix, self.size_pix * self.bar_width_ratio]) - np.array([self.size_pix/2.0, (self.size_pix * self.bar_width_ratio)/2.0])
		self.element_sfs = np.ones((self.num_elements)) * self.session.standard_parameters['element_spatial_frequency']
		self.element_sizes = np.ones((self.num_elements)) * self.session.standard_parameters['element_size']
		self.element_phases = np.zeros(self.num_elements)
		self.element_orientations = np.random.rand(self.num_elements) * 720.0 - 360.0
		
	
	def draw(self, phase = 0):
		self.phase = phase
		self.frames += 1

		if self.redraws <= (self.phase * self.period * self.refresh_frequency):
			self.redraws = self.redraws + 1

			self.populate_stimulus()
			self.session.element_array.setSfs(self.element_sfs)
			self.session.element_array.setSizes(self.element_sizes)
			self.session.element_array.setColors(self.colors)
			self.session.element_array.setOris(self.element_orientations)
			if np.mod(self.redraws,self.session.standard_parameters['redraws_per_TR']) == 1:
				self.midpoint = phase * self.full_width - 0.5 * self.full_width
			self.session.element_array.setXYs(np.array(np.matrix(self.element_positions + np.array([0, -self.midpoint])) * self.rotation_matrix)) 
			log_msg = 'stimulus draw for phase %f, at %f'%(phase, self.session.clock.getTime())
			self.trial.events.append( log_msg )
			if self.session.tracker:
				self.session.tracker.log( log_msg )

			
		# if fmod(self.phase * self.period * self.refresh_frequency, 1.0) > 0.5: 
		self.session.element_array.setPhases(self.element_speeds * self.phase * self.period + self.element_phases)

		if self.session.tasks[self.trial.parameters['task_index']] != 'Fix_no_stim':
			self.session.element_array.draw()
		
		self.session.fixation_outer_rim.draw()
		self.session.fixation_rim.draw()
		self.session.fixation.setColor(self.fix_gray_value)
		self.session.fixation.draw()

		self.session.mask_stim.draw()
		
		