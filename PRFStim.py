from __future__ import division
from psychopy import visual, core, misc, event, filters
import numpy as np
from scipy.signal import convolve2d
from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


class PRFStim(object):
    def __init__(self, screen, trial, session, orientation):
        # parameters

        self.trial = trial
        self.session = session
        self.screen = screen
        self.orientation = orientation    # convert to radians immediately, and use to calculate rotation matrix
        self.rotation_matrix = np.matrix([[cos(self.orientation), -sin(self.orientation)],[sin(self.orientation), cos(self.orientation)]])
        self.refresh_frequency = session.standard_parameters['redraws_per_TR'] / session.standard_parameters['TR']

        self.RG_color=session.standard_parameters['RG_color']
        self.BY_color=session.standard_parameters['BY_color']

        self.fast_speed = session.standard_parameters['fast_speed']
        self.slow_speed = session.standard_parameters['slow_speed']
        
        # print(self.orientation)

        if self.orientation in self.session.directions[[0,4]]:
            self.bar_width = self.screen.size[1] * session.standard_parameters['vertical_stim_size'] * session.standard_parameters['bar_width_ratio']
            self.bar_length = self.screen.size[0]
        elif self.orientation in self.session.directions[[2,6]]:
            self.bar_width = self.screen.size[0] * session.standard_parameters['horizontal_stim_size'] * session.standard_parameters['bar_width_ratio']
            self.bar_length = self.screen.size[1]
        self.num_elements = session.standard_parameters['num_elements']

        # change n_elements, sizes and bar width ratio for horizontal / vertical passes
        if self.trial.parameters['orientation'] in [0,np.pi]: # these are the vertical passes (e.g. top-bottom)
            self.size_pix = [self.screen.size[1]*session.standard_parameters['vertical_stim_size'],self.screen.size[0]*session.standard_parameters['horizontal_stim_size']]
            self.period = session.standard_parameters['vertical_pass_dur'] * session.standard_parameters['TR']
        else: # horizontal bar passes:
            self.size_pix = [self.screen.size[0]*session.standard_parameters['horizontal_stim_size'],self.screen.size[1]*session.standard_parameters['vertical_stim_size']]
            self.period = np.int(np.round(session.standard_parameters['horizontal_pass_dur'] * session.standard_parameters['TR']))
        
        if self.trial.parameters['stim_bool'] == 0:
            self.period = np.int(np.round(session.standard_parameters['vertical_pass_dur'] * session.standard_parameters['TR']))

        self.full_width = self.size_pix[0] + self.bar_width + self.session.standard_parameters['element_size']
        self.midpoint = 0

        # this is for determining ecc, which we make dependent on largest screen dimension

        self.phase = 0
        # bookkeeping variables
        self.eccentricity_bin = -1
        self.redraws = 0
        self.frames = 0
        self.last_stimulus_present_for_task = 0

        # psychopy stimuli
        self.populate_stimulus(pulse=False)

        # create the stimulus
        self.session.element_array = visual.ElementArrayStim(screen, nElements = self.num_elements, sizes = self.element_sizes, sfs = self.element_sfs, 
            xys = self.element_positions, colors = self.colors, colorSpace = 'rgb') 

        # set this to its default no-answer necessary value of None - this is tested for in PRFTrial when incorporating responses
        self.last_sampled_staircase = None

    def convert_sample(self,in_sample):
        return 1 - (1/(np.e**in_sample+1))
    
    def populate_stimulus(self,pulse=False):

        # what eccentricity bin are we in? 
        self.eccentricity_bin = np.min([floor(2.0 * abs(self.phase - 0.5) * (self.session.nr_staircases_ecc)), self.session.nr_staircases_ecc-1])

        RG_ratio = 0.5
        BY_ratio = 0.5
        fast_ratio = 0.5
        slow_ratio = 0.5

        # set the default colors
        self.colors = np.ones((self.num_elements,3)) * 0.5
        self.fix_gray_value = self.session.background_color

        # and change them if a pulse is wanted
        if pulse: 

            # update the color
            color_sample = self.session.staircases['bar_%i'%self.eccentricity_bin].get_intensity()
            color_1_ratio = self.convert_sample(color_sample)
            color_2_ratio = 1-color_1_ratio

            self.present_color_task_sign = np.random.choice([-1,1])
            if self.present_color_task_sign == 1:
                RG_ratio = color_1_ratio
                BY_ratio = color_2_ratio
            elif self.present_color_task_sign == -1:
                RG_ratio = color_2_ratio
                BY_ratio = color_1_ratio
            
            # send a log msg
            log_msg = 'signal in feature: bar ecc bin: %i phase: %1.3f value: %f (RG_ratio) %f at %f ' %(self.eccentricity_bin, self.phase, color_sample, RG_ratio, self.session.clock.getTime())
            if 'log_msg' in locals():
                if self.session.tracker:
                    self.session.tracker.log( log_msg )
                self.trial.events.append( log_msg )
                if self.session.task == 'bar':
                    print log_msg     

            fix_sample = self.session.staircases['fix_%i'%self.eccentricity_bin].get_intensity()
            fix_value = (self.convert_sample(fix_sample) - 0.5) * 2.0
        
            log_msg = 'signal in feature: fix ecc bin: %i phase: %1.3f value: %f/%f at %f ' % (self.eccentricity_bin, self.phase, fix_sample, fix_value, self.session.clock.getTime())
            if 'log_msg' in locals():
                if self.session.tracker:
                    self.session.tracker.log( log_msg )
                self.trial.events.append( log_msg )
                if self.session.task == 'fix':
                    print log_msg

            # define the last sampled staircase so the right staircase is updated
            self.last_sampled_staircase = self.session.task + '_%i'%self.eccentricity_bin    

            # Now set the actual stimulus parameters
            self.colors = np.concatenate((np.ones((int(np.round(self.num_elements*RG_ratio/2.0)),3)) * np.array([1,-1,0]) * self.RG_color,  # red/green - red
                                        np.ones((int(np.round(self.num_elements*RG_ratio/2.0)),3)) * np.array([-1,1,0]) * self.RG_color,  # red/green - green
                                        np.ones((int(np.round(self.num_elements*BY_ratio/2.0)),3)) * np.array([-1,-1,1]) * self.BY_color,  # blue/yellow - blue
                                        np.ones((int(np.round(self.num_elements*BY_ratio/2.0)),3)) * np.array([1,1,-1]) * self.BY_color))  # blue/yellow - yellow

            # and fix point parameters
            self.present_fix_task_sign = np.random.choice([-1,1])
            self.fix_gray_value = np.ones(3) * fix_value * self.present_fix_task_sign
    
        np.random.shuffle(self.colors)

        # but do update all other stim parameters (regardless of pulse)
        self.element_speeds = np.concatenate((np.ones(int(np.round(self.num_elements*fast_ratio))) * self.session.standard_parameters['fast_speed'],
                                            np.ones(int(np.round(self.num_elements*slow_ratio))) * self.session.standard_parameters['slow_speed']))
        np.random.shuffle(self.element_speeds)

        self.element_positions = np.random.rand(self.num_elements, 2) * np.array([self.bar_length, self.bar_width]) - np.array([self.bar_length/2.0, self.bar_width/2.0])
        # self.element_sfs = np.ones((self.num_elements)) * self.session.standard_parameters['element_spatial_frequency']
        self.element_sfs = np.random.rand(self.num_elements)*5+0.5
        self.element_sizes = np.ones((self.num_elements)) * self.session.standard_parameters['element_size']
        self.element_phases = np.zeros(self.num_elements)
        self.element_orientations = np.random.rand(self.num_elements) * 720.0 - 360.0

    def draw(self, phase = 0):

        self.phase = phase
        self.frames += 1

        if self.redraws <= (self.phase * self.period * self.refresh_frequency):

            # define midpoint
            if np.mod(self.redraws,self.session.standard_parameters['redraws_per_TR']) == 0:
                self.midpoint = phase * self.full_width - 0.5 * self.full_width #+ self.session.standard_parameters['x_offset']
            if (np.mod(self.redraws,self.session.standard_parameters['redraws_per_TR']) == 1):
                self.populate_stimulus(pulse=True)
            else:
                self.populate_stimulus(pulse=False)

            self.session.element_array.setSfs(self.element_sfs)
            self.session.element_array.setSizes(self.element_sizes)
            self.session.element_array.setColors(self.colors)
            self.session.element_array.setOris(self.element_orientations)
            if self.trial.parameters['orientation'] == np.pi/2:
                draw_midpoint = self.midpoint - self.session.standard_parameters['x_offset']
            elif self.trial.parameters['orientation'] == 3*(np.pi/2):
                draw_midpoint = self.midpoint + self.session.standard_parameters['x_offset']
            else:
                draw_midpoint = self.midpoint 
            self.session.element_array.setXYs(np.array(np.matrix(self.element_positions + np.array([0, -draw_midpoint])) * self.rotation_matrix)) 
            log_msg = 'stimulus draw for phase %f, at %f'%(phase, self.session.clock.getTime())
            self.trial.events.append( log_msg )
            if self.session.tracker:
                self.session.tracker.log( log_msg )
            
            self.redraws = self.redraws + 1

            
        # if fmod(self.phase * self.period * self.refresh_frequency, 1.0) > 0.5: 
        self.session.element_array.setPhases(self.element_speeds * self.phase * self.period + self.element_phases)

        if self.trial.parameters['stim_bool'] == 1:
            self.session.element_array.draw()
            #self.session.fixation.setColor(self.fix_gray_value)
        
        self.session.fixation_outer_rim.draw()
        self.session.fixation_rim.draw()
        self.session.fixation.draw()

        self.session.mask_stim.draw()
        
        
