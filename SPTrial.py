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
        
    def update_fix_pos(self,time):#0.5):

        # note: this loop takes in extreme cases 1 ms, but median is 0.0004 ms. 
        # self.freq f = self.parameters['sp_path_temporal_frequency']#/self.parameters['TR']
        # f = frequency/self.parameters['TR']
        # y_pos = self.screen.size[1]*self.parameters['sp_path_elevation']-self.screen.size[1]/2
        # self.session.fixation_outer_rim.setPos([x_pos,y_pos])
        # self.session.fixation_rim.setPos([x_pos,y_pos])

        if self.parameters['sp_type'] == 0:
            x_pos = self.session.sp_amplitude_pix * np.sin(2*np.pi* self.parameters['sp_path_temporal_frequency']*time) # costs about 
        elif self.parameters['sp_type'] == 1:
            phase = ((time-self.session.sp_cycle_time/4)/(self.session.sp_cycle_time/2))%1
            sign = (int(((time-self.session.sp_cycle_time/4)/(self.session.sp_cycle_time/2))%2<1)*2)-1
            x_pos = sign * self.session.sp_amplitude_pix + -sign*phase*self.session.sp_amplitude_pix*2 # costs about 
        
        return x_pos
        
    def draw(self):

        """docstring for draw"""


        if self.parameters['window']:
            self.session.ref_line.draw()

        # the position of the dot is determined based
        # on the session time
        if (self.phase == 0) * (self.ID == 0):
            draw_time = 0         
        else:
            draw_time = self.session.clock.getTime() - self.session.start_time

        if not self.parameters['fixate']:
            fix_x =self.update_fix_pos(draw_time)
        else:
            fix_x = 0

        self.session.fixation.setPos([fix_x,self.fp_y])
        # if self.parameters['moving_window']:
        #     self.session.ref_right.setPos([self.max_x+fix_x,self.fp_y])
        #     self.session.ref_left.setPos([-self.max_x+fix_x,self.fp_y])

        # if self.parameters['window'] + self.parameters['fixate']:
        #     self.session.ref_left.draw()
        #     self.session.ref_right.draw()

        # self.session.fixation_outer_rim.draw()
        # self.session.fixation_rim.draw()
        self.session.fixation.draw()

        # draw additional stimuli:
        if (self.phase == 0 ) * (self.ID == 0):
                self.instruction.draw()
        # phase 2 starts with the presentation of the target stimulus
        elif self.phase == 1:
            if self.stim1_drawn == False:
                print 'eye dir: %d'%self.parameters['eye_dir']
                # print 'trial %d draw time %.2f'%(self.ID,draw_time)
                self.session.test_stim.draw()
                self.stim1_drawn = True

        super(SPTrial, self).draw() # flip

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
                        self.phase_forward()
                else:
                    self.parameters['answer'] = ev

                log_msg = 'trial ' + str(self.ID) + ' key: ' + str(ev) + ' at time: ' + str(self.session.clock.getTime())
                print log_msg
                # add to tracker log
                if self.session.tracker:
                    self.session.tracker.log( log_msg )                
                # add to self.events for adding to behavioral pickle
                self.events.append(log_msg)
        
            super(SPTrial, self).key_event( ev )

    def run(self, ID = 0):

        # shell()
        self.ID = ID
        super(SPTrial, self).run()

        self.fp_y = self.screen.size[1]*self.parameters['sp_path_elevation']-self.screen.size[1]/2
        target_y_offset = self.parameters['y_order']*self.parameters['test_stim_y_offset']*self.session.pixels_per_degree
  
        x_pos = self.parameters['x_pos']*self.session.pixels_per_degree
        y_pos = self.fp_y + target_y_offset
        self.session.test_stim.setPos([x_pos,y_pos ])

        # self.max_x = int(np.round( (self.parameters['sp_path_amplitude']/2*self.session.pixels_per_degree)))
        # self.session.ref_left.setPos([self.max_x*-1,self.fp_y])
        # self.session.ref_right.setPos([self.max_x,self.fp_y])

        # we are fascists on timing issues
        if self.ID != 0:
            self.trial_onset_time = self.session.cumulative_phase_durations[self.ID,0] + self.session.start_time

        while not self.stopped:
            # Only in trial 1, phase 0 represents the instruction period.
            # After the first trial, this phase is skipped immediately
            if (self.phase == 0) * (self.ID != 0):
                self.phase_forward()
            # only 1 phase in this trial
            if self.phase == 1:
                self.phase_1_time = self.session.clock.getTime()
                if ( self.phase_1_time  - self.trial_onset_time ) > self.phase_durations[1]:
                    self.stopped = True

            # events and draw
            self.event()
            self.draw()
    
        self.stop()
        
