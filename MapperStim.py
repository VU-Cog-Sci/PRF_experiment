from __future__ import division
from psychopy import visual, core, misc, event, filters
import numpy as np
from scipy.signal import convolve2d
from IPython import embed as shell
from math import *
import random, sys

sys.path.append( 'exp_tools' )
# sys.path.append( os.environ['EXPERIMENT_HOME'] )


class MapperStim(object):
    def __init__(self, screen, trial, session):#,task):
        # parameters
        self.num_elements = session.standard_parameters['num_elements'] * (1/session.standard_parameters['bar_width_ratio'])
        self.trial = trial
        self.session = session
        self.screen = screen
        self.size_pix_hor = session.standard_parameters['horizontal_stim_size'] * session.screen_pix_size[0]
        self.size_pix_ver = session.standard_parameters['vertical_stim_size'] * session.screen_pix_size[1]
        # self.size_pix = session.standard_parameters['stim_size'] * session.screen_pix_size[1]
        self.period = session.standard_parameters['mapper_stim_in_TR'] * session.standard_parameters['TR']
        self.refresh_frequency = session.standard_parameters['redraws_per_TR'] / session.standard_parameters['TR']
        self.task_rate = session.standard_parameters['task_rate']
        # self.task = task

        self.phase = 0
        # bookkeeping variables
        self.eccentricity_bin = -1
        self.redraws = 0
        self.frames = 0
        self.last_stimulus_present_for_task = 0
        
        # construct timecourses of tasks
        # task_rate is in task_rate seconds per occurrence. we add 2x refresh frequency to avoid transients in the first second(s) and those following too quickly, and add an insane number to avoid tasks in the last second(s). 
                
        # psychopy stimuli
        self.populate_stimulus()

        # make this stimulus array a session variable, in order to have to create it only once...
        if not hasattr(session, 'element_array'):
            self.session.element_array = visual.ElementArrayStim(screen, nElements = self.num_elements, sizes = self.element_sizes, sfs = self.element_sfs, xys = self.element_positions, colors = self.colors, colorSpace = 'rgb') 

        # set this to its default no-answer necessary value of None - this is tested for in PRFTrial when incorporating responses
        self.last_sampled_staircase = None

    def populate_stimulus(self,pulse=False):

        self.colors = np.ones((self.num_elements,3)) * 0.5

        if pulse:
            red = np.array([ self.session.standard_parameters['RG_color'],- self.session.standard_parameters['RG_color'],0]) 
            green = np.array([- self.session.standard_parameters['RG_color'], self.session.standard_parameters['RG_color'],0]) 
            yellow = np.array([ self.session.standard_parameters['BY_color'], self.session.standard_parameters['BY_color'],- self.session.standard_parameters['BY_color']])
            blue = np.array([- self.session.standard_parameters['BY_color'],- self.session.standard_parameters['BY_color'], self.session.standard_parameters['BY_color']]) 
            # Now set the actual stimulus parameters
            self.colors = np.concatenate((np.ones((self.num_elements/4.0,3)) * red,  # red/green - red
                                        np.ones((self.num_elements/4.0,3)) * green,  # red/green - green
                                        np.ones((self.num_elements/4.0,3)) * blue,  # blue/yellow - blue
                                        np.ones((self.num_elements/4.0,3)) * yellow))  # blue/yellow - yellow


        self.fast_speed = self.session.standard_parameters['fast_speed']
        self.slow_speed = self.session.standard_parameters['slow_speed']

        np.random.shuffle(self.colors)
        self.element_positions = np.random.rand(self.num_elements, 2) * np.array([self.size_pix_hor, self.size_pix_ver]) - np.array([self.size_pix_hor/2.0, self.size_pix_ver/2.0])
        
        self.element_speeds = np.concatenate((np.ones(np.round(self.num_elements*self.session.fast_ratio)) * self.fast_speed,
                                            np.ones(np.round(self.num_elements*self.session.slow_ratio)) * self.slow_speed))
        np.random.shuffle(self.element_speeds)

        self.element_sfs = np.random.rand(self.num_elements)*5+0.5
        self.element_sizes = np.ones((self.num_elements)) * self.session.standard_parameters['element_size']
        self.element_phases = np.zeros(self.num_elements)
        self.element_orientations = np.random.rand(self.num_elements) * 720.0 - 360.0
        
    
    def draw(self, phase = 0):
        self.phase = phase
        self.frames += 1

        # if self.frames == 1:#self.redraws < (self.phase * self.period * self.refresh_frequency):
        # self.redraws = self.redraws + 1
        # self.populate_stimulus()
        if self.redraws <= (self.phase * self.period * self.refresh_frequency):
            if (np.mod(self.redraws,self.session.standard_parameters['redraws_per_TR']) == 1):
                self.populate_stimulus(pulse=True)
            else:
                self.populate_stimulus(pulse=False)

            self.session.element_array.setSfs(self.element_sfs)
            self.session.element_array.setSizes(self.element_sizes)
            self.session.element_array.setColors(self.colors)
            self.session.element_array.setOris(self.element_orientations)
            self.session.element_array.setXYs(np.array(np.matrix(self.element_positions))) 
            log_msg = 'stimulus draw for phase %f, at %f'%(phase, self.session.clock.getTime())
            self.trial.events.append( log_msg )
            if self.session.tracker:
                self.session.tracker.log( log_msg )
            self.redraws = self.redraws + 1

        # if fmod(self.phase * self.period * self.refresh_frequency, 1.0) > 0.5: 
        self.session.element_array.setPhases(self.element_speeds * self.phase * self.period + self.element_phases)

        if self.trial.parameters['draw_stim']:
            self.session.element_array.draw()    
        self.session.fixation_outer_rim.draw()
        self.session.fixation_rim.draw()
        self.session.fixation.draw()
        self.session.mask_stim.draw()
        
        
