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

class SPTrial(Trial):
    def __init__(self, parameters = {}, phase_durations = [], session = None, screen = None, tracker = None):
        super(SPTrial, self).__init__(parameters = parameters, phase_durations = phase_durations, session = session, screen = screen, tracker = tracker)
                
        this_instruction_string = '\t\t\t\t  Left\t\t/\tRight:\n\nColor\t\t-\tBY\t\t\t/\tRG'# self.parameters['task_instruction']
        self.instruction = visual.TextStim(self.screen, text = this_instruction_string, font = 'Helvetica Neue', pos = (0, 0), italic = True, height = 30, alignHoriz = 'center')
        self.instruction.setSize((1200,50))

        self.run_time = 0.0
        self.instruct_time = self.t_time=self.fix_time = self.stimulus_time = self.post_stimulus_time = 0.0

        self.stim1_drawn = False
        self.stim2_drawn = False
        
    def update_fix_pos(self,time,frequency=0.5):
        amplitude = self.parameters['sp_amplitude'] * self.screen.size[0] /2
        f = frequency/self.parameters['TR']
        x_pos = amplitude * np.sin(2*np.pi*f*time)# + self.screen.size[0]/2
        self.session.fixation_outer_rim.setPos([x_pos,self.screen.size[1]/2*self.parameters['sp_path_elevation']])
        self.session.fixation_rim.setPos([x_pos,self.screen.size[1]/2*self.parameters['sp_path_elevation']])
        self.session.fixation.setPos([x_pos,self.screen.size[1]/2*self.parameters['sp_path_elevation']])

    def draw(self):
        """docstring for draw"""

        # the position of the dot is determined based
        # on the session time
        if (self.phase == 0) * (self.ID == 0):
            draw_time = 0         
        else:
            draw_time = self.session.clock.getTime() - self.session.start_time

        self.update_fix_pos(draw_time)
        self.session.fixation_outer_rim.draw()
        self.session.fixation_rim.draw()
        self.session.fixation.draw()

        # draw additional stimuli:
        if (self.phase == 0 ) * (self.ID == 0):
                self.instruction.draw()
        # phase 2 starts with the presentation of the first stimulus
        elif self.phase == 2:
            if self.stim1_drawn == False:
                # print 'trial %d draw time %.2f'%(self.ID,draw_time)
                self.session.test_stim_1.draw()
                self.stim1_drawn = True
        # phase 3 starts with the presentation of the second stimulus
        elif self.phase == 3:
            if self.stim2_drawn == False:
                # print 'trial %d draw time %.2f'%(self.ID,draw_time)
                self.session.test_stim_2.draw()
                self.stim2_drawn = True    

        super(SPTrial, self).draw()

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
                #     # if self.phase == 0:
                #         # self.phase_forward()
                #     # first check, do we even need an answer?
                #     if self.phase == 3:
                #         if self.stim.last_sampled_staircase != None:
                #             # what value were we presenting at?
                #             test_value = self.session.staircases[self.stim.last_sampled_staircase].quantile()
                #             if self.session.tasks[self.parameters['task_index']] == 'Color':
                #                 response = self.session.response_button_signs[ev]*self.stim.present_color_task_sign
                #             elif self.session.tasks[self.parameters['task_index']] == 'Speed':
                #                 response = self.session.response_button_signs[ev]*self.stim.present_speed_task_sign
                #             elif self.session.tasks[self.parameters['task_index']] == 'Fix':
                #                 response = self.session.response_button_signs[ev]*self.stim.present_fix_task_sign
                #             elif self.session.tasks[self.parameters['task_index']] == 'Fix_no_stim':
                #                 response = self.session.response_button_signs[ev]*self.stim.present_fns_task_sign

                #             # update the staircase
                #             self.session.staircases[self.stim.last_sampled_staircase].update(test_value,(response+1)/2)
                #             # now block the possibility of further updates
                #             self.stim.last_sampled_staircase = None

                #             if self.session.tasks[self.parameters['task_index']] != 'Fix_no_stim':
                #                 log_msg = 'staircase %s bin %d updated from %f after response %s at %f'%( self.session.tasks[self.parameters['task_index']], self.stim.eccentricity_bin,test_value, str((response+1)/2), self.session.clock.getTime() )
                #             else:
                #                 log_msg = 'staircase %s updated from %f after response %s at %f'%( self.session.tasks[self.parameters['task_index']], test_value, str((response+1)/2), self.session.clock.getTime() )

                #             self.events.append( log_msg )
                #             print log_msg
                #             if self.session.tracker:
                #                 self.session.tracker.log( log_msg )



                # add answers based on stimulus changes, and interact with the staircases at hand
                # elif ev == 'b' or ev == 'right': # answer pulse
                event_msg = 'trial ' + str(self.ID) + ' key: ' + str(ev) + ' at time: ' + str(self.session.clock.getTime())
                self.events.append(event_msg)
        
            super(SPTrial, self).key_event( ev )

    def run(self, ID = 0):
        self.ID = ID
        super(SPTrial, self).run()

        x_pos_1 = self.parameters['x_pos_1']*self.session.pixels_per_degree
        y_pos_1 = self.screen.size[1]/2*self.parameters['sp_path_elevation'] + self.parameters['y_order']*self.parameters['test_stim_y_offset']*self.session.pixels_per_degree
        self.session.test_stim_1.setPos([x_pos_1,y_pos_1 ])

        x_pos_2 = self.parameters['x_pos_2']*self.session.pixels_per_degree
        y_pos_2 = self.screen.size[1]/2*self.parameters['sp_path_elevation'] - self.parameters['y_order']*self.parameters['test_stim_y_offset']*self.session.pixels_per_degree
        self.session.test_stim_2.setPos([x_pos_2,y_pos_2 ])

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
            # determine run_time 
            # phase 1 is the smooth pursuit 'rest period'
            if self.phase == 1:
                self.phase_1_time = self.session.clock.getTime()
                if ( self.phase_1_time  - self.trial_onset_time ) > self.phase_durations[1]:
                # if self.session.clock.getTime() > (self.session.cumulative_phase_durations[self.ID,1] + self.session.start_time):
                    # print 'trial %d phase 1 end time %.2f'%(self.ID,self.session.clock.getTime() - self.session.start_time)
                    # print 'trial %d:\n phase_dur: %.2f\nphase 1 end time %.2f\ncum :%.2f'%(self.ID,self.phase_durations[1], self.phase_1_time  - self.trial_onset_time, self.session.cumulative_phase_durations[self.ID,0])
                    self.phase_forward()
            # phase 2 starts with the presentation of the first stimulus
            if self.phase == 2:
                self.phase_2_time = self.session.clock.getTime()
                if ( self.phase_2_time  - self.phase_1_time ) > self.phase_durations[2]:
                    # print 'trial %d:\n phase_dur: %.2f\nphase 2 end time %.2f\ncum :%.2f'%(self.ID,self.phase_durations[2],self.phase_2_time  - self.phase_1_time , self.session.cumulative_phase_durations[self.ID,1])
                    self.phase_forward()
            # phase 3 starts with the presentation of the second stimulus
            if self.phase == 3:
                self.phase_3_time = self.session.clock.getTime()
                if ( self.phase_3_time  - self.phase_2_time ) > self.phase_durations[3]:
                    # print 'trial %d:\n phase_dur: %.2f\nphase 3 end time %.2f\ncum :%.2f'%(self.ID,self.phase_durations[3],self.phase_3_time  - self.phase_2_time , self.session.cumulative_phase_durations[self.ID,2])
                    self.stopped = True

            # events and draw
            self.event()
            self.draw()
    
        self.stop()
        