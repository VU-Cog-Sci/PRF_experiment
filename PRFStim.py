from psychopy import visual, core, misc, event, filters
import numpy as np
from scipy.signal import convolve2d
from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


class PRFStim(object):
	def __init__(self, screen, trial, session, size_pix = 1000, num_elements = 2000, bar_width_ratio = 0.1, orientation = 0.0, period = 24.0, refresh_frequency = 4.0, task_rate = 3.5):
		# parameters
		self.num_elements = num_elements
		self.trial = trial
		self.session = session
		self.screen = screen
		self.size_pix = size_pix
		self.bar_width_ratio = bar_width_ratio
		self.orientation = orientation	# convert to radians immediately, and use to calculate rotation matrix
		self.rotation_matrix = np.matrix([[cos(self.orientation), -sin(self.orientation)],[sin(self.orientation), cos(self.orientation)]])
		self.period = period
		self.refresh_frequency = refresh_frequency
		self.task_rate = task_rate

		self.phase = 0
		# bookkeeping variables
		self.redraws = 0
		self.frames = 0
		self.last_stimulus_present_for_task = 0
		
		# construct timecourses of tasks
		# task_rate is in one per task_rate seconds. we add a refresh frequency to avoid transients in the first second, and add an insane number to avoid tasks in the last second. 
		self.transient_occurrences = np.round(np.cumsum(np.random.exponential(task_rate * refresh_frequency, size = (len(self.session.unique_tasks), 20)) + refresh_frequency, axis = 1))
		self.transient_occurrences[self.transient_occurrences > (self.trial.parameters['period'] * refresh_frequency - refresh_frequency)] += 500000
				
		# psychopy stimuli
		self.populate_stimulus()
		self.element_array = visual.ElementArrayStim(screen, nElements = self.num_elements, sizes = self.element_sizes, sfs = self.element_sfs, xys = self.element_positions, colors = self.colors, colorSpace = 'rgb') 

		# set this to its default no-answer necessary value of None - this is tested for in PRFTrial when incorporating responses
		self.last_sampled_staircase = None

	
	def populate_stimulus(self):

		# what eccentricity bin are we in? phase runs from 0 to 1, so we take the ecc on a linear scale for now
		self.eccentricity_bin = floor(np.abs(self.phase-0.5) * 2.0 * self.session.nr_staircases_ecc)

		self.fix_gray_value = (0,0,0)
		self.speed = self.trial.parameters['baseline_speed_for_task']
		RG_color = self.trial.parameters['baseline_color_for_task'] 
		BY_color = self.trial.parameters['baseline_color_for_task'] 



		for i, task in enumerate(self.session.unique_tasks):
			this_stim_value_incr = False
			if self.redraws in list(self.transient_occurrences[i]):
				this_stim_value_incr = True

			# now fill in this value into the different cues/tasks whatever, supplement this with a quest staircase...
			if self.session.unique_tasks[i] == 'Color' and this_stim_value_incr:
				# get quest sample here
				color_quest_sample = self.session.staircases[self.session.unique_tasks[i] + '_%i'%self.eccentricity_bin].quantile()

				self.present_color_task_sign = np.random.choice([-1,1])
				RG_color = self.trial.parameters['baseline_color_for_task'] + self.present_color_task_sign * color_quest_sample
				BY_color = self.trial.parameters['baseline_color_for_task'] + -self.present_color_task_sign * color_quest_sample

				log_msg = 'signal in task: %s ecc bin: %i phase: %1.3f value: %f at %f ' % (self.session.unique_tasks[i], self.eccentricity_bin, self.phase, self.present_color_task_sign * color_quest_sample, self.session.clock.getTime())

			elif self.session.unique_tasks[i] == 'Speed' and this_stim_value_incr:
				# get quest sample here
				speed_quest_sample = self.session.staircases[self.session.unique_tasks[i] + '_%i'%self.eccentricity_bin].quantile()

				self.present_speed_task_sign = np.random.choice([-1,1])
				self.speed = self.trial.parameters['baseline_speed_for_task'] + self.present_speed_task_sign * speed_quest_sample

				log_msg = 'signal in task: %s ecc bin: %i phase: %1.3f value: %f at %f ' % (self.session.unique_tasks[i], self.eccentricity_bin, self.phase, self.speed, self.session.clock.getTime())

			elif self.session.unique_tasks[i] == 'Fix' and this_stim_value_incr:
				# get quest sample here
				fix_quest_sample = self.session.staircases[self.session.unique_tasks[i] + '_%i'%self.eccentricity_bin].quantile()

				self.present_fix_task_sign = np.random.choice([-1,1])
				self.fix_gray_value = np.ones(3) * fix_quest_sample * self.present_fix_task_sign

				log_msg = 'signal in task: %s ecc bin: %i phase: %1.3f value: %f at %f ' % (self.session.unique_tasks[i], self.eccentricity_bin, self.phase, self.fix_gray_value[0], self.session.clock.getTime())

			if this_stim_value_incr:
				if self.session.tracker:
					self.session.tracker.log( log_msg )
				self.trial.events.append( log_msg )
				print log_msg



			# tell the subject he/she has something to do, for the task-relevant shizzle that gets shown during this stimulus refresh.
			if this_stim_value_incr and i == self.trial.parameters['unique_task']:
				self.session.play_sound()
				self.last_sampled_staircase = self.session.unique_tasks[i] + '_%i'%self.eccentricity_bin


		# Now set the actual stimulus parameters

		self.colors = np.concatenate((np.ones((self.num_elements/4.0,3)) * np.array([1,-1,0]) * RG_color,  # red/green - red
									np.ones((self.num_elements/4.0,3)) * np.array([-1,1,0]) * RG_color,  # red/green - green
									np.ones((self.num_elements/4.0,3)) * np.array([-1,-1,1]) * BY_color,  # blue/yellow - blue
									np.ones((self.num_elements/4.0,3)) * np.array([1,1,-1]) * BY_color))  # blue/yellow - yellow
		np.random.shuffle(self.colors)
		self.element_positions = np.random.rand(self.num_elements, 2) * np.array([self.size_pix, self.size_pix * self.bar_width_ratio]) - np.array([self.size_pix/2.0, (self.size_pix * self.bar_width_ratio)/2.0])
		self.element_speeds = np.ones((self.num_elements)) * self.speed

		self.element_sfs = np.ones((self.num_elements)) * self.trial.parameters['element_spatial_frequency']
		self.element_sizes = np.ones((self.num_elements)) * self.trial.parameters['element_size']
		self.element_phases = np.zeros(self.num_elements)
		self.element_orientations = np.random.rand(self.num_elements) * 720.0 - 360.0
		
	
	def draw(self, phase = 0):
		self.phase = phase
		self.frames += 1

		full_width = self.size_pix * (1.0 * self.bar_width_ratio + 1.0)
		midpoint = phase * full_width - 0.5 * full_width
		
		if self.redraws < (self.phase * self.period * self.refresh_frequency):
			self.redraws = self.redraws + 1
			self.populate_stimulus()
			self.element_array.setSfs(self.element_sfs)
			self.element_array.setSizes(self.element_sizes)
			self.element_array.setColors(self.colors)
			self.element_array.setOris(self.element_orientations)
			self.element_array.setXYs(np.array(np.matrix(self.element_positions + np.array([0, -midpoint])) * self.rotation_matrix)) #  + np.array([midpoint, 0])
			self.trial.events.append( 'stimulus populated at  ' + str(phase) + ' at ' + str(self.session.clock.getTime()) + ' for midpoint ' + str(midpoint))
			# print self.session.unique_tasks[self.trial.parameters['unique_task']] + ' - ' + self.trial.parameters['unique_task'] + ' stimulus populated at  ' + str(phase) + \
			# 		' at ' + str(self.session.clock.getTime()) + ' for midpoint ' + str(midpoint) + ' eccen bin is ' + str(self.eccentricity_bin)
			
		# if fmod(self.phase * self.period * self.refresh_frequency, 1.0) > 0.5: 
		self.element_array.setPhases(self.element_speeds * self.phase * self.trial.parameters['period'] + self.element_phases)

		if self.trial.parameters['task'] != 'fix_no_stim':
			self.element_array.draw()
		
		self.session.fixation_outer_rim.draw()
		self.session.fixation_rim.draw()
		self.session.fixation.setColor(self.fix_gray_value)
		self.session.fixation.draw()

		self.session.mask_stim.draw()
		
		