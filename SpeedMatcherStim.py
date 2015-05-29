from __future__ import division
from psychopy import visual, core, misc, event, filters
import numpy as np
from scipy.signal import convolve2d
from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


class SpeedMatcherStim(object):
	def __init__(self, screen, trial, session, speed_offset):
		# parameters
		self.num_elements = session.standard_parameters['num_elements'] * (1/session.standard_parameters['bar_width_ratio'])
		self.trial = trial
		self.session = session
		self.screen = screen
		self.size_pix = session.standard_parameters['stim_size']*session.screen_pix_size[1]

		self.speed_offset = speed_offset
		self.redraw = True
		
		# psychopy stimuli
		self.populate_stimulus()

		self.frames = 0

		# make this stimulus array a session variable, in order to have to create it only once...
		if not hasattr(session, 'element_array'):
			self.session.element_array = visual.ElementArrayStim(screen, nElements = self.num_elements, sizes = self.element_sizes, sfs = self.element_sfs, xys = self.element_positions, colors = self.colors, colorSpace = 'rgb') 

	def populate_stimulus(self):

		red = np.array([ self.session.standard_parameters['RG_color'], - self.session.standard_parameters['RG_color'],0]) 
		green = np.array([- self.session.standard_parameters['RG_color'], self.session.standard_parameters['RG_color'],0]) 
		yellow = np.array([ self.session.standard_parameters['BY_color'], self.session.standard_parameters['BY_color'],- self.session.standard_parameters['BY_color']])
		blue = np.array([- self.session.standard_parameters['BY_color'],- self.session.standard_parameters['BY_color'], self.session.standard_parameters['BY_color']]) 

		# Now set the actual stimulus parameters
		self.colors = np.concatenate((np.ones((self.num_elements/4.0,3)) * red,  # red/green - red
									np.ones((self.num_elements/4.0,3)) * green,  # red/green - green
									np.ones((self.num_elements/4.0,3)) * blue,  # blue/yellow - blue
									np.ones((self.num_elements/4.0,3)) * yellow))  # blue/yellow - yellow

		self.speed_ratio = np.min([np.max([0,self.speed_offset + self.trial.speed_ratio_diff]), 1])

		self.element_speeds = np.concatenate((np.ones(np.round(self.num_elements*(self.speed_ratio))) * self.session.standard_parameters['fast_speed'],
											np.ones(np.round(self.num_elements*(1-self.speed_ratio))) * self.session.standard_parameters['slow_speed']))

		np.random.shuffle(self.element_speeds)
		np.random.shuffle(self.colors)
		self.element_positions = np.random.rand(self.num_elements, 2) * np.array([self.size_pix, self.size_pix]) - np.array([self.size_pix/2.0, (self.size_pix)/2.0])
		self.element_sfs = np.ones((self.num_elements)) * self.session.standard_parameters['element_spatial_frequency']
		self.element_sizes = np.ones((self.num_elements)) * self.session.standard_parameters['element_size']
		self.element_orientations = np.random.rand(self.num_elements) * 720.0 - 360.0
		self.element_phases = np.zeros(self.num_elements)

	def update_speeds(self):

		self.speed_ratio = np.min([np.max([0,self.speed_offset + self.trial.speed_ratio_diff]), 1])

		self.element_speeds = np.concatenate((np.ones(np.round(self.num_elements*(self.speed_ratio))) * self.session.standard_parameters['fast_speed'],
											np.ones(np.round(self.num_elements*(1-self.speed_ratio))) * self.session.standard_parameters['slow_speed']))

		np.random.shuffle(self.element_speeds)

	
	def draw(self,phase=0):

		self.phase = phase

		if self.redraw:
			self.populate_stimulus()
			self.update_speeds()
			log_msg = 'stimulus redraw at %f'%(self.session.clock.getTime())
			self.trial.events.append( log_msg )
			if self.session.tracker:
				self.session.tracker.log( log_msg )
			self.redraw=False
			self.session.element_array.setSfs(self.element_sfs)
			self.session.element_array.setSizes(self.element_sizes)
			self.session.element_array.setColors(self.colors)
			self.session.element_array.setOris(self.element_orientations)
	
		if self.frames % 15 == 0:
			self.redraw = True
		self.frames += 1

		self.session.element_array.setPhases(self.element_speeds * self.phase * self.session.standard_parameters['period'] + self.element_phases)

		# if self.frames % 3 == 0:
			# self.redraw = True
		self.frames += 1

		self.session.element_array.draw()		
		self.session.fixation_outer_rim.draw()
		self.session.fixation_rim.draw()
		self.session.fixation.draw()
		self.session.mask_stim.draw()
		
		