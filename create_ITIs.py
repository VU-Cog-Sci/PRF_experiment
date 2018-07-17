from __future__ import division
from constants import *
import numpy as np
import os
import pickle

precueITIs = np.random.exponential(standard_parameters['mean_iti_precue'], standard_parameters['n_targets']) + standard_parameters['min_iti_precue']
np.save('ITIs/precueITIs.npy',precueITIs)

postcueITIs = np.random.exponential(standard_parameters['mean_iti_postcue'], standard_parameters['n_targets']) + standard_parameters['min_iti_postcue']
np.save('ITIs/postcueITIs.npy',postcueITIs)

targetsITIs = np.random.uniform(-standard_parameters['target_delay_window']/2,standard_parameters['target_delay_window']/2,standard_parameters['n_targets'])
np.save('ITIs/targetsITIs.npy',targetsITIs)

spITIs = np.round(np.random.exponential(standard_parameters['mean_iti_sp'], standard_parameters['n_targets']) + standard_parameters['min_iti_sp']).astype('int32')
np.save('ITIs/spITIs.npy',spITIs)