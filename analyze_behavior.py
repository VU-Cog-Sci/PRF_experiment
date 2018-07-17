from __future__ import division
import pickle
import numpy as np
from IPython import embed as shell
import matplotlib.pyplot as pl
import statsmodels.stats.api as sms
import matplotlib as mpl
mpl.use('Agg')
import seaborn as sn
sn.set(style="white")
import sys

# from constants import *

mpl.rc_file_defaults()
keys = np.array(['a','s','d','f','j','k','l','semicolon'])

all_answers_left, all_answers_right, all_true_left,all_true_right,all_true_center,all_answers_center = [],[],[],[],[],[]
for fi in range(2,(len(sys.argv))):
	# pop the 0 position
	# answer_positions = np.delete(answer_positions,standard_parameters['n_targets']/2)

	fn = 'data/%s.pickle'%sys.argv[fi]

	with open(fn) as a:
		f=pickle.load(a)
		answers = np.array([t['answer'] for t in f['parameterArray']])
		positions= np.array([t['x_pos'] for t in f['parameterArray']])
		eye_dir= np.array([t['eye_dir'] for t in f['parameterArray']])
		params = f['parameterArray']

	false_trials = (answers==0)+(np.abs(positions)==1000)+np.array([a not in keys for a in answers])

	# answer_positions = np.linspace(-params[0]['sp_path_amplitude']/2-params[0]['ref_x_offset'],params[0]['ref_x_offset']+params[0]['sp_path_amplitude']/2, len(keys))
	answer_positions = np.linspace(-params[0]['sp_path_amplitude']/2,params[0]['sp_path_amplitude']/2, len(keys))

	answers=answers[~false_trials]
	positions=positions[~false_trials]
	eye_dir = eye_dir[~false_trials]

	answers_idx = np.array([np.where(a==keys)[0][0] for a in answers])
	answers_deg = answer_positions[answers_idx]

	all_answers_left.extend(answers_deg[(eye_dir==-1)])
	all_true_left.extend(positions[(eye_dir==-1)])

	all_answers_right.extend(answers_deg[(eye_dir==1)])
	all_true_right.extend(positions[(eye_dir==1)])
 
	all_answers_center.extend(answers_deg[(eye_dir==0)])
	all_true_center.extend(positions[(eye_dir==0)])	

# sort all trials
left_sort_order = np.argsort(all_true_left)
all_true_left = np.array(all_true_left)[left_sort_order]
all_answers_left = np.array(all_answers_left)[left_sort_order]

right_sort_order = np.argsort(all_true_right)
all_true_right = np.array(all_true_right)[right_sort_order]
all_answers_right = np.array(all_answers_right)[right_sort_order]

center_sort_order = np.argsort(all_true_center)
all_true_center = np.array(all_true_center)[center_sort_order]
all_answers_center = np.array(all_answers_center)[center_sort_order]

window_size = 10
smooth_answers_right_mean = np.array([np.mean(np.array(all_answers_right)[t:t+window_size]) for t in range(len(np.array(all_answers_right))-window_size)])
smooth_answers_right_ci = np.array([sms.DescrStatsW(np.array(all_answers_right)[t:t+window_size]).tconfint_mean() for t in range(len(np.array(all_answers_right))-window_size)])
smooth_true_right_mean = np.array([np.mean(np.array(all_true_right)[t:t+window_size]) for t in range(len(np.array(all_true_right))-window_size)])

smooth_answers_left_mean = np.array([np.mean(np.array(all_answers_left)[t:t+window_size]) for t in range(len(np.array(all_answers_left))-window_size)])
smooth_answers_left_ci = np.array([sms.DescrStatsW(np.array(all_answers_left)[t:t+window_size]).tconfint_mean() for t in range(len(np.array(all_answers_left))-window_size)])
smooth_true_left_mean = np.array([np.mean(np.array(all_true_left)[t:t+window_size]) for t in range(len(np.array(all_true_left))-window_size)])

smooth_answers_center_mean = np.array([np.mean(np.array(all_answers_center)[t:t+window_size]) for t in range(len(np.array(all_answers_center))-window_size)])
smooth_answers_center_ci = np.array([sms.DescrStatsW(np.array(all_answers_center)[t:t+window_size]).tconfint_mean() for t in range(len(np.array(all_answers_center))-window_size)])
smooth_true_center_mean = np.array([np.mean(np.array(all_true_center)[t:t+window_size]) for t in range(len(np.array(all_true_center))-window_size)])

f = pl.figure()
s = f.add_subplot(111)
if 1 in eye_dir:
	pl.plot(smooth_true_right_mean,smooth_answers_right_mean,color='g',label='sp rightwards')
	pl.fill_between(smooth_true_right_mean,smooth_answers_right_ci[:,0],smooth_answers_right_ci[:,1],alpha=0.1,color='g')

if -1 in eye_dir:
	pl.plot(smooth_true_left_mean,smooth_answers_left_mean,color='b',label='sp leftwards')
	pl.fill_between(smooth_true_left_mean,smooth_answers_left_ci[:,0],smooth_answers_left_ci[:,1],alpha=0.1,color='b')

if 0 in eye_dir:
	pl.plot(smooth_true_center_mean,smooth_answers_center_mean,color='r',label='fixation')
	pl.fill_between(smooth_true_center_mean,smooth_answers_center_ci[:,0],smooth_answers_center_ci[:,1],alpha=0.1,color='r')

pl.plot([np.min(positions),np.max(positions)],[np.min(positions),np.max(positions)],color='k')
pl.axhline(0,color='k',ls='--')
pl.axvline(0,color='k',ls='--')
pl.xlabel('presented x position (deg)')
pl.ylabel('reported x position (deg)')
sn.despine(offset=10)
pl.legend(loc='best')
pl.ylim(-params[0]['sp_path_amplitude']/2, params[0]['sp_path_amplitude']/2)
# s = f.add_subplot(212)
# pl.plot(np.unique(positions),answer_per_pos_dir_left_minus_right,color='r',label='left-right sp')
# pl.axhline(0,color='k',ls='--')
# pl.axvline(0,color='k',ls='--')
# pl.xlabel('presented x position (deg)')
# pl.ylabel('reported x pos (deg)')
# sn.despine(offset=10)
# pl.legend(loc='best')
pl.tight_layout()
pl.savefig('data/%s.pdf'%sys.argv[1])