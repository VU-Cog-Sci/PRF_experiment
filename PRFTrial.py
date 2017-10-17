from __future__ import division
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
		
		self.stim = PRFStim(self.screen, self, self.session, orientation = self.parameters['orientation'])
		
		this_instruction_string = '\t\t\t\t  Left\t\t/\tRight:\n\nColor\t\t-\tBY\t\t\t/\tRG'# self.parameters['task_instruction']
		self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, 0), italic = True, height = 30, alignHoriz = 'center')
		self.instruction.setSize((1200,50))

		self.run_time = 0.0
		self.instruct_time = self.t_time=self.fix_time = self.stimulus_time = self.post_stimulus_time = 0.0
		
	
	def draw(self):
		"""docstring for draw"""


		if not ((self.ID == 0) * (self.phase == 0)):
			
			# wait with presenting the fixation task after the first trial
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

			self.session.fixation_outer_rim.draw()
			self.session.fixation_rim.draw()
			self.session.fixation.draw()

		if self.phase == 0:
			if self.ID == 0:
				self.instruction.draw()

		if self.phase == 3:
			self.stim.draw(phase = np.max([(self.stimulus_time - self.t_time) / self.phase_durations[3],0]))
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
					if (self.ID==0) * (self.phase == 0):
						self.session.exp_start_time = self.session.clock.getTime()
						self.phase_forward()
					elif scanner * (self.phase==2):
						self.phase_forward()
				elif ev in self.session.response_button_signs.keys():
					# if self.phase == 0:
						# self.phase_forward()
					if self.session.stim_value != 0:
						# then check whether one of the correct buttons was pressed:
						response = self.session.response_button_signs[ev]
						if response in [-1,1]:

							answer = self.session.response_button_signs[ev]
							log_msg = 'fix value: %d, response: %d, accuracy: %d'%(self.session.stim_value,response,self.session.stim_value*response)

							self.events.append( log_msg )
							print log_msg
							if self.session.tracker:
								self.session.tracker.log( log_msg )

				event_msg = 'trial ' + str(self.ID) + ' key: ' + str(ev) + ' at time: ' + str(self.session.clock.getTime())
				self.events.append(event_msg)
		
			super(PRFTrial, self).key_event( ev )

	def run(self, ID = 0):
		self.ID = ID
		super(PRFTrial, self).run()
		
		while not self.stopped:
			self.run_time = self.session.clock.getTime() - self.start_time
			# Only in trial 1, phase 0 represents the instruction period.
			# After the first trial, this phase is skipped immediately
			if self.phase == 0:
				self.instruct_time = self.session.clock.getTime()
				if self.ID != 0:
					self.phase_forward()
			# In phase 1, we present the task instruction auditorily
			if self.phase == 1:
				self.fix_time = self.session.clock.getTime()
				if self.ID == 0:#self.session.exp_start_time == 0.0:
					self.session.exp_start_time = self.session.clock.getTime()
				# this trial phase is timed
				if ( self.fix_time  - self.instruct_time ) > self.phase_durations[1]:
					self.phase_forward()
			# In phase 2, we wait for the scanner pulse (t)
			if self.phase == 2:
				self.t_time = self.session.clock.getTime()
				if self.session.scanner == 'n':
					# self.pulse_id = np.random.randint(5)+1
					self.phase_forward()
			# In phase 3, the stimulus is presented
			if self.phase == 3:
				self.stimulus_time = self.session.clock.getTime()
				if ( self.stimulus_time - self.t_time ) > self.phase_durations[3]:
					self.phase_forward()
			# Phase 4 reflects the ITI
			if self.phase == 4:
				self.post_stimulus_time = self.session.clock.getTime()
				if ( self.post_stimulus_time  - self.stimulus_time ) > self.phase_durations[4]:
					self.stopped = True
		
			# events and draw
			self.event()
			self.draw()
	
		self.stop()
		