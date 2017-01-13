from __future__ import division
from psychopy import visual, core, misc, event
import numpy#for maths on arrays
from numpy.random import random, shuffle #we only need these two commands from this lib
# from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )

from ColorMatcherStim import *
from Trial import *

class ColorMatcherTrial(Trial):
    def __init__(self, parameters = {}, phase_durations = [], session = None, screen = None, tracker = None):
        super(ColorMatcherTrial, self).__init__(parameters = parameters, phase_durations = phase_durations, session = session, screen = screen, tracker = tracker)
        self.color_diff = 0.0

        self.stim = ColorMatcherStim(self.screen, self, self.session, 
                        num_elements = self.parameters['num_elements'] * (1/self.parameters['bar_width_ratio']), 
                        RG_offset = self.parameters['RG_offset'])
        
        this_instruction_string = '\tLeft\t\t/\tRight\n\nLess RG\t\t/\tMore RG'# self.parameters['task_instruction']
        self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, 0), italic = True, height = 30, alignHoriz = 'center')
        self.instruction.setSize((1200,50))

        self.run_time = 0.0
        self.instruct_time = self.fix_time = self.stimulus_time = self.post_stimulus_time = 0.0
    
    def draw(self):
        """docstring for draw"""

        if self.phase == 0:
            if self.ID == 0:
                self.instruction.draw()
            else:
                self.session.fixation_outer_rim.draw()
                self.session.fixation_rim.draw()
                self.session.fixation.draw()
        if self.phase == 1:
            self.session.fixation_outer_rim.draw()
            self.session.fixation_rim.draw()
            self.session.fixation.draw()

        elif self.phase == 2:
            self.session.fixation_outer_rim.draw()
            self.session.fixation_rim.draw()
            self.session.fixation.draw()
            
        elif self.phase == 3:

            self.session.fixation_outer_rim.draw()
            self.session.fixation_rim.draw()
            self.session.fixation.draw()
            self.stim.draw()
        
        elif self.phase == 4:
            self.session.fixation_outer_rim.draw()
            self.session.fixation_rim.draw()
            self.session.fixation.setColor((0,0,0))
            self.session.fixation.draw()
            
        super(ColorMatcherTrial, self).draw( )

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
                elif ev in self.session.response_button_signs.keys():
                    if self.phase == 3:
                        if self.session.response_button_signs[ev] == -1:
                            self.color_diff -= self.session.color_step
                            self.stim.redraw=True
                        elif self.session.response_button_signs[ev] == 1:
                            self.color_diff += self.session.color_step
                            self.stim.redraw=True
                        elif self.session.response_button_signs[ev] == 2:
                            self.phase_forward()
            
            super(ColorMatcherTrial, self).key_event( ev )


    def run(self, ID = 0):
        self.ID = ID
        super(ColorMatcherTrial, self).run()
        
        while not self.stopped:
            self.run_time = self.session.clock.getTime() - self.start_time
            if self.phase == 0:
                self.instruct_time = self.session.clock.getTime()
                if (self.ID != 0) * (self.session.scanner == 'n'):
                    self.phase_forward()
            if self.phase == 1:
                # this trial phase is timed
                self.initial_wait_time = self.session.clock.getTime()
                if ( self.initial_wait_time  - self.instruct_time ) > self.phase_durations[1]:
                    self.phase_forward()
            if self.phase == 2:
                if self.session.exp_start_time == 0.0:
                    self.session.exp_start_time = self.session.clock.getTime()
                self.fix_time = self.session.clock.getTime()

                # this trial phase is timed
                if ( self.fix_time  - self.initial_wait_time ) > self.phase_durations[2]:
                    self.phase_forward()
            if self.phase == 3:
                self.stimulus_time = self.session.clock.getTime()
            if self.phase == 4:
                # this trial phase is timed
                self.session.all_color_values.append(self.stim.color_value)
                self.post_stimulus_time = self.session.clock.getTime()
                if ( self.post_stimulus_time  - self.stimulus_time ) > self.phase_durations[4]:
                    self.stopped = True
        
            # events and draw
            self.event()
            self.draw()
    
        self.stop()
        
