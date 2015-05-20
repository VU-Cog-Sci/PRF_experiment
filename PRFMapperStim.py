from psychopy import visual, core, misc, event, filters
import numpy as np
from scipy.signal import convolve2d
from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


class PRFMapperStim(object):
	def __init__(self, screen, trial, session,task, size_pix = 1000, num_elements = 2000, period = 24.0, task_rate = 3.5):
		# parameters
		self.num_elements = num_elements
		self.trial = trial
		self.session = session
		self.screen = screen
		self.size_pix = size_pix
		self.period = period
		# self.refresh_frequency = refresh_frequency
		self.task_rate = task_rate
		self.task = task

		self.phase = 0
		# bookkeeping variables
		self.eccentricity_bin = -1
		self.redraws = 0
		self.frames = 0
		self.last_stimulus_present_for_task = 0
		
		# construct timecourses of tasks
		# task_rate is in task_rate seconds per occurrence. we add 2x refresh frequency to avoid transients in the first second(s) and those following too quickly, and add an insane number to avoid tasks in the last second(s). 
				
		# psychopy stimuli
		self.populate_stimulus()

		# make this stimulus array a session variable, in order to have to create it only once...
		if not hasattr(session, 'element_array'):
			self.session.element_array = visual.ElementArrayStim(screen, nElements = self.num_elements, sizes = self.element_sizes, sfs = self.element_sfs, xys = self.element_positions, colors = self.colors, colorSpace = 'rgb') 

		# set this to its default no-answer necessary value of None - this is tested for in PRFTrial when incorporating responses
		self.last_sampled_staircase = None

	
	def populate_stimulus(self):

		# what eccentricity bin are we in? phase runs from 0 to 1, so we take the ecc on a linear scale for now
		# self.eccentricity_bin = floor(np.abs(self.phase-0.5) * 2.0 * self.session.nr_staircases_ecc)

		self.fix_gray_value = (0,0,0)
		self.speed = self.trial.parameters['baseline_speed_for_task']



		if self.task == 'no_color_no_speed':

			red = np.array([-1,-1,-1])
			green = np.array([1,1,1])
			yellow = np.array([-1,-1,-1])
			blue = np.array([1,1,1]) 

			self.speed = 0.0

		elif self.task == 'yes_color_no_speed':

			red = np.array([1,-1,0])
			green = np.array([-1,1,0])
			yellow = np.array([1,1,-1])
			blue = np.array([-1,-1,1]) 

			self.speed = 0.0

		elif self.task == 'no_color_yes_speed':
			red = np.array([-1,-1,-1])
			green = np.array([1,1,1])
			yellow = np.array([-1,-1,-1])
			blue = np.array([1,1,1]) 
			self.speed = self.trial.parameters['baseline_speed_for_task']

		elif self.task == 'yes_color_yes_speed':

			red = np.array([1,-1,0])
			green = np.array([-1,1,0])
			yellow = np.array([1,1,-1])
			blue = np.array([-1,-1,1]) 

			self.speed = self.trial.parameters['baseline_speed_for_task']	

		elif self.task == 'fix_no_stim':
			
			red,green,yellow,blue = self.session.background_color,self.session.background_color,self.session.background_color,self.session.background_color

			self.speed = 0


		# Now set the actual stimulus parameters

		self.colors = np.concatenate((np.ones((self.num_elements/4.0,3)) * red,  # red/green - red
									np.ones((self.num_elements/4.0,3)) * green,  # red/green - green
									np.ones((self.num_elements/4.0,3)) * blue,  # blue/yellow - blue
									np.ones((self.num_elements/4.0,3)) * yellow))  # blue/yellow - yellow
		np.random.shuffle(self.colors)
		self.element_positions = np.random.rand(self.num_elements, 2) * np.array([self.size_pix, self.size_pix]) - np.array([self.size_pix/2.0, (self.size_pix)/2.0])
		self.element_speeds = np.ones((self.num_elements)) * self.speed

		self.element_sfs = np.ones((self.num_elements)) * self.trial.parameters['element_spatial_frequency']
		self.element_sizes = np.ones((self.num_elements)) * self.trial.parameters['element_size']
		self.element_phases = np.zeros(self.num_elements)
		self.element_orientations = np.random.rand(self.num_elements) * 720.0 - 360.0
		
	
	def draw(self, phase = 0):
		self.phase = phase
		self.frames += 1

		full_width = self.size_pix * (1.0 + 1.0)
		midpoint = 0#phase * full_width - 0.5 * full_width
		
		if self.frames == 1:#self.redraws < (self.phase * self.period * self.refresh_frequency):
			self.redraws = self.redraws + 1
			self.populate_stimulus()
			self.session.element_array.setSfs(self.element_sfs)
			self.session.element_array.setSizes(self.element_sizes)
			self.session.element_array.setColors(self.colors)
			self.session.element_array.setOris(self.element_orientations)
			self.session.element_array.setXYs(np.array(np.matrix(self.element_positions + np.array([0, -midpoint])))) 
			log_msg = 'stimulus draw for phase %f, at %f'%(phase, self.session.clock.getTime())
			self.trial.events.append( log_msg )
			if self.session.tracker:
				self.session.tracker.log( log_msg )

			
		# if fmod(self.phase * self.period * self.refresh_frequency, 1.0) > 0.5: 
		self.session.element_array.setPhases(self.element_speeds * self.phase * self.trial.parameters['mapper_period'] + self.element_phases)

		if self.session.tasks[self.trial.parameters['task_index']] != 'fix_no_stim':
			self.session.element_array.draw()
		
		self.session.fixation_outer_rim.draw()
		self.session.fixation_rim.draw()
		self.session.fixation.draw()
		self.session.mask_stim.draw()
		
		