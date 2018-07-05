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
        
        if self.session.task == 'bar':
            this_instruction_string = '\t\t\t\t  Index\t\t/\tMiddle:\n\nColor\t\t-\tBY\t\t\t/\tRG'# self.parameters['task_instruction']
        else:
            this_instruction_string = '\t\t\t\t  Left\t\t/\tRight:\n\nDarker\t\t-\tBrighter\t\t\t\tDarker'# self.parameters['task_instruction']        
        self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, 0), italic = True, height = 30, alignHoriz = 'center')
        self.instruction.setSize((1200,50))

        self.run_time = 0.0
        self.instruct_time = self.t_time=self.fix_time = self.stimulus_time = self.post_stimulus_time = 0.0
        self.instruct_sound_played = False

        
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
            self.stim.draw(phase = np.max([(self.stimulus_time - self.t_time) / self.stim.period,0]))
        elif self.phase == 3:
            self.session.fixation_outer_rim.draw()
            self.session.fixation_rim.draw()
            # self.session.fixation.setColor((0,0,0))
            self.session.fixation.draw()
        super(PRFTrial, self).draw( )

    def event(self):
        for ev in event.getKeys():
            if len(ev) > 0:
                if ev in ['esc', 'escape']:
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
                    if (self.phase == 0) + (self.phase==1):
                        self.phase_forward()
                elif ev in self.session.response_button_signs.keys():
                    if self.phase == 2:
                        # then check whether one of the correct buttons was pressed:
                        if self.session.response_button_signs[ev] in [-1,1]:
                            # do we even need an answer?
                            if self.stim.last_sampled_staircase != None:
                                # what value were we presenting at?
                                if self.session.task == 'bar':
                                    response = self.session.response_button_signs[ev]*self.stim.present_color_task_sign
                                elif self.session.task == 'fix':
                                    response = self.session.response_button_signs[ev]*self.stim.present_fix_task_sign

                                # update the staircase
                                self.session.staircases[self.stim.last_sampled_staircase].answer((response+1)/2)
                                # now block the possibility of further updates
                                self.stim.last_sampled_staircase = None

                                log_msg = 'staircase %s bin %d updated after response %s at %f'%( self.session.task, self.stim.eccentricity_bin, str((response+1)/2), self.session.clock.getTime() )

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
            # In phase 1, we wait for the scanner pulse (t)
            if self.phase == 1:
                self.t_time = self.session.clock.getTime()
                if self.session.scanner == 'n':
                    self.phase_forward()
            # In phase 2, the stimulus is presented
            if self.phase == 2:
                self.stimulus_time = self.session.clock.getTime()
                if ( self.stimulus_time - self.t_time ) > self.stim.period:
                    self.phase_forward()
            # Phase 3 reflects the ITI
            if self.phase == 3:
                self.post_stimulus_time = self.session.clock.getTime()
                if ( self.post_stimulus_time  - self.stimulus_time ) > self.phase_durations[2]:
                    self.stopped = True
        
            # events and draw
            self.event()
            self.draw()
    
        self.stop()
        
