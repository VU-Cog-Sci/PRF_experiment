from __future__ import division
from psychopy import visual, core, misc, event
import numpy#for maths on arrays
from numpy.random import random, shuffle #we only need these two commands from this lib
# from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )

from MapperStim import *
from Trial import *

class MapperTrial(Trial):
	def __init__(self, parameters = {}, phase_durations = [], session = None, screen = None, tracker = None):
		super(MapperTrial, self).__init__(parameters = parameters, phase_durations = phase_durations, session = session, screen = screen, tracker = tracker)
		
		self.stim = MapperStim(self.screen, self, self.session, self.parameters['task'])
		
		this_instruction_string = '\t\t\t\t  Left\t\t/\tRight:\n\nFix\t\t\t-\tBlack\t\t/\tWhite'# self.parameters['task_instruction']
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, 0), italic = True, height = 30, alignHoriz = 'center')
		self.instruction.setSize((1200,50))

		self.run_time = 0.0
		self.instruct_time = self.trial_start_time =self.stimulus_time = self.post_stimulus_time = 0.0
		# self.instruct_sound_played = False

		# set this to its default no-answer necessary value of None - this is tested for in PRFTrial when incorporating responses

	def draw(self):
		"""docstring for draw"""

		# wait with presenting the fixation task after the first trial
		if (self.ID != 0):

			time_elapsed_since_start = self.session.clock.getTime() - self.session.exp_start_time
			# see whether the elapsed time divided in 0.5 second steps is in transient occurences, and whether this pulse has not yet bee presented
			if ((np.round(time_elapsed_since_start * (1/self.session.time_steps))/(1/self.session.time_steps)) in self.session.transient_occurrences) * self.session.ready_for_next_pulse:  

				self.session.ready_for_next_pulse = False
				
				self.session.stim_value = np.random.choice([-1,1])
				self.fix_gray_value = np.ones(3) * self.session.stim_value

				log_msg = 'fix signal value: %d at %f ' % (self.session.stim_value, self.session.clock.getTime())

				self.session.fixation.setColor(self.fix_gray_value)

				if self.session.tracker:
					self.session.tracker.log( log_msg )
				self.events.append( log_msg )
				print log_msg

			elif ((np.round(time_elapsed_since_start * (1/self.session.time_steps))/(1/self.session.time_steps)) not in self.session.transient_occurrences) :
				self.session.ready_for_next_pulse = True
				self.session.fixation.setColor((0,0,0))

		if (self.phase == 0) * (self.ID == 0):
			self.instruction.draw()
			
		elif self.phase == 1:

			self.session.fixation_outer_rim.draw()
			self.session.fixation_rim.draw()
			self.session.fixation.draw()

		elif self.phase == 2:
			self.stim.draw(phase = (self.stimulus_time - self.trial_start_time) / self.phase_durations[2])
			self.session.fixation_outer_rim.draw()
			self.session.fixation_rim.draw()
			self.session.fixation.draw()

		elif self.phase == 3:
			self.session.fixation_outer_rim.draw()
			self.session.fixation_rim.draw()
			self.session.fixation.draw()
			
		super(MapperTrial, self).draw( )

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
					if (self.ID==0) * (self.phase == 0):
						self.session.exp_start_time = self.session.clock.getTime()
						self.phase_forward()
					elif self.session.scanner * (self.phase==2):
						self.phase_forward()
				elif ev in self.session.response_button_signs.keys():
					# then check whether one of the correct buttons was pressed:
					response = self.session.response_button_signs[ev]
					# do we even need a response:
					if self.session.stim_value != 0:
						if response in [-1,1]:

							answer = self.session.response_button_signs[ev]
							log_msg = 'fix value: %d, response: %d, accuracy: %d'%(self.session.stim_value,response,((self.session.stim_value*response)+1)/2)

							self.events.append( log_msg )
							print log_msg
							if self.session.tracker:
								self.session.tracker.log( log_msg )

				event_msg = 'trial ' + str(self.ID) + ' key: ' + str(ev) + ' at time: ' + str(self.session.clock.getTime())
				self.events.append(event_msg)
			
			super(MapperTrial, self).key_event( ev )

	def run(self, ID = 0):
		self.ID = ID
		super(MapperTrial, self).run()
		
		while not self.stopped:
			self.run_time = self.session.clock.getTime() - self.start_time
			# Only in trial 1, phase 0 represents the instruction period.
			# After the first trial, this phase is skipped immediately
			if self.phase == 0:
				self.instruct_time = self.session.clock.getTime()
				if self.ID != 0:
					self.phase_forward()
			# in phase 1, waiting for t if in the scanner
			elif self.phase == 1:
				if self.ID == 0:
					self.session.exp_start_time = self.session.clock.getTime()
				self.trial_start_time = self.session.clock.getTime()
				if self.session.scanner == 'n':
					self.phase_forward()		
			# phase 2 is stimulus presentation phase
			elif self.phase == 2:
				self.stimulus_time = self.session.clock.getTime()
				if ( self.stimulus_time - self.trial_start_time ) > self.phase_durations[2]:
					self.phase_forward()
			# phase 3 is ITI
			elif self.phase == 3:
				self.post_stimulus_time = self.session.clock.getTime()
				if ( self.post_stimulus_time  - self.stimulus_time ) > self.phase_durations[3]:
					self.stopped = True
		
			# events and draw
			self.event()
			self.draw()
	
		self.stop()
		