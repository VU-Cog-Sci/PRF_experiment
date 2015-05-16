#!/usr/bin/env python
# encoding: utf-8
"""
Session.py

Created by Tomas HJ Knapen on 2009-11-26.
Copyright (c) 2009 TK. All rights reserved.
"""


import os, sys, datetime
import subprocess, logging
import pickle, datetime, time

import scipy as sp
import numpy as np
# import matplotlib.pylab as pl
from math import *

from psychopy import visual, core, event, misc

# import VisionEgg
# VisionEgg.start_default_logging(); VisionEgg.watch_exceptions()
# 
# from VisionEgg.Core import *
import pygame
from pygame.locals import *
from scipy.io import wavfile

import pyaudio, wave

from pylink import *
from EyeLinkCoreGraphicsPyglet import EyeLinkCoreGraphicsPyglet


class Session(object):
	"""Session is a main class that creates screen and file properties"""
	def __init__(self, subject_initials, index_number):
		super(Session, self).__init__()
		self.subject_initials = subject_initials
		self.index_number = index_number
		
		self.setup_sound_system()
		# pygame.mixer.init()
		# os.chdir('sounds')
		# self.sound_files = ['%d.wav' % i for i in range(3)] # subprocess.Popen('ls *.*', shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')[0:-1]
		# self.sounds = [pygame.mixer.Sound(s) for s in self.sound_files]
		# os.chdir('..')
		
		self.clock = core.Clock()
		
		self.outputDict = {'parameterArray': [], 'eventArray' : []}
		self.events = []
		self.stopped = False
	
	def setup_sound_system(self):
		"""initialize pyaudio backend, and create dictionary of sounds."""
		self.pyaudio = pyaudio.PyAudio()
		self.sound_files = subprocess.Popen('ls ' + os.path.join(os.environ['EXPERIMENT_HOME'], 'sounds', '*.wav'), shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')[0:-1]
		self.sounds = {}
		for sf in self.sound_files:
			self.read_sound_file(file_name = sf)
		# print self.sounds

	def read_sound_file(self, file_name, sound_name = None):
		"""Read sound file from file_name, and append to self.sounds with name as key"""
		if sound_name == None:
			sound_name = os.path.splitext(os.path.split(file_name)[-1])[0]

		rate, data = wavfile.read(file_name)
		# create stream data assuming 2 channels, i.e. stereo data, and use np.float32 data format
		stream_data = data.astype(np.int16)

		# check data formats - is this stereo sound? If so, we need to fix it. 
		wf = wave.open(file_name, 'rb')
		# print sound_name
		# print wf.getframerate(), wf.getnframes(), wf.getsampwidth(), wf.getnchannels()
		if wf.getnchannels() == 2:
			stream_data = stream_data[::2]

		self.sounds.update({sound_name: stream_data})

	def create_screen(self, size = (1280, 960), full_screen = False, background_color = (0.0,0.0,0.0), 
						gamma_scale = (2.475,2.25,2.15), physical_screen_size = (48, 32), physical_screen_distance = 71.0, max_lums = (24.52, 78.8, 10.19), wait_blanking = True ):
		"""
		create_screen take a screen to display the stimuli on. 
		the standard screen is assumed to be the Sony FW600, which is set up to start up in the 
		1280x960@96Hz resolution.
		"""
		
		# the actual screen-getting
		# self.screen = visual.Window( size = size, fullscr = full_screen, allowGUI = False, units = 'pix', allowStencil = True, rgb = background_color, gamma = gamma_scale, waitBlanking = wait_blanking, winType = 'pyglet' )
		self.screen = visual.Window( size = size, fullscr = full_screen, allowGUI = False, units = 'pix', allowStencil = True, rgb = background_color, waitBlanking = wait_blanking, winType = 'pyglet' )
		
		self.screen.background_color = background_color
#		worked = pygame.display.set_gamma(gamma_scale[0],gamma_scale[1],gamma_scale[2])
		self.screen_pix_size = size
		self.max_lums = max_lums
		self.physical_screen_size = physical_screen_size
		self.physical_screen_distance = physical_screen_distance
		self.screen_height_degrees = 2.0 * 180.0/pi * atan((physical_screen_size[1]/2.0)/physical_screen_distance)
		self.pixels_per_degree = (size[1]) / self.screen_height_degrees
		self.centimeters_per_degree = physical_screen_size[1] / self.screen_height_degrees
		self.pixels_per_centimeter = self.pixels_per_degree / self.centimeters_per_degree
		# print 'screen: ' + str(self.screen_height_degrees) + ' degrees tall and pixels per degree: ' + str(self.pixels_per_degree)
		
		self.screen.setMouseVisible(False)
		self.screen.flip()
	
	def create_output_file_name(self, data_directory = 'data'):
		"""create output file"""
		now = datetime.datetime.now()
		opfn = now.strftime("%Y-%m-%d_%H.%M.%S")
		
		if not os.path.isdir(data_directory):
			os.mkdir(data_directory)
			
		self.output_file = os.path.join(data_directory, self.subject_initials + '_' + str(self.index_number) + '_' + opfn )
	
	def open_input_file(self):
		"""
		This method opens a pickle file that has input data in it.
		we assume the input data consists of two arrays - one for parameters and one for timings. 
		the two arrays' rows will be trials.
		"""
		self.input_file_name = self.index_number + '.pickle'
		ipf = open(self.input_file_name)
		self.input_data = pickle.load(ipf)
		ipf.close()
	
	def create_input_data(self, save = False):
		"""
		This method should be provided by subclasses that create input data on the fly
		"""
		pass
	
	def parse_input_data(self):
		"""
		We assume that the pickle file used as input will be an array, 
		the rows of which will be the requested trials.
		"""
		self.nr_trials = len(self.input_data)
	
	def close(self):
		"""close screen and save data"""
		pygame.mixer.quit()
		self.screen.close()
		parsopf = open(self.output_file + '_outputDict.pickle', 'a')
		pickle.dump(self.outputDict,parsopf)
		parsopf.close()
	
	def play_sound(self, sound_index = '0'):
		"""docstring for play_sound"""
		if type(sound_index) == int:
			sound_index = str(sound_index)
		# assuming 44100 Hz, mono channel np.int16 format for the sounds
		stream_data = self.sounds[sound_index]
		
		self.frame_counter = 0
		def callback(in_data, frame_count, time_info, status):
 			data = stream_data[self.frame_counter:self.frame_counter+frame_count]
 			self.frame_counter += frame_count
 			return (data, pyaudio.paContinue)

		# open stream using callback (3)
		stream = self.pyaudio.open(format=pyaudio.paInt16,
						channels=1,
						rate=44100,
						output=True,
						stream_callback=callback)

		stream.start_stream()
		# stream.write(stream_data)

	def play_np_sound(self, sound_array):
		# assuming 44100 Hz, mono channel np.int16 format for the sounds
		
		self.frame_counter = 0
		def callback(in_data, frame_count, time_info, status):
 			data = sound_array[self.frame_counter:self.frame_counter+frame_count]
 			self.frame_counter += frame_count
 			return (data, pyaudio.paContinue)

		# open stream using callback (3)
		stream = self.pyaudio.open(format=pyaudio.paInt16,
						channels=1,
						rate=44100,
						output=True,
						stream_callback=callback)

		stream.start_stream()
	

class EyelinkSession(Session):
	"""docstring for EyelinkSession"""
	def __init__(self, subject_initials, index_number):
		super(EyelinkSession, self).__init__(subject_initials, index_number)
	
	def create_tracker(self, tracker_on = True, sensitivity_class = 0, split_screen = False, screen_half = 'L', auto_trigger_calibration = 1, calibration_type = 'HV9', sample_rate = 1000):
		"""
		tracker sets up the connection and inputs the parameters.
		only start tracker after the screen is taken, its parameters are set,
		 and output file names are created.
		"""
		if tracker_on:
			# create actual tracker
			try:
				self.tracker = EyeLink()
				self.tracker_on = True
			except RuntimeError:
				print '\ncould not connect to tracker'
				self.tracker = None
				self.tracker_on = False
				self.eye_measured, self.sample_rate, self.CR_mode, self.file_sample_filter, self.link_sample_filter = 'N', sample_rate, 1, 1, 1
				return
		else:
			# not even create dummy tracker
			self.tracker = None
			self.tracker_on = False
			return
		
		self.eyelink_temp_file = self.subject_initials[:2] + '_' + str(self.index_number) + '_' + str(np.random.randint(99)) + '.edf'
		self.tracker.openDataFile(self.eyelink_temp_file)
		
		dir(self.tracker)
		self.genv = EyeLinkCoreGraphicsPyglet(self.screen.screen, self.screen, self.screen_pix_size)
		openGraphicsEx(self.genv)
		
		self.apply_settings(sensitivity_class = sensitivity_class, split_screen = split_screen, screen_half = screen_half, auto_trigger_calibration = auto_trigger_calibration, calibration_type = calibration_type, sample_rate = sample_rate)
		
	def apply_settings(self, sensitivity_class = 0, split_screen = False, screen_half = 'L', auto_trigger_calibration = True, sample_rate = 1000, calibration_type = 'HV9', margin = 60):
		
		# set EDF file contents 
		getEYELINK().sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
		getEYELINK().sendCommand("file_sample_filter = LEFT,RIGHT,GAZE,SACCADE,BLINK,MESSAGE,AREA,GAZERES,STATUS,HTARGET")
		getEYELINK().sendCommand("file_sample_data = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET")
		# set link data (used for gaze cursor) 
		getEYELINK().sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK")
		getEYELINK().sendCommand("link_sample_data = GAZE,GAZERES,AREA,HREF,PUPIL,STATUS")
		getEYELINK().sendCommand("link_event_data = GAZE,GAZERES,AREA,HREF,VELOCITY,FIXAVG,STATUS")
		# set further info
		getEYELINK().sendCommand("screen_pixel_coords =  0 0 %d %d" %self.screen_pix_size)
		getEYELINK().sendCommand("pupil_size_diameter = %s"%('YES'));
		getEYELINK().sendCommand("heuristic_filter %d %d"%([1, 0][sensitivity_class], 1))
		getEYELINK().sendCommand("sample_rate = %d" % sample_rate)
		
		# settings that address saccade sensitivity - to be set with sensitivity_class parameter. 0 is cognitive style, 1 is pursuit/neurological style
		getEYELINK().sendCommand("saccade_velocity_threshold = %d" %[30, 22][sensitivity_class])
		getEYELINK().sendCommand("saccade_acceleration_threshold = %d" %[9500, 5000][sensitivity_class])
		getEYELINK().sendCommand("saccade_motion_threshold = %d" %[0.15, 0][sensitivity_class])
		
#		getEYELINK().sendCommand("file_sample_control = 1,0,0")
		getEYELINK().sendCommand("screen_phys_coords = %d %d %d %d" %(-self.physical_screen_size[0] / 2.0, self.physical_screen_size[1] / 2.0, self.physical_screen_size[0] / 2.0, -self.physical_screen_size[1] / 2.0))
		getEYELINK().sendCommand("simulation_screen_distance = " + str(self.physical_screen_distance))
		
		if auto_trigger_calibration:
			getEYELINK().sendCommand("enable_automatic_calibration = YES")
		else:
			getEYELINK().sendCommand("enable_automatic_calibration = NO")
		
		# for binocular stereo-setup need to adjust the calibration procedure to sample only points on the left/right side of the screen. This allows only HV9 calibration for now.
			# standard would be:
			# getEYELINK().sendCommand("calibration_targets = 320,240 320,40 320,440 40,240 600,240 40,40 600,40, 40,440 600,440")
			# ordering of points:
		#	;; FOR 9-SAMPLE ALGORITHM:
		#	;; POINTS MUST BE ORDERED ON SCREEN:
		#	;; 5 1 6
		#	;; 3 0 4
		#	;; 7 2 8

		#	;; ordering for points in bicubic ("HV13", 13 pt) cal
		#	;; Point order: 6 2 7
		#	;;	 10 11
		#	;;	 4 1 5
		#	;;	 12 13
		#	;;	 8 3 9
		if split_screen:
			getEYELINK().sendCommand("calibration_type = HV9")
			getEYELINK().sendCommand("generate_default_targets = NO")
			
			sh, nsw = self.screen.size[1], self.screen.size[0]/2
			points = np.array([[nsw/2, sh/2], [nsw/2, sh-margin], [nsw/2, margin], [margin, sh/2], [nsw-margin, sh/2], [margin, sh - margin], [nsw - margin, sh - margin], [margin, margin], [nsw - margin, margin]])
			if screen_half == 'R':
				points[:,0] += nsw
			points_string = ''
			for p in points:
				points_string += "%s,%s " % tuple(p)
			points_string = points_string[:-1] # delete last space
			getEYELINK().sendCommand("calibration_targets = " % points_string)
			getEYELINK().sendCommand("validation_targets = " % points_string)
		else:
			getEYELINK().sendCommand("calibration_type = " + calibration_type)
			
			
			
	
	def tracker_setup(self, sensitivity_class = 0, split_screen = False, screen_half = 'L', auto_trigger_calibration = True, calibration_type = 'HV9', sample_rate = 1000):
		if self.tracker:
			
			# set colors and point size to be used during calibration
#			pylink.setCalibrationColors((127,127,127), (0,0,0))
#			pylink.setTargetSize(diameter = self.pixels_per_degree * 0.125, holesize = self.pixels_per_degree * 0.0625)
			
			# self.tracker.doTrackerSetup()
			# re-set all the settings to be sure of sample rate and filter and such that may have been changed during the calibration procedure and the subject pressing all sorts of buttons
			self.apply_settings(sensitivity_class = sensitivity_class, split_screen = split_screen, screen_half = screen_half, auto_trigger_calibration = auto_trigger_calibration, calibration_type = calibration_type, sample_rate = sample_rate )
			
			# we'll record the whole session continuously and parse the data afterward using the messages sent to the eyelink.
			self.tracker.startRecording(1,1,1,1)
			# for that, we'll need the pixel size and the like. 
			self.tracker.sendMessage('degrees per pixel ' + str(self.pixels_per_degree) )
			# now, we want to know how fast we're sampling, really
#			self.eye_measured, self.sample_rate, self.CR_mode, self.file_sample_filter, self.link_sample_filter = self.tracker.getModeData()
			self.sample_rate = self.tracker.getSampleRate()
			# self.sample_rate = 2000
			self.CR_mode = self.tracker.getCRMode()
			self.eye_measured = self.tracker.getEyeUsed()
			self.file_sample_filter = self.tracker.getFileFilter()
			self.link_sample_filter = self.tracker.getLinkFilter()
	
	def drift_correct(self, position = None):
		"""docstring for drift_correct"""
		if self.tracker:
			if position == None:	# standard is of course centered on the screen.
				position = [self.screen.size[0]/2,self.screen.size[1]/2]
			while 1:
				# Does drift correction and handles the re-do camera setup situations
				error = self.tracker.doDriftCorrect(position[0],position[1],1,1)
				if error != 27: 
					break;
				else:
					self.tracker_setup()
	
	def eye_pos(self):
		if self.tracker:
			dt = self.tracker.getNewestSample() # check for new sample update
			if(dt != None):
				# Gets the gaze position of the latest sample,
				if dt.isRightSample():
					gaze_position = dt.getRightEye().getGaze()
					return gaze_position[0],gaze_position[1] # self.screen.size[1]-
				elif dt.isLeftSample():
					gaze_position = dt.getLeftEye().getGaze()
					return gaze_position[0],gaze_position[1] # self.screen.size[1]-
			return 0,self.screen.size[1]-0
		else:
			pygame.event.pump()
			(x,y) = pygame.mouse.get_pos()
			y = self.screen.size[1]-y
			return x,y
		
	def detect_saccade(self, algorithm_type = 'velocity', threshold = 0.25, direction = None, fixation_position = None, max_time = 1.0 ):
		"""
		detect_saccade tries to detect a saccade based on position (needs fixation_position argument) or velocity (perhaps a direction argument?) information. 
		It can be 'primed' with a vector giving the predicted direction of the impending saccade. 
		detect_saccade looks for a saccade between call_time (= now) and max_time+call_time
		"""
		no_saccade = True
		start_time = core.getTime()
		if algorithm_type == 'velocity':
			sample_array = np.zeros((max_time * self.sample_rate, 2), dtype = np.float32)
			velocity_array = np.zeros((max_time * self.sample_rate, 2), dtype = np.float32)
			f = np.array([1,1,2,3], dtype = np.float32)/7.0
			nr_samples = 1
			sample_array[0,:] = self.eye_pos()
			velocity_array[0,:] = 0.001, 0.001
			if direction != None: # make direction a unit vector if it is an argument to this function
				direction = direction / np.linalg.norm(direction)
			
			while no_saccade:
				saccade_polling_time = core.getTime()
				sample_array[nr_samples][:] = self.eye_pos()
				if (sample_array[nr_samples-1][0] != sample_array[nr_samples][0]) or (sample_array[nr_samples-1][1] != sample_array[nr_samples][1]):
					velocity_array[nr_samples][:] = sample_array[nr_samples][:] - sample_array[nr_samples-1][:]
					if nr_samples > 3:
						# scale velocities according to x and y median-based standard deviations, as in engbert & mergenthaler, 2006
						med_scaled_velocity = velocity_array[:nr_samples]/np.mean(np.sqrt(((velocity_array[:nr_samples] - np.median(velocity_array[:nr_samples], axis = 0))**2)), axis = 0)
						if direction != None: 
							# scale the velocity array according to the direction in the direction argument before thresholding
							# assuming direction is a x,y unit vector specifying the expected direction of the impending saccade
							if np.inner(med_scaled_velocity[nr_samples], direction) > threshold:
								no_saccade = False
						if np.linalg.norm(med_scaled_velocity[-1]) > threshold:
							no_saccade = False
					nr_samples += 1
				if ( saccade_polling_time - start_time ) > max_time:
					no_saccade = False
			
		if algorithm_type == 'position' or not self.tracker:
			if fixation_position == None:
				fixation_position = np.array(self.eye_pos())
			while no_saccade:
				saccade_polling_time = core.getTime()
				ep = np.array(self.eye_pos())
		#		print ep, fixation_position, threshold, np.linalg.norm(ep - fixation_position) / self.pixels_per_degree
				if (np.linalg.norm(ep - fixation_position) / self.pixels_per_degree) > threshold:
					# eye position is outside the safe zone surrounding fixation - swap the buffers to change saccade target position
					no_saccade = False
		#			print '\n'
				if ( saccade_polling_time - start_time ) > max_time:
					no_saccade = False
			
		if algorithm_type == 'eyelink':
			while no_saccade:
				saccade_polling_time = core.getTime()
				ev = self.tracker.getNextData()
				if ev == 5: # start of a saccade
					no_saccade = False
				if ( saccade_polling_time - start_time ) > max_time:
					no_saccade = False
			
		return saccade_polling_time
			
	
	def close(self):
		if self.tracker:
			if self.tracker.isRecording():
				self.tracker.stopRecording()
			self.tracker.receiveDataFile(self.eyelink_temp_file,self.output_file + '.edf')
			self.tracker.close()
		super(EyelinkSession, self).close()
	
	def play_sound(self, sound_index = '1'):
		"""docstring for play_sound"""
		super(EyelinkSession, self).play_sound(sound_index = sound_index)
		if self.tracker != None:
			self.tracker.sendMessage('sound ' + str(sound_index) + ' at ' + str(VisionEgg.time_func()) )


class StarStimSession(EyelinkSession):
	"""StarStimSession adds starstim EEG trigger functionality to the EyelinkSession.
	It assumes an active recording, using NIC already connected over bluetooth.
	Triggers land in the file that's already set up and recording.
	"""
	def __init__(self, subject_initials, index_number, connect_to_starstim = False, TCP_IP = '10.0.1.201', TCP_PORT = 1234):
		super(StarStimSession, self).__init__(subject_initials, index_number)
		self.setup_starstim_connection(TCP_IP = TCP_IP, TCP_PORT = TCP_PORT, connect_to_starstim = connect_to_starstim)

	def setup_starstim_connection(self, TCP_IP = '10.0.1.201', TCP_PORT = 1234, connect_to_starstim = True):
		"""setup_starstim_connection opens a connection to the starstim to its standard ip address
		and standard (trigger) port. For controlling the recordings etc, we need tcp port 1235, it seems.
		more on that later. 
		"""
		if connect_to_starstim:
			self.star_stim_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.star_stim_socket.connect((TCP_IP, TCP_PORT))
			self.star_stim_connected = True
		else:
			self.star_stim_connected = False

	def close_starstim_connection(self):
		if self.star_stim_connected:
			self.star_stim_socket.close()

	def send_starstim_trigger(self, trigger = 1):
		if self.star_stim_connected:
			self.star_stim_socket.sendall('<TRIGGER>%i</TRIGGER>'%trigger)

	def close(self):
		super(StarStimSession, self).close()
		if self.star_stim_connected:
			self.close_starstim_connection()
