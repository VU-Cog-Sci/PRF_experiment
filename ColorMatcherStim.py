from __future__ import division
from psychopy import visual, core, misc, event, filters
import numpy as np
from scipy.signal import convolve2d
from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


class ColorMatcherStim(object):
	def __init__(self, screen, trial, session, num_elements = 2000, RG_offset=0):
		# parameters
		self.num_elements = num_elements
		self.trial = trial
		self.session = session
		self.screen = screen
		self.size_pix_hor = session.standard_parameters['horizontal_stim_size'] * session.screen_pix_size[0]
		self.size_pix_ver = session.standard_parameters['vertical_stim_size'] * session.screen_pix_size[1]

		self.RG_offset = RG_offset
		self.redraw = True
		
		# psychopy stimuli
		self.populate_stimulus()

		self.frames = 0

		# make this stimulus array a session variable, in order to have to create it only once...
		if not hasattr(session, 'element_array'):
			self.session.element_array = visual.ElementArrayStim(screen, nElements = self.num_elements, sizes = self.element_sizes, sfs = self.element_sfs, xys = self.element_positions, colors = self.colors, colorSpace = 'rgb') 

	def populate_stimulus(self):

		self.color_value = np.min([np.max([0,self.RG_offset + self.trial.color_diff]), 1])

		red = np.array([ self.color_value, - self.color_value,0]) 
		green = np.array([- self.color_value, self.color_value,0]) 
		yellow = np.array([ self.trial.parameters['BY_comparison_color'], self.trial.parameters['BY_comparison_color'],- self.trial.parameters['BY_comparison_color']])
		blue = np.array([- self.trial.parameters['BY_comparison_color'],- self.trial.parameters['BY_comparison_color'], self.trial.parameters['BY_comparison_color']]) 

		# Now set the actual stimulus parameters
		self.colors = np.concatenate((np.ones((self.num_elements/4.0,3)) * red,  # red/green - red
									np.ones((self.num_elements/4.0,3)) * green,  # red/green - green
									np.ones((self.num_elements/4.0,3)) * blue,  # blue/yellow - blue
									np.ones((self.num_elements/4.0,3)) * yellow))  # blue/yellow - yellow

		np.random.shuffle(self.colors)
		self.element_positions = np.random.rand(self.num_elements, 2) * np.array([self.size_pix_hor, self.size_pix_ver]) - np.array([self.size_pix_hor/2.0, self.size_pix_ver/2.0])
		self.element_sfs = np.random.rand(self.num_elements)*5+0.5
		self.element_sizes = np.ones((self.num_elements)) * self.trial.parameters['element_size']
		self.element_orientations = np.random.rand(self.num_elements) * 720.0 - 360.0
		
	
	def draw(self):

		if self.redraw:
			self.populate_stimulus()
			self.session.element_array.setSfs(self.element_sfs)
			self.session.element_array.setSizes(self.element_sizes)
			self.session.element_array.setColors(self.colors)
			self.session.element_array.setOris(self.element_orientations)
			log_msg = 'stimulus redraw at %f'%(self.session.clock.getTime())
			self.trial.events.append( log_msg )
			if self.session.tracker:
				self.session.tracker.log( log_msg )
			self.redraw=False

		if self.frames % 3 == 0:
			self.redraw = True
		self.frames += 1

		self.session.element_array.draw()		
		self.session.fixation_outer_rim.draw()
		self.session.fixation_rim.draw()
		self.session.fixation.draw()
		self.session.mask_stim.draw()
		
		