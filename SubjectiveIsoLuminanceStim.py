from psychopy import visual, core, misc, event, filters
import numpy as np
from scipy.signal import convolve2d
from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


class SubjectiveIsoLuminanceStim(object):
	def __init__(self, screen, trial, session, size = 1, RG_offset = 0, BY_offset = 0):
		# parameters
		self.trial = trial
		self.session = session
		self.screen = screen

		# bookkeeping variables
		self.frames = 0
			
		# psychopy stimuli
		# self.populate_stimulus()

		self.BY_offset = BY_offset
		self.RG_offset = RG_offset

		# make this stimulus array a session variable, in order to have to create it only once...
		self.gabor = visual.GratingStim(screen,tex='sin', mask='gauss', texRes = 2048)
		self.gabor.size = size
		self.gabor.sf = 0.01


	def populate_stimulus(self,which_stim):

		if which_stim == 'RG':

			self.RG_offset = 0.5
			color_value = np.max([np.max([0.1,self.RG_offset-self.trial.RG_diff]), 1])
			self.color = np.array([color_value,-color_value,0])


			self.orientation = 90

		elif which_stim == 'BY':

			self.BY_offset = 0.5
			color_value = np.max([np.max([0.1,self.BY_offset-self.trial.BY_diff]), 1])
			self.color = np.array([color_value,color_value,-color_value])
	
			self.orientation = 0


	def draw(self):

		self.frames += 1
		if np.mod(self.frames,self.trial.parameters['redraws_per_stim'])==1:
			self.populate_stimulus(which_stim = 'RG')
		elif np.mod(self.frames,self.trial.parameters['redraws_per_stim'])==((self.trial.parameters['redraws_per_stim']/2)+1):
			self.populate_stimulus(which_stim = 'BY')

			# self.gabor.setColor(np.vstack([self.color_1,self.color_2]))
		self.gabor.color = self.color
		self.gabor.ori = self.orientation

		self.gabor.draw()		

		
		