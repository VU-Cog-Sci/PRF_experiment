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

class SATrial(Trial):
    def __init__(self, parameters = {}, phase_durations = [], session = None, screen = None, tracker = None,target_stim=None):
        super(SATrial, self).__init__(parameters = parameters, phase_durations = phase_durations, session = session, screen = screen, tracker = tracker)
                
        this_instruction_string = 'Determine where the flash is\n by pressing the corresponding button'
        self.instruction = visual.TextStim(self.screen, 
		    text = this_instruction_string, 
		    font = 'Helvetica Neue',
		    pos = (0, 0),
		    italic = True, 
			height = 30, 
			alignHoriz = 'center',
			color=self.session.stim_color)
        self.instruction.setSize((1200,50))
        self.target_stim=target_stim

        self.run_time = 0.0
        self.instruct_time = self.t_time=self.fix_time = self.stimulus_time = self.post_stimulus_time = 0.0

        self.stim1_drawn = False
        self.saccade_before_target= False

    def draw(self):    
        """docstring for draw"""
        
        self.session.ref_right.draw()
        self.session.ref_left.draw()
        self.session.fixation_center.draw()

        # draw additional stimuli:
        if (self.phase == 0 ) * (self.ID == 0):
                self.instruction.draw()
        
        # cue presentation
        if self.phase in [2,3]:
            if self.parameters['eye_dir'] ==1:
                self.session.saccade_cue_right.draw()
            elif self.parameters['eye_dir'] ==-1:
                self.session.saccade_cue_left.draw()
        
        # target presentation and response window
        if self.phase == 3:
            if self.stim1_drawn == False:
                # print 'eye_dir: %d'%self.parameters['eye_dir']
                # print 'trial %d draw time %.2f'%(self.ID,draw_time)
                self.target_stim.draw()
                self.stim1_drawn = True
        
        if self.phase == 4:
            if self.parameters['eye_dir'] == 1:
                self.session.saccade_cue_back_right.draw()
            elif self.parameters['eye_dir'] == -1:
                self.session.saccade_cue_back_left.draw()

        # if (self.ID == 0):# + (self.phase < 4):


        super(SATrial, self).draw() # flip

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
                else:
                    self.parameters['answer'] = ev

                log_msg = 'trial ' + str(self.ID) + ' key: ' + str(ev) + ' at time: ' + str(self.session.clock.getTime())
                # print log_msg
                # add to tracker log
                if self.session.tracker:
                    self.session.tracker.log( log_msg )                
                # add to self.events for adding to behavioral pickle
                self.events.append(log_msg)
        
            super(SATrial, self).key_event( ev )

    def run(self, ID = 0):

        self.ID = ID
        super(SATrial, self).run()

        # we are fascists on timing issues
        if self.ID != 0:
            self.trial_onset_time = self.session.cumulative_phase_durations[self.ID,0] + self.session.start_time

        while not self.stopped:
            # Only in trial 1, phase 0 represents the instruction period.
            # After the first trial, this phase is skipped immediately
            if (self.phase == 0) * (self.ID != 0):
                self.phase_forward()
            if self.phase == 1:
                self.phase_1_time = self.session.clock.getTime()
                if ( self.phase_1_time  - self.trial_onset_time ) > self.phase_durations[1]:
                    self.phase_forward()
            if self.phase == 2:
                self.phase_2_time = self.session.clock.getTime()
                if ( self.phase_2_time  - self.phase_1_time ) > self.phase_durations[2]:
                    self.phase_forward()
            if self.phase == 3:
                self.phase_3_time = self.session.clock.getTime()
                if ( self.phase_3_time  - self.phase_2_time ) > self.phase_durations[3]:
                    self.phase_forward()
            if self.phase == 4:
                self.phase_4_time = self.session.clock.getTime()
                if ( self.phase_4_time  - self.phase_3_time ) > self.phase_durations[4]:
            #         self.phase_forward()
            # if self.phase == 5:
            #     self.phase_5_time = self.session.clock.getTime()
            #     if ( self.phase_5_time  - self.phase_4_time ) > self.phase_durations[5]:
                    self.stopped = True      
            # events and draw
            self.event()
            self.draw()
    
        self.stop()
        
