from psychopy import visual, core, misc, event
import numpy#for maths on arrays
from numpy.random import random, shuffle #we only need these two commands from this lib
# from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

from PRFStim import *
from Trial import *

class PRFTrial(Trial):
	def __init__(self, parameters = {}, phase_durations = [], session = None, screen = None, tracker = None):
		super(PRFTrial, self).__init__(parameters = parameters, phase_durations = phase_durations, session = session, screen = screen, tracker = tracker)
		
		self.stim = PRFStim(self.screen, self, self.session, 
						size_pix = self.parameters['stim_size'] * session.screen_pix_size[1], 
						num_elements = self.parameters['num_elements'], 
						bar_width_ratio = self.parameters['bar_width_ratio'], 
						orientation = self.parameters['orientation'], 
						period = self.parameters['period'], 
						refresh_frequency = self.parameters['refresh_frequency'], 
						task_rate = self.parameters['task_rate'])
		
		this_instruction_string = 'keep fixation'# self.parameters['task_instruction']
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0.0, 30.0), italic = True, height = 30)
		
		self.run_time = 0.0
		self.instruct_time = self.fix_time = self.stimulus_time = self.post_stimulus_time = 0.0
		self.instruct_sound_played = False

		self.response_button_signs = {'b':-1, 'g':1}
		
	
	def draw(self):
		"""docstring for draw"""
		if self.phase == 0:
			self.session.fixation_rim.draw()
			self.session.fixation.draw()
			if self.ID == 0:
				self.instruction.draw()
		
		elif self.phase == 1:
			self.session.fixation_rim.draw()
			self.session.fixation.draw()
			
		elif self.phase == 2:
			self.stim.draw(phase = (self.stimulus_time - self.fix_time) / self.phase_durations[2])
		
		elif self.phase == 3:
			self.session.fixation_rim.draw()
			self.session.fixation.setColor((0,0,0))
			self.session.fixation.draw()
			
		super(PRFTrial, self).draw( )

	def event(self):
		for ev in event.getKeys():
			if len(ev) > 0:
				if ev in ['esc', 'escape', 'q']:
					self.events.append([-99,self.session.clock.getTime()-self.start_time])
					self.stopped = True
					self.session.stopped = True
					print 'run canceled by user'
				# it handles both numeric and lettering modes 
				elif ev == ' ':
					self.events.append([0,self.session.clock.getTime()-self.start_time])
					if self.phase == 0:
						self.phase_forward()
					else:
						self.events.append([-99,self.session.clock.getTime()-self.start_time])
						self.stopped = True
						print 'trial canceled by user'
				elif ev == 't': # TR pulse
					self.events.append([99,self.session.clock.getTime()-self.start_time])
					if self.phase == 0:
						self.phase_forward()
				elif ev in self.response_button_signs:
					# first check, do we even need an answer?
					if self.stim.last_sampled_staircase != None:
						# what value were we presenting at?
						test_value = self.session.staircases[self.stim.last_sampled_staircase].quantile()
						if self.session.unique_tasks[self.parameters['unique_task']] == 'Color':
							response = self.response_button_signs[ev]*self.stim.present_color_task_sign
						elif self.session.unique_tasks[self.parameters['unique_task']] == 'Speed':
							response = self.response_button_signs[ev]*self.stim.present_speed_task_sign
						elif self.session.unique_tasks[self.parameters['unique_task']] == 'Fix':
							response = self.response_button_signs[ev]*self.stim.present_fix_task_sign

						print str(self.session.staircases[self.session.unique_tasks[self.parameters['unique_task']] + '_%i'%self.stim.eccentricity_bin]) + ' response ' + str((response+1)/2) + 'updated at ' + str(test_value)
						self.session.staircases[self.stim.last_sampled_staircase].update(test_value,(response+1)/2)

						# now block teh possibility of further updates
						self.stim.last_sampled_staircase = None


				# add answers based on stimulus changes, and interact with the staircases at hand
				# elif ev == 'b' or ev == 'right': # answer pulse
				self.events.append('trial ' + str(self.ID) + ' key: ' + str(ev) + ' at time: ' + str(self.session.clock.getTime()) + ' for task ' + self.parameters['task'])
				if self.tracker:
					self.tracker.sendMessage( 'trial ' + str(self.ID) + ' key: ' + str(ev) + ' at time: ' + str(self.session.clock.getTime()) + ' for task ' + self.parameters['task'] )
		
			super(PRFTrial, self).key_event( ev )

	def run(self, ID = 0):
		self.ID = ID
		super(PRFTrial, self).run()
		
		while not self.stopped:
			self.run_time = self.session.clock.getTime() - self.start_time
			if self.phase == 0:
				self.instruct_time = self.session.clock.getTime()
			if self.phase == 1:
				self.fix_time = self.session.clock.getTime()

				if not self.instruct_sound_played:
					self.session.play_sound(self.session.unique_tasks[self.parameters['unique_task']].lower())
					self.instruct_sound_played = True

				# this trial phase is timed
				if ( self.fix_time  - self.instruct_time ) > self.phase_durations[1]:
					self.phase_forward()
			if self.phase == 2:
				# this trial phase is timed
				self.stimulus_time = self.session.clock.getTime()
				if ( self.stimulus_time - self.fix_time ) > self.phase_durations[2]:
					self.phase_forward()
			if self.phase == 3:
				# this trial phase is timed
				self.post_stimulus_time = self.session.clock.getTime()
				if ( self.post_stimulus_time  - self.stimulus_time ) > self.phase_durations[3]:
					self.stopped = True
		
			# events and draw
			self.event()
			self.draw()
	
		self.stop()
		