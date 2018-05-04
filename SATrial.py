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
    def __init__(self, parameters = {}, phase_durations = [], session = None, screen = None, tracker = None):
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

        self.run_time = 0.0
        self.instruct_time = self.t_time=self.fix_time = self.stimulus_time = self.post_stimulus_time = 0.0

        self.stim1_drawn = False

    def set_fix_color(self,time):

        self.session.fixation_left.setColor(self.session.stim_color)       
        self.session.fixation_right.setColor(self.session.stim_color)            
        self.session.fixation_center.setColor(self.session.stim_color)

        # dim center ref
        if (time % self.parameters['TR']) < self.parameters['fp_dim_dur']:
            self.session.fixation_center.setColor((self.session.stim_color[0]*0.2,-1,-1))  

        # this is how i determined stim pos in smooth pursuit
        amplitude = self.parameters['sp_path_amplitude']*self.session.pixels_per_degree/2# * self.screen.size[0] /2
        f = self.parameters['sp_path_temporal_frequency']/self.parameters['TR']
        x_pos = amplitude * np.sin(2*np.pi*f*time) # costs about 
        # so if x_pos is positive, it should be the right target that lights up

        # you know if it's the right one if the 
        if ((time+self.parameters['TR']/2) % (self.parameters['TR'])) < self.parameters['fp_dim_dur']:
            if x_pos > 0:
                self.session.fixation_right.setColor((self.session.stim_color[0]*0.2,-1,-1))
            else:
                self.session.fixation_left.setColor((self.session.stim_color[0]*0.2,-1,-1))


    def draw(self):

        """docstring for draw"""

        if (self.phase == 0) * (self.ID == 0):
            draw_time = 0         
        else:
            draw_time = self.session.clock.getTime() - self.session.start_time

        self.set_fix_color(draw_time)
        self.session.fixation_center.draw()

        self.session.fixation_left.draw()
        self.session.fixation_right.draw()

        # draw additional stimuli:
        if (self.phase == 0 ) * (self.ID == 0):
                self.instruction.draw()
        # phase 2 starts with the presentation of the target stimulus
        elif self.phase == 2:
            if self.stim1_drawn == False:
                # print 'trial %d draw time %.2f'%(self.ID,draw_time)
                self.session.test_stim.draw()
                self.stim1_drawn = True


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
                print log_msg
                # add to tracker log
                if self.session.tracker:
                    self.session.tracker.log( log_msg )                
                # add to self.events for adding to behavioral pickle
                self.events.append(log_msg)
        
            super(SATrial, self).key_event( ev )

    def run(self, ID = 0):

        # shell()
        self.ID = ID
        super(SATrial, self).run()

        fp_y = self.screen.size[1]*self.parameters['sp_path_elevation']-self.screen.size[1]/2
       
        target_y_offset = self.parameters['y_order']*self.parameters['test_stim_y_offset']*self.session.pixels_per_degree
        x_pos = self.parameters['x_pos']*self.session.pixels_per_degree
        y_pos = fp_y + target_y_offset
        self.session.test_stim.setPos([x_pos,y_pos ])

        # eye_dir 1 should be to the left, eye dir 0 to the rigth:
        target_x_pos = int(np.round( (self.parameters['sp_path_amplitude']/2*self.session.pixels_per_degree)*([1,-1][int(self.parameters['eye_dir'])])))
        self.session.saccade_target.setPos([target_x_pos,fp_y])

        leftrefx = int(np.round( (self.parameters['sp_path_amplitude']/2*self.session.pixels_per_degree) * -1))
        rightrefx = int(np.round( (self.parameters['sp_path_amplitude']/2*self.session.pixels_per_degree) ))
        self.session.fixation_left.setPos((leftrefx,fp_y))
        self.session.fixation_right.setPos((rightrefx,fp_y))
        self.session.fixation_center.setPos((0,fp_y))

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

            # only 1 phase in this trial
            if self.phase == 1:
                self.phase_1_time = self.session.clock.getTime()
                if ( self.phase_1_time  - self.trial_onset_time ) > self.phase_durations[1]:
                    self.phase_forward()
            # only 1 phase in this trial
            if self.phase == 2:
                self.phase_2_time = self.session.clock.getTime()
                if ( self.phase_2_time  - self.phase_1_time ) > self.phase_durations[2]:
                    self.stopped = True      
            # events and draw
            self.event()
            self.draw()
    
        self.stop()
        
