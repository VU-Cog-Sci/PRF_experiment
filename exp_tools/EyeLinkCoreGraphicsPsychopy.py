import pylink

 
 
RIGHT_EYE = 1
LEFT_EYE = 0
BINOCULAR = 2
HIGH = 1
LOW = 0
WHITE = (255,255,255)
GRAY = GREY = (128,128,128)
BLACK = (0,0,0)
buttons =(0, 0);

 
 
 
class EyeLinkCoreGraphicsPsychopy(pylink.EyeLinkCustomDisplay):
	def __init__(self, tracker, display, displaySize):   
		'''Initialize a Custom EyeLinkCoreGraphics for Psychopy
		tracker: the TRACKER() object
		display: the Psychopy display window
		'''
		pylink.EyeLinkCustomDisplay.__init__(self)
		self.display = display
		self.displaySize = displaySize
		self.tracker = tracker		
		print("Finished initializing custom graphics")
 
	
 
 
 
 
class Tracker_EyeLink():
	def __init__(self, win, clock, sj = "TEST", autoCalibration=True, 
				 saccadeSensitivity = HIGH, calibrationType = 'HV9',
				 calibrationTargetColor = WHITE,
				 calibrationBgColor = BLACK, CalibrationSounds = False
				 ):
		'''
		win: psychopy visual window used for the experiment
 
		clock: psychopy time clock recording time for whole experiment
 
		sj: Subject identifier string (affects EDF filename)   cf plus bas
 
		autoCalibration:
		 True: enable auto-pacing during calibration
 
		saccadeSensitivity:
		 HIGH: Pursuit and neurological work
		 LOW:  Cognitive research
 
		calibrationType:
		 H3: Horizontal 3-point
		 HV3: 3-point calibration, poor linearization
		 HV5: 5-point calibration, poor at corners
		 HV9: 9-point calibration, best overall
 
		calibrationTargetColor and calibrationBgColor:
		 RGB tuple, i.e., (255,0,0) for Red
		 One of: BLACK, WHITE, GRAY
 
		calibrationSounds:
		 True: enable feedback sounds when calibrating 
 
		'''
		self.edfFileName = str(sj)+".edf"  ##nom du .edf
		print(self.edfFileName)
		self.screenSize = (1024,768)  
		self.units = 'deg'#inf['windowUnits']# 'deg'
		self.monitorName = "ViewSonic" #inf['windowMonitor.name']#   monitor de l'INT
		print("Connecting to eyetracker.")
		self.tracker = pylink.EyeLink("100.1.1.1")#########		 CONNECTION A L'EYELINK		  ########################
		print("Loading custom graphics")
		genv = EyeLinkCoreGraphicsPsychopy(self.tracker, win, self.screenSize)
		self.tracker.openDataFile(self.edfFileName)####
		pylink.flushGetkeyQueue() #It may be called at any time to get rid any of old keys from the queue.
		self.tracker.setOfflineMode();###Places EyeLink tracker in off-line mode. Wait till the traker has finished the mode transition.
		self.tracker.sendCommand("screen_pixel_coords =  0 0 %d %d"
									%( tuple(self.screenSize) ))
		self.tracker.setCalibrationType(calibrationType)
		self.tracker.sendMessage("DISPLAY_COORDS  0 0 %d %d"
									%( tuple(self.screenSize) ))
 
 
 
		###EYElink version
		eyelink_ver = self.tracker.getTrackerVersion()
		if eyelink_ver == 3:
			tvstr = self.tracker.getTrackerVersionString()
			vindex = tvstr.find("EYELINK CL")
			tracker_software_ver = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))
		else: tracker_software_ver = 0
		if eyelink_ver>=2:
			self.tracker.sendCommand("select_parser_configuration %d" %saccadeSensitivity)
		else:
			if saccadeSensitivity == HIGH:
				svt, sat = 22, 5000
			else: svt, sat = 35, 9500
			self.tracker.sendCommand("saccade_velocity_threshold = %d" %svt)
			self.tracker.sendCommand("saccade_acceleration_threshold = %d" %sat)
 
		if eyelink_ver == 2: #turn off scenelink camera stuff
			self.tracker.sendCommand("scene_camera_gazemap = NO")
 
 
 
		# set EDF file contents
		self.tracker.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
		if tracker_software_ver>=4:
			self.tracker.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET")
		else:
			self.tracker.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS")
			
		# set link data (used for gaze cursor)
		self.tracker.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON")
		if tracker_software_ver>=4:
			self.tracker.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET")
		else:
			self.tracker.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS")
 
 
 
		#Set the calibration settings:
		pylink.setCalibrationColors( calibrationTargetColor, calibrationBgColor)
		if CalibrationSounds:
			pylink.setCalibrationSounds("", "", "")
			pylink.setDriftCorrectSounds("", "off", "off")
		else:
			pylink.setCalibrationSounds("off", "off", "off")
			pylink.setDriftCorrectSounds("off", "off", "off")
 
		if autoCalibration:
			self.tracker.enableAutoCalibration
		else: self.tracker.disableAutoCalibration
		win.flip()
		print("Opening graphics")
		pylink.openGraphicsEx(genv)
		print("Begining tracker setup")
		self.tracker.doTrackerSetup()
		win.flip()
 
 
 
	def sendMessage(self, msg):
		'''Record a message to the tracker'''
		print(msg)
		self.tracker.sendMessage(msg)
 
	def sendCommand(self, msg):
		'''Send command to the tracker'''
		print(msg)
		self.tracker.sendCommand(msg)
 
	def resetEventQue(self):
		'''Reset the eyetracker event cue
			usage: use this prior to a loop calling recordFixation() so
			that old fixations or other events are cleared from the 
			buffer.
		'''
		self.tracker.resetData()
 
 
	def getStatus(self):###virer?
		"""Return the status of the connection to the eye tracker"""
		if self.tracker.breakPressed():
			return("ABORT_EXPT")
		if self.tracker.escapePressed():
			return("SKIP_TRIAL")
		if self.tracker.isRecording()==0:
			return("RECORDING")
		if self.tracker.isConnected(): 
			return("ONLINE")
		else:
			return("OFFLINE")
		return("UNKNOWN STATUS: " + str(self.tracker.getStatus()) )
 
	#================================================================
 
 
  
	def endTrial(self):
		'''Ends recording: adds 100 msec of data to catch final events'''
		pylink.endRealTimeMode() #Returns the application to a priority slightly above normal, to end realtime mode
		pylink.pumpDelay(100)# ???????
		self.tracker.stopRecording()#Stops recording, resets EyeLink data mode. Call 50 to 100 msec after an event occurs that ends the trial.

 
 
	#####################################################################
	#	Eyetracker set up and take-down
	#####################################################################
 
	def preTrial(self, trial, win, calibTrial=False):
		'''Set up each trial with the eye tracker
		'''
 
		if calibTrial: cond = "Test/Calibration Trial"
		else: cond = "Non-test/no calibration trial"
		message ="record_status_message 'Trial %d %s'"%(trial, cond)####rajouter le run?
		self.tracker.sendCommand(message)
		msg = "TRIALID %s"%trial
		self.tracker.sendMessage(msg)
		#Do drift correction if necissary
 
		if calibTrial:
			win.flip()
			while True:
				try:
					error = self.tracker.doDriftCorrect(self.screenSize[0]/2,self.screenSize[1]/2,1,1) 
					if error != 27:
						self.tracker.applyDriftCorrect
						break
					else:
						#self.tracker.doTrackerSetup()
						win.flip()#####refaire une calib?
				except:
					print("Exception")######sert a rien
					break
			win.flip()
			##################################################################################enlever au dessus +
		print("Switching to record mode")


		error = self.tracker.startRecording(1,1,1,1)
		pylink.beginRealTimeMode(100)
		if error: return error####
 
		if not self.tracker.waitForBlockStart(1000, 1, 0):######
			self.tracker.sendMessage ("TRIAL ERROR")
			self.endTrial()#arreter l'enregistrement car il y a erreur
			print "ERROR: No link samples received!"
			return "TRIAL_ERROR"
			
		self.eye_used = self.tracker.eyeAvailable(); 
		#determine which eye(s) are available
		if self.eye_used == RIGHT_EYE:
			self.tracker.sendMessage("EYE_USED 1 RIGHT")
		elif self.eye_used == LEFT_EYE or self.eye_used == BINOCULAR:
			self.tracker.sendMessage("EYE_USED 0 LEFT")
			self.eye_used = LEFT_EYE
		else:
			print "Error in getting the eye information!"
			return "TRIAL_ERROR"
			self.tracker.sendMessage ("TRIAL ERROR")
 
		self.tracker.flushKeybuttons(0)
 
 
 
	def closeConnection(self):
		'''Clean everything up, save data and close connection to tracker'''
		if self.tracker != None:
			# File transfer and cleanup!
			self.tracker.setOfflineMode();
			pylink.msecDelay (600)
			#Close the file and transfer it to Display PC
			self.tracker.closeDataFile()
			self.tracker.receiveDataFile(self.edfFileName, 
										 self.edfFileName) 
			self.tracker.close();
			return "Eyelink connection closed successfully"
		else:
			return "Eyelink not available, not closed properly"
 
 
 