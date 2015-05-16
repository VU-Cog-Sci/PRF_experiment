#!/usr/bin/env python
# encoding: utf-8
"""
Staircase.py

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

class OneUpOneDownStaircase(object):
	"""
	OneUpOneDownStaircase object, for one-up-one-down staircase in its standard form.
	"""
	def __init__(self, initial_value, initial_stepsize, nr_reversals = 10, increment_value = None, stepsize_multiplication_on_reversal = 0.75, max_nr_trials = 40 ):
		self.initial_value = initial_value
		self.initial_stepsize = initial_stepsize
		self.nr_reversals = nr_reversals
		self.increment_value = increment_value
		self.stepsize_multiplication_on_reversal = stepsize_multiplication_on_reversal
		self.max_nr_trials = max_nr_trials
		
		self.test_value = self.initial_value
		self.present_increment_value = increment_value
		
		# set up filler variables
		self.past_answers = []
		self.nr_trials = 0
		self.present_nr_reversals = 0
	
	def test_value(self):
		return self.test_value
	
	def answer( self, correct ):
		continue_after_this_trial = True
		self.nr_trials = self.nr_trials + 1
		if correct: # answer was correct and so we lower the contrast/whatever value
			self.test_value = self.test_value - self.present_increment_value
		else:
			self.test_value = self.test_value + self.present_increment_value
	
		self.past_answers.append(correct)
			
		if self.nr_trials > 1:
			if self.past_answers[-1] != self.past_answers[-2]:	# we have a reversal here
				self.present_nr_reversals = self.present_nr_reversals + 1
				if self.present_nr_reversals % 2 == 0:
					self.present_increment_value = self.present_increment_value * self.stepsize_multiplication_on_reversal
				if self.present_nr_reversals >= self.nr_reversals:
					continue_after_this_trial = False
			else: 
				pass
			if self.nr_trials >= self.max_nr_trials:
				continue_after_this_trial = False
		
		return continue_after_this_trial
	
class TwoUpOneDownStaircase(OneUpOneDownStaircase):
	def __init__(self, initial_value, initial_stepsize, nr_reversals = 10, increment_value = None, stepsize_multiplication_on_reversal = 0.75, max_nr_trials = 40 ):
		super(TwoUpOneDownStaircase, self).__init__(initial_value, initial_stepsize, nr_reversals = 10, increment_value = None, stepsize_multiplication_on_reversal = 0.75, max_nr_trials = 40)
		self.past_answers = [0.5, 0.5, 0.5]
	
	def answer( self, correct ):
		continue_after_this_trial = True
		self.nr_trials = self.nr_trials + 1
		self.past_answers.append(correct)
		
		nr_corrects_in_last_2_trials = np.array(self.past_answers, dtype = float)[-2:].sum()
		
		if nr_corrects_in_last_2_trials == 2:	# this subject is too good for this stimulus value
			self.test_value = self.test_value - self.present_increment_value
		else:
			self.test_value = self.test_value + self.present_increment_value
		
		if self.nr_trials > 1:
			if self.past_answers[-1] != self.past_answers[-2]:	# we have a reversal here
				self.present_nr_reversals = self.present_nr_reversals + 1
				if self.present_nr_reversals % 2 == 0:
					self.present_increment_value = self.present_increment_value * self.stepsize_multiplication_on_reversal
				if self.present_nr_reversals >= self.nr_reversals:
					continue_after_this_trial = False
			else: 
				pass
			if self.nr_trials >= self.max_nr_trials:
				continue_after_this_trial = False
		
		return continue_after_this_trial
	
class ThreeUpOneDownStaircase(TwoUpOneDownStaircase):
	def answer( self, correct ):
		continue_after_this_trial = True
		self.nr_trials = self.nr_trials + 1
		self.past_answers.append(correct)
		
		nr_corrects_in_last_3_trials = np.array(self.past_answers, dtype = float)[-3:].sum()
		
		if nr_corrects_in_last_3_trials == 3:	# this subject is too good for this stimulus value
			self.test_value = self.test_value - self.present_increment_value
		else:
			self.test_value = self.test_value + self.present_increment_value
		
		if self.nr_trials > 1:
			if self.past_answers[-1] != self.past_answers[-2]:	# we have a reversal here
				self.present_nr_reversals = self.present_nr_reversals + 1
				if self.present_nr_reversals % 2 == 0:
					self.present_increment_value = self.present_increment_value * self.stepsize_multiplication_on_reversal
				if self.present_nr_reversals >= self.nr_reversals:
					continue_after_this_trial = False
			else: 
				pass
			if self.nr_trials >= self.max_nr_trials:
				continue_after_this_trial = False
		
		return continue_after_this_trial
	
class YesNoStaircase(object):
	def __init__(self, initial_value, initial_stepsize, nr_reversals = 100, stepsize_multiplication_on_reversal = 0.75, max_nr_trials = 400 ):
		self.initial_value = initial_value
		self.initial_stepsize = initial_stepsize
		self.nr_reversals = nr_reversals
		self.stepsize_multiplication_on_reversal = stepsize_multiplication_on_reversal
		self.max_nr_trials = max_nr_trials
		
		self.test_value = self.initial_value
		self.present_increment_value = initial_stepsize
		
		# set up filler variables
		self.past_answers = []
		self.nr_trials = 0
		self.present_nr_reversals = 0
	
	def test_value(self):
		return self.test_value
	
	def answer( self, correct ):
		continue_after_this_trial = True
		self.nr_trials = self.nr_trials + 1
		if correct: # answer was correct and so we lower the contrast/whatever value according to Kaernbach's method
			self.test_value = self.test_value - self.present_increment_value
		else:
			self.test_value = self.test_value + 3.0 * self.present_increment_value
	
		self.past_answers.append(correct)
			
		if self.nr_trials > 1:
			if self.past_answers[-1] != self.past_answers[-2]:	# we have a reversal here
				self.present_nr_reversals = self.present_nr_reversals + 1
				if self.present_nr_reversals % 2 == 0:
					self.present_increment_value = self.present_increment_value * self.stepsize_multiplication_on_reversal
				if self.present_nr_reversals >= self.nr_reversals:
					continue_after_this_trial = False
			else: 
				pass
			if self.nr_trials >= self.max_nr_trials:
				continue_after_this_trial = False
		
		return continue_after_this_trial
	
	