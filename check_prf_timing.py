from __future__ import division
import pickle

filename = 'data/de_prf_2_2017-10-16_18.56.36_outputDict.pickle'
ipf = open(filename)
picklefile = pickle.load(ipf)
ipf.close()
import numpy as np
sp = picklefile['parameterArray'][0]
trial_start_times = []
stim_on_times = []
stim_off_times = []
phase_starts = np.zeros((len(picklefile['eventArray']),5))
for i,trial in enumerate(picklefile['eventArray']):
	for event in trial:
		for phase in range(5):
			if 'trial %d started at'%i in event:
				phase_starts[i,phase] = float(event.split(' ')[-1])
			elif 'trial %d phase %d'%(i,phase) in event:
				phase_starts[i,phase] = float(event.split(' ')[-1])

phase_durations = np.zeros((len(picklefile['eventArray']),5))
for phase in range(4):
	phase_durations[:,phase] = phase_starts[:,phase+1] - phase_starts[:,phase]
phase_durations[:-1,4] = phase_starts[1:,0]-phase_starts[:-1,-1]
		# if 'trial 0 phase 2' in event:
		# 	start_time = float(event.split(' ')[-1])

		# if 'trial %d started at'%i in event:
		# 	trial_start_times.append(float(event.split(' ')[-1]))
		
		# if 'phase 3' in event:
		# 	stim_on_times.append(float(event.split(' ')[-1])-start_time)
		# elif 'phase 4' in event:
		# 	stim_off_times.append(float(event.split(' ')[-1])-start_time)

stim_on_times = np.array(stim_on_times)
stim_off_times = np.array(stim_off_times)
trial_start_times = np.array(trial_start_times)

scanner = False
print 'stim durations (should be %.3f)'%(sp['TR']*sp['PRF_period_in_TR'])
print np.array(stim_off_times-stim_on_times)
if scanner:
	print 'stim itis (should be %.3f)'%(sp['TR']*np.ceil(sp['PRF_ITI_in_TR']))
else:
	print 'stim itis (should be %.3f)'%(sp['TR']*sp['PRF_ITI_in_TR'])

print np.array(stim_on_times[1:]-stim_off_times[:-1])
print 'trial durations'
print np.diff(trial_start_times)



