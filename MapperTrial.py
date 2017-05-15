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

class MapperTrial(Trial):
    def __init__(self, parameters = {}, phase_durations = [], session = None, screen = None, tracker = None):
        super(MapperTrial, self).__init__(parameters = parameters, phase_durations = phase_durations, session = session, screen = screen, tracker = tracker)
                
        this_instruction_string = 'CW: R - CCW: L'
        self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, 0), italic = True, height = 50, alignHoriz = 'center')
        self.instruction.setSize((200,50))

        self.run_time = 0.0
        self.instruct_time = self.trial_start_time =self.stimulus_time = self.post_stimulus_time = 0.0

        # set this to its default no-answer necessary value of None - this is tested for in PRFTrial when incorporating responses

    def draw(self):
        """docstring for draw"""

        if (self.phase == 0) * (self.ID == 0):
            self.instruction.draw()

        elif self.phase == 2:
            grating_phase = 0.5 * np.round(self.stimulus_time * \
                                self.parameters['stim_flicker_freq'])
            self.session.CW_stim.setPhase(grating_phase)
            self.session.CCW_stim.setPhase(grating_phase)

            self.session.CW_stim.draw()
            self.session.CCW_stim.draw()

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
                    if (self.phase == 0) and self.ID == 0:
                        self.phase_forward()
                elif ev == 't': # TR pulse
                    self.events.append([99,self.session.clock.getTime()-self.start_time])
                    if (self.phase == 0) and self.ID == 0:
                        self.phase_forward()
                elif ev in self.session.response_button_signs.keys():
                   # do we even need an answer?
                    self.parameters['rt'] = self.session.clock.getTime() - self.stimulus_time
                    self.parameters['answer'] = self.session.response_button_signs[ev]
                    self.parameters['correct'] = self.parameters['HR_location'] * self.parameters['answer']
                    if self.parameters['correct'] == 1:
                        if self.parameters['feedback_if_HR_chosen'] == 1:
                            self.session.fixation.setColor((0,1,0))
                            self.parameters['reward'] = 1
                        else:
                            self.session.fixation.setColor((1,0,0))
                            self.parameters['reward'] = -1
                    elif self.parameters['correct'] == -1:
                        if self.parameters['feedback_if_HR_chosen'] == 1:
                            self.session.fixation.setColor((1,0,0))
                            self.parameters['reward'] = -1
                        else:
                            self.session.fixation.setColor((0,1,0))
                            self.parameters['reward'] = 1

                    # add answers based on stimulus changes, and interact with the staircases at hand
                    # elif ev == 'b' or ev == 'right': # answer pulse
                    event_msg = 'trial ' + str(self.ID) + ' key: ' + str(ev) + ' at time: ' + str(self.session.clock.getTime())
                    self.events.append(event_msg)
                    print event_msg
                    print self.parameters['correct'], self.parameters['answer'], self.parameters['feedback_if_HR_chosen']
            
            super(MapperTrial, self).key_event( ev )

    def run(self, ID = 0):
        self.ID = ID
        super(MapperTrial, self).run()

        # set locations of oriented gratings here.
        self.session.CW_stim.setPos([self.parameters['position_CW'], 0])
        self.session.CCW_stim.setPos([self.parameters['position_CCW'], 0])
        self.session.fixation.setColor((0,0,0))

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
                self.trial_start_time = self.session.clock.getTime()
                if ( self.trial_start_time - self.instruct_time ) > self.phase_durations[1]:
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
                if ( self.post_stimulus_time  - self.stimulus_time ) > self.session.standard_parameters['fb_dur']:
                    self.session.fixation.setColor((0,0,0))
        
            # events and draw
            self.event()
            self.draw()
    
        self.stop()
        
