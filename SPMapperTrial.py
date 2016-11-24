from __future__ import division
from psychopy import visual, core, misc, event
import numpy#for maths on arrays
from numpy.random import random, shuffle #we only need these two commands from this lib
# from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

from Trial import *

class SPMapperTrial(Trial):
    def __init__(self, parameters = {}, phase_durations = [], session = None, screen = None, tracker = None):
        super(SPMapperTrial, self).__init__(parameters = parameters, phase_durations = phase_durations, session = session, screen = screen, tracker = tracker)
                
        this_instruction_string = 'follow the dot'# self.parameters['task_instruction']
        self.instruction = visual.TextStim(self.screen, 
		    text = this_instruction_string, 
		    font = 'Helvetica Neue',
		    pos = (0, 0),
		    italic = True, 
			height = 30, 
			alignHoriz = 'center',
			color=self.session.stim_color)
        self.instruction.setSize((1200,50))

        self.run_time = 0.0
        self.instruct_time = self.t_time=self.fix_time = self.stimulus_time = self.post_stimulus_time = 0.0

        
    def update_fix_pos(self,time,frequency=0.5):

        # note: this loop takes in extreme cases 1 ms, but median is 0.0004 ms. 
        amplitude = self.parameters['sp_path_amplitude']*self.session.pixels_per_degree/2# * self.screen.size[0] /2
        f = self.parameters['sp_path_temporal_frequency']/self.parameters['TR']
        # f = frequency/self.parameters['TR']
        x_pos = amplitude * np.sin(2*np.pi*f*time) # costs about 
        y_pos = self.screen.size[1]*self.parameters['sp_path_elevation']-self.screen.size[1]/2
        # self.session.fixation_outer_rim.setPos([x_pos,y_pos])
        # self.session.fixation_rim.setPos([x_pos,y_pos])
        self.session.fixation.setPos([x_pos,y_pos])

    def draw(self):

        """docstring for draw"""

        # the position of the dot is determined based
        # on the session time
        if (self.phase == 0) * (self.ID == 0):
            draw_time = 0         
        else:
            draw_time = self.session.clock.getTime() - self.session.start_time

        self.update_fix_pos(draw_time)
        # self.session.fixation_outer_rim.draw()
        # self.session.fixation_rim.draw()
        self.session.fixation.draw()

        # draw additional stimuli:
        if (self.phase == 0 ) * (self.ID == 0):
                self.instruction.draw()

        super(SPMapperTrial, self).draw() # flip

    def event(self):
        for ev in event.getKeys():
            if len(ev) > 0:
                if ev in ['esc', 'escape', 'q']:
                    # self.events.append([-99,self.session.clock.getTime()-self.start_time])
                    self.stopped = True
                    self.session.stopped = True
                    print 'run canceled by user'
                # it handles both numeric and lettering modes 
                elif ev == 't': # TR pulse
                    # self.events.append([99,self.session.clock.getTime()-self.start_time])
                    if (self.phase == 0) * (self.ID == 0):
                        self.session.start_time = self.session.clock.getTime()
                        self.trial_onset_time = self.session.cumulative_phase_durations[self.ID,0] + self.session.start_time
                        # print 'trial %d start time %.2f'%(self.ID,self.trial_onset_time)
                        self.phase_forward()
                # elif ev in self.session.response_button_signs.keys():
                #     log_msg = 'trial ' + str(self.ID) + ' key: ' + str(ev) + ' at time: ' + str(self.session.clock.getTime())
                #     # first check, do we even need an answer?
                #     self.events.append( log_msg )
                #     if self.session.tracker:
                #         self.session.tracker.log( log_msg )

                log_msg = 'trial ' + str(self.ID) + ' key: ' + str(ev) + ' at time: ' + str(self.session.clock.getTime())
                print log_msg
                # add to tracker log
                if self.session.tracker:
                    self.session.tracker.log( log_msg )                
                # add to self.events for adding to behavioral pickle
                self.events.append(log_msg)
        
            super(SPMapperTrial, self).key_event( ev )

    def run(self, ID = 0):
        self.ID = ID
        super(SPMapperTrial, self).run()

        fp_y = self.screen.size[1]*self.parameters['sp_path_elevation']-self.screen.size[1]/2

        # we are fascists on timing issues
        if self.ID != 0:
            self.trial_onset_time = self.session.cumulative_phase_durations[self.ID,0] + self.session.start_time
            # print 'session cumsum %.2f'%self.session.cumulative_phase_durations[self.ID,0]
            # print 'session start time %.2f'%self.session.start_time
            # print 'trial %d start time %.2f'%(self.ID,self.trial_onset_time)

        while not self.stopped:
            # Only in trial 1, phase 0 represents the instruction period.
            # After the first trial, this phase is skipped immediately
            if (self.phase == 0) * (self.ID != 0):
                self.phase_forward()
            if self.phase == 1:
                self.phase_1_time = self.session.clock.getTime()
                if ( self.phase_1_time  - self.trial_onset_time ) > self.phase_durations[1]:
                   self.stopped = True

            # events and draw
            self.event()
            self.draw()
    
        self.stop()
        
