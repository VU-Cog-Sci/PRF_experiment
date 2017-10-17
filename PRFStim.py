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
		self.size_pix = session.standard_parameters['max_ecc'] * self.session.pixels_per_degree * 2
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
		self.last_stimulus_present_for_task = 0
		
		# psychopy stimuli
		self.populate_stimulus()

		# make this stimulus array a session variable, in order to have to create it only once...
		if not hasattr(session, 'element_array'):
			self.session.element_array = visual.ElementArrayStim(screen, nElements = self.num_elements, sizes = self.element_sizes, sfs = self.element_sfs, xys = self.element_positions, colors = self.colors, colorSpace = 'rgb') 

		# self.orientation_text = visual.TextStim(self.screen, text = '%d'%np.degrees(self.orientation), font = 'Helvetica Neue', pos = (0, 0), italic = True, height = 30, alignHoriz = 'center')
	
	def populate_stimulus(self):

		self.fix_gray_value = (0,0,0)

		RG_ratio = 0.5
		BY_ratio = 0.5
		fast_ratio = self.session.fast_ratio
		slow_ratio = self.session.slow_ratio

		self.colors = np.ones((self.num_elements,3)) * 0.75
			
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
		# self.element_sfs = np.ones((self.num_elements)) * self.session.standard_parameters['element_spatial_frequency']
		sf_mean = self.session.standard_parameters['element_sf_mean'] #* self.session.pixels_per_degree
		sf_min = self.session.standard_parameters['element_sf_min'] #* self.session.pixels_per_degree
		self.element_sfs = np.random.rand(self.num_elements)*sf_mean+sf_min
		self.element_sizes = np.ones((self.num_elements)) * self.session.standard_parameters['element_size'] * self.session.pixels_per_degree
		self.element_phases = np.zeros(self.num_elements)
		self.element_orientations = np.random.rand(self.num_elements) * 720.0 - 360.0
		
	
	def draw(self, phase = 0):

		self.phase = phase

		if self.redraws <= (self.phase * self.period * self.refresh_frequency):

			# define midpoint
			if np.mod(self.redraws,self.session.standard_parameters['redraws_per_TR']) == 0:
				self.midpoint = phase * self.full_width - 0.5 * self.full_width

			self.populate_stimulus()

			#if np.mod(self.redraws, self.redraw_length) == 0:			
			self.session.element_array.setSfs(self.element_sfs)
			self.session.element_array.setSizes(self.element_sizes)
			self.session.element_array.setColors(self.colors)
			self.session.element_array.setOris(self.element_orientations)
			self.session.element_array.setXYs(np.array(np.matrix(self.element_positions + np.array([0, -self.midpoint])) * self.rotation_matrix)) 
			log_msg = 'stimulus draw for phase %f, at %f'%(phase, self.session.clock.getTime())
			self.trial.events.append( log_msg )
			if self.session.tracker:
				self.session.tracker.log( log_msg )
			
			self.redraws += 1

		# if fmod(self.phase * self.period * self.refresh_frequency, 1.0) > 0.5: 
		self.session.element_array.setPhases(self.element_speeds * self.phase * self.period + self.element_phases)

		if self.session.tasks[self.trial.parameters['task_index']] != 'Fix_no_stim':
			self.session.element_array.draw()
		
		self.session.fixation_outer_rim.draw()
		self.session.fixation_rim.draw()
		# self.session.fixation.setColor(self.fix_gray_value)
		self.session.fixation.draw()

		self.session.mask_stim.draw()
		
		