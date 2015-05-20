
from matplotlib import pyplot as pl 
import numpy as np 
import pickle
import glob
import seaborn as sn

from IPython import embed as shell


def plot_staircases(initials,run_nr):

	filename = glob.glob('data/%s_%d_2015*'%(initials,run_nr))[-1]
	ipf = open(filename)
	picklefile = pickle.load(ipf)
	ipf.close()

	color_staircase = [np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ("signal in feature: Color ecc bin: %d"%ecc in e) * (picklefile['parameterArray'][i]['unique_task'] == 0)]) for i in range(len(picklefile['eventArray']))])  for ecc in np.arange(4)]
	speed_staircase = [np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ("signal in feature: Speed ecc bin: %d"%ecc in e) * (picklefile['parameterArray'][i]['unique_task'] == 1)]) for i in range(len(picklefile['eventArray']))])  for ecc in np.arange(4)]
	fix_staircase = [np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ("signal in feature: Fix ecc bin: %d"%ecc in e) * (picklefile['parameterArray'][i]['unique_task'] == 2)]) for i in range(len(picklefile['eventArray']))]) for ecc in np.arange(4)]
	
	color_responses = [np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Color bin %d'%ecc in e]) for i in range(len(picklefile['eventArray']))]) for ecc in np.arange(4)]
	speed_responses = [np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Speed bin %d'%ecc in e]) for i in range(len(picklefile['eventArray']))])for ecc in np.arange(4)]
	fix_responses = [np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Fix bin %d'%ecc in e]) for i in range(len(picklefile['eventArray']))])for ecc in np.arange(4)]

	color_moving_accuracy = [];speed_moving_accuracy = []; fix_moving_accuracy = []
	for ecc_bin in np.arange(4):
		color_ma_this_bin = np.zeros(len(color_responses[ecc_bin]))
		for ri, response in enumerate(color_responses[ecc_bin]):
			color_ma_this_bin[ri] = np.mean(color_responses[ecc_bin][:(ri+1)])
		color_moving_accuracy.append(color_ma_this_bin)

		speed_ma_this_bin = np.zeros(len(speed_responses[ecc_bin]))
		for ri, response in enumerate(speed_responses[ecc_bin]):
			speed_ma_this_bin[ri] = np.mean(speed_responses[ecc_bin][:(ri+1)])
		speed_moving_accuracy.append(speed_ma_this_bin)

		fix_ma_this_bin = np.zeros(len(fix_responses[ecc_bin]))
		for ri, response in enumerate(fix_responses[ecc_bin]):
			fix_ma_this_bin[ri] = np.mean(fix_responses[ecc_bin][:(ri+1)])
		fix_moving_accuracy.append(fix_ma_this_bin)

	f = pl.figure(figsize=(12,8))
	colors = [(c, 1-c, 1-c) for c in np.linspace(0.0,1.0,4)]
	s = f.add_subplot(321)
	pl.title('Staircase Color')
	for ecc_bin in np.arange(4):
		pl.plot(np.abs(color_staircase[ecc_bin]),color=colors[ecc_bin],label='bin %d'%ecc_bin)
	pl.legend()
	pl.ylim(ymin=0)
	s = f.add_subplot(323)
	pl.title('Staircase Speed')
	for ecc_bin in np.arange(4):
		pl.plot(np.abs(speed_staircase[ecc_bin]),color=colors[ecc_bin],label='bin %d'%ecc_bin)
	pl.ylim(ymin=0)
	pl.legend()
	s = f.add_subplot(325)
	pl.title('Staircase Fix')
	for ecc_bin in np.arange(4):
		pl.plot(np.abs(fix_staircase[ecc_bin]),color=colors[ecc_bin],label='bin %d'%ecc_bin)
	pl.legend()
	pl.ylim(ymin=0)

	s = f.add_subplot(322)
	pl.title('Moving accuracy Color')
	for ecc_bin in np.arange(4):
		pl.plot(color_moving_accuracy[ecc_bin],color=colors[ecc_bin],label='bin %d'%ecc_bin)
	pl.legend()
	s = f.add_subplot(324)
	pl.title('Moving accuracy Speed')
	for ecc_bin in np.arange(4):
		pl.plot(speed_moving_accuracy[ecc_bin],color=colors[ecc_bin],label='bin %d'%ecc_bin)
	pl.legend()
	s = f.add_subplot(326)
	pl.title('Moving accuracy Fix')
	for ecc_bin in np.arange(4):
		pl.plot(fix_moving_accuracy[ecc_bin],color=colors[ecc_bin],label='bin %d'%ecc_bin)
	pl.legend()

	pl.savefig('data/%s_%d_staircase_plot.pdf'%(initials,run_nr))







