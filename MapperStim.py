from __future__ import division
from psychopy import visual, core, misc, event, filters
import numpy as np
from scipy.signal import convolve2d
from IPython import embed as shell
from math import *
import random, sys
import colorsys
sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


class MapperStim(object):
	def __init__(self, screen, trial, session,task):
		# parameters
		self.num_elements = session.standard_parameters['num_elements'] * (1/session.standard_parameters['bar_width_ratio'])
		self.trial = trial
		self.session = session
		self.screen = screen
		self.size_pix = session.standard_parameters['max_ecc'] * self.session.pixels_per_degree * 2
		self.period = session.standard_parameters['mapper_stim_in_TR'] * session.standard_parameters['TR']
		# self.refresh_frequency = refresh_frequency
		self.task_rate = session.standard_parameters['task_rate']
		self.task = task
		self.refresh_frequency = session.standard_parameters['redraws_per_TR'] / session.standard_parameters['TR']

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

		# if self.task == np.where(self.session.tasks=='no_color_no_speed')[0][0]:

		# 	average_color_value = np.mean([self.session.standard_parameters['RG_color'],self.session.standard_parameters['BY_color']])
		# 	red = np.array([-average_color_value,-average_color_value,-average_color_value])
		# 	green = np.array([average_color_value,average_color_value,average_color_value])
		# 	yellow = np.array([-average_color_value,-average_color_value,-average_color_value])
		# 	blue = np.array([average_color_value,average_color_value,average_color_value]) 

		# 	self.slow_speed = 0.0
		# 	self.fast_speed = 0.0

		# elif self.task == np.where(self.session.tasks=='yes_color_no_speed')[0][0]:

		# 	red = np.array([ self.session.standard_parameters['RG_color'],- self.session.standard_parameters['RG_color'],0])
		# 	green = np.array([- self.session.standard_parameters['RG_color'], self.session.standard_parameters['RG_color'],0])
		# 	yellow = np.array([ self.session.standard_parameters['BY_color'], self.session.standard_parameters['BY_color'],- self.session.standard_parameters['BY_color']])
		# 	blue = np.array([- self.session.standard_parameters['BY_color'],- self.session.standard_parameters['BY_color'], self.session.standard_parameters['BY_color']]) 

		# 	self.slow_speed = 0.0
		# 	self.fast_speed = 0.0

		red_c = np.array([ self.session.standard_parameters['RG_color'],- self.session.standard_parameters['RG_color'],0])
		green_c = np.array([- self.session.standard_parameters['RG_color'], self.session.standard_parameters['RG_color'],0])
		yellow_c = np.array([ self.session.standard_parameters['BY_color'], self.session.standard_parameters['BY_color'],- self.session.standard_parameters['BY_color']])
		blue_c = np.array([- self.session.standard_parameters['BY_color'],- self.session.standard_parameters['BY_color'], self.session.standard_parameters['BY_color']]) 

		red_c2 = (red_c+1)/2
		green_c2 = (green_c+1)/2
		yellow_c2 = (yellow_c+1)/2
		blue_c2 = (blue_c+1)/2

		if self.task == np.where(self.session.tasks=='no_color_yes_speed')[0][0]:


			bw_method = 'retina2'
			if bw_method == 'desaturate':
				red_hsv = colorsys.rgb_to_hsv(red_c2[0],red_c2[1],red_c2[2])
				green_hsv = colorsys.rgb_to_hsv(green_c2[0],green_c2[1],green_c2[2])
				yellow_hsv = colorsys.rgb_to_hsv(yellow_c2[0],yellow_c2[1],yellow_c2[2])
				blue_hsv = colorsys.rgb_to_hsv(blue_c2[0],blue_c2[1],blue_c2[2])

				red = (np.array(colorsys.hsv_to_rgb(red_hsv[0],0,red_hsv[-1]))*2)-1
				green = ((np.array(colorsys.hsv_to_rgb(green_hsv[0],0,green_hsv[-1])))*2)-1
				yellow = ((np.array(colorsys.hsv_to_rgb(yellow_hsv[0],0,yellow_hsv[-1])))*2)-1
				blue = ((np.array(colorsys.hsv_to_rgb(blue_hsv[0],0,blue_hsv[-1])))*2)-1

			elif bw_method == 'old_average':

				average_color_value = np.mean([self.session.standard_parameters['RG_color'],self.session.standard_parameters['BY_color']])
				red = np.array([-average_color_value,-average_color_value,-average_color_value])
				green = np.array([average_color_value,average_color_value,average_color_value])
				yellow = np.array([-average_color_value,-average_color_value,-average_color_value])
				blue = np.array([average_color_value,average_color_value,average_color_value]) 


			elif bw_method == 'average':

				red = np.array([np.average(red_c),np.average(red_c),np.average(red_c)])
				green = np.array([np.average(green_c),np.average(green_c),np.average(green_c)])
				yellow = np.array([np.average(yellow_c),np.average(yellow_c),np.average(yellow_c)])
				blue = np.array([np.average(blue_c),np.average(blue_c),np.average(blue_c)])

			elif bw_method == 'retina':

				c= [0.3,0.59,0.11]
				red = np.array([np.average(red_c,weights=c),np.average(red_c,weights=c),np.average(red_c,weights=c)])
				green = np.array([np.average(green_c,weights=c),np.average(green_c,weights=c),np.average(green_c,weights=c)])
				yellow = np.array([np.average(yellow_c,weights=c),np.average(yellow_c,weights=c),np.average(yellow_c,weights=c)])
				blue = np.array([np.average(blue_c,weights=c),np.average(blue_c,weights=c),np.average(blue_c,weights=c)])

			elif bw_method == 'retina2':

				c = [0.3,0.59,0.11]
				red = (np.array([c[0]*red_c2[0]**2 + c[1]*red_c2[1]**2 + c[2]*red_c2[2]**2]*3)*2)-1
				green = (np.array([c[0]*green_c2[0]**2 + c[1]*green_c2[1]**2 + c[2]*green_c2[2]**2]*3)*2)-1
				yellow = (np.array([c[0]*yellow_c2[0]**2 + c[1]*yellow_c2[1]**2 + c[2]*yellow_c2[2]**2]*3)*2)-1
				blue = (np.array([c[0]*blue_c2[0]**2 + c[1]*blue_c2[1]**2 + c[2]*blue_c2[2]**2]*3)*2)-1
			
			self.fast_speed = 0#self.session.standard_parameters['fast_speed']
			self.slow_speed = 0#self.session.standard_parameters['slow_speed']

		elif self.task == np.where(self.session.tasks=='yes_color_yes_speed')[0][0]:

			red = red_c#np.array([ self.session.standard_parameters['RG_color'],- self.session.standard_parameters['RG_color'],0]) 
			green = green_c#np.array([- self.session.standard_parameters['RG_color'], self.session.standard_parameters['RG_color'],0]) 
			yellow = yellow_c#np.array([ self.session.standard_parameters['BY_color'], self.session.standard_parameters['BY_color'],- self.session.standard_parameters['BY_color']])
			blue = blue_c#np.array([- self.session.standard_parameters['BY_color'],- self.session.standard_parameters['BY_color'], self.session.standard_parameters['BY_color']]) 

			self.fast_speed = 0#self.session.standard_parameters['fast_speed']
			self.slow_speed = 0#self.session.standard_parameters['slow_speed']

		elif self.task == np.where(self.session.tasks=='fix_no_stim')[0][0]:
		
			red,green,yellow,blue = self.session.screen.background_color,self.session.screen.background_color,self.session.screen.background_color,self.session.screen.background_color

			self.slow_speed = 0.0
			self.fast_speed = 0.0

		# Now set the actual stimulus parameters
		self.colors = np.concatenate((np.ones((self.num_elements/4.0,3)) * red,  # red/green - red
									np.ones((self.num_elements/4.0,3)) * green,  # red/green - green
									np.ones((self.num_elements/4.0,3)) * blue,  # blue/yellow - blue
									np.ones((self.num_elements/4.0,3)) * yellow))  # blue/yellow - yellow
		np.random.shuffle(self.colors)
		self.element_positions = np.random.rand(self.num_elements, 2) * np.array([self.size_pix, self.size_pix]) - np.array([self.size_pix/2.0, (self.size_pix)/2.0])
		np.random.shuffle(self.element_positions)

		self.element_speeds = np.concatenate((np.ones(np.round(self.num_elements*self.session.fast_ratio)) * self.fast_speed,
											np.ones(np.round(self.num_elements*self.session.slow_ratio)) * self.slow_speed))
		np.random.shuffle(self.element_speeds)

		sf_mean = self.session.standard_parameters['element_sf_mean'] #* self.session.pixels_per_degree
		sf_min = self.session.standard_parameters['element_sf_min'] #* self.session.pixels_per_degree
		self.element_sfs = np.random.rand(self.num_elements)*sf_mean+sf_min
		self.element_sizes = np.ones((self.num_elements)) * self.session.standard_parameters['element_size'] * self.session.pixels_per_degree
		self.element_phases = np.zeros(self.num_elements)
		self.element_orientations = np.random.rand(self.num_elements) * 720.0 - 360.0
		
	
	def draw(self, phase = 0):
		self.phase = phase
		self.frames += 1

		if self.frames == 1:
		# if self.redraws < (self.phase * self.period * self.refresh_frequency):
			self.redraws = self.redraws + 1
			# self.populate_stimulus()
			self.session.element_array.setSfs(self.element_sfs)
			self.session.element_array.setSizes(self.element_sizes)
			self.session.element_array.setColors(self.colors)
			self.session.element_array.setOris(self.element_orientations)
			self.session.element_array.setXYs(np.array(np.matrix(self.element_positions))) 
			log_msg = 'stimulus draw for phase %f, at %f'%(phase, self.session.clock.getTime())
			self.trial.events.append( log_msg )
			if self.session.tracker:
				self.session.tracker.log( log_msg )

			
		# if fmod(self.phase * self.period * self.refresh_frequency, 1.0) > 0.5: 
		self.session.element_array.setPhases(self.element_speeds * self.phase * self.period + self.element_phases)

		if self.session.tasks[self.task] != 'fix_no_stim':
			self.session.element_array.draw()	
		self.session.fixation_outer_rim.draw()
		self.session.fixation_rim.draw()
		self.session.fixation.draw()
		self.session.mask_stim.draw()
		
		