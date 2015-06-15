
from matplotlib import pyplot as pl 
import numpy as np 
import pickle
import glob
import seaborn as sn

from IPython import embed as shell


def plot_staircases(initials,run_nr):

	for eccen_bin in np.arange(3):
		exec("color_staircase_%d=[]"%eccen_bin); exec("speed_staircase_%d = []"%eccen_bin); exec("fix_staircase_%d = []"%eccen_bin);exec("fix_no_stim_staircase_%d = []"%eccen_bin)
		exec("color_responses_%d =[]"%eccen_bin); exec("speed_responses_%d = []"%eccen_bin); exec("fix_responses_%d = []"%eccen_bin); exec("fix_no_stim_responses_%d = []"%eccen_bin)
	fix_no_stim_staircase = fix_no_stim_responses = []

	for ri in range(run_nr):

		filename = glob.glob('data/%s_%d_2015*'%(initials,ri+1))[-1]
		ipf = open(filename)
		picklefile = pickle.load(ipf)
		ipf.close()

		color_staircase_0.append(np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: Color ecc bin: 0' in e) * (picklefile['parameterArray'][i]['task_index'] == 0)]) for i in range(len(picklefile['eventArray']))])  )
		speed_staircase_0.append(np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: Speed ecc bin: 0' in e) * (picklefile['parameterArray'][i]['task_index'] == 1)]) for i in range(len(picklefile['eventArray']))])  )
		fix_staircase_0.append(np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: Fix ecc bin: 0' in e) * (picklefile['parameterArray'][i]['task_index'] == 2)]) for i in range(len(picklefile['eventArray']))]) )

		color_responses_0.append(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Color bin 0' in e]) for i in range(len(picklefile['eventArray']))]))
		speed_responses_0.append(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Speed bin 0' in e]) for i in range(len(picklefile['eventArray']))]))
		fix_responses_0.append(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Fix bin 0' in e]) for i in range(len(picklefile['eventArray']))]))
		
		color_staircase_1.append(np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: Color ecc bin: 1' in e) * (picklefile['parameterArray'][i]['task_index'] == 0)]) for i in range(len(picklefile['eventArray']))])  )
		speed_staircase_1.append(np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: Speed ecc bin: 1' in e) * (picklefile['parameterArray'][i]['task_index'] == 1)]) for i in range(len(picklefile['eventArray']))])  )
		fix_staircase_1.append(np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: Fix ecc bin: 1' in e) * (picklefile['parameterArray'][i]['task_index'] == 2)]) for i in range(len(picklefile['eventArray']))]) )

		color_responses_1.append(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Color bin 1' in e]) for i in range(len(picklefile['eventArray']))]))
		speed_responses_1.append(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Speed bin 1' in e]) for i in range(len(picklefile['eventArray']))]))
		fix_responses_1.append(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Fix bin 1' in e]) for i in range(len(picklefile['eventArray']))]))

		color_staircase_2.append(np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: Color ecc bin: 2' in e) * (picklefile['parameterArray'][i]['task_index'] == 0)]) for i in range(len(picklefile['eventArray']))])  )
		speed_staircase_2.append(np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: Speed ecc bin: 2' in e) * (picklefile['parameterArray'][i]['task_index'] == 1)]) for i in range(len(picklefile['eventArray']))])  )
		fix_staircase_2.append(np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: Fix ecc bin: 2' in e) * (picklefile['parameterArray'][i]['task_index'] == 2)]) for i in range(len(picklefile['eventArray']))]) )

		color_responses_2.append(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Color bin 2' in e]) for i in range(len(picklefile['eventArray']))]))
		speed_responses_2.append(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Speed bin 2' in e]) for i in range(len(picklefile['eventArray']))]))
		fix_responses_2.append(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Fix bin 2' in e]) for i in range(len(picklefile['eventArray']))]))

		fix_no_stim_staircase.append(np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ("signal in feature: Fix_no_stim" in e) * (picklefile['parameterArray'][i]['task_index'] == 3)]) for i in range(len(picklefile['eventArray']))]))
		fix_no_stim_responses.append(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Fix_no_stim' in e]) for i in range(len(picklefile['eventArray']))]))


	color_moving_accuracy = [];speed_moving_accuracy = []; fix_moving_accuracy = []
	for ecc_bin in np.arange(3):
		color_ma_this_bin = np.zeros(len(np.hstack(eval('color_responses_%d'%ecc_bin))))
		for ri, response in enumerate(np.hstack(eval('color_responses_%d'%ecc_bin))):
			color_ma_this_bin[ri] = np.mean(np.hstack(eval('color_responses_%d'%ecc_bin))[:(ri+1)])
		color_moving_accuracy.append(color_ma_this_bin)

		speed_ma_this_bin = np.zeros(len(np.hstack(eval('speed_responses_%d'%ecc_bin))))
		for ri, response in enumerate(np.hstack(eval('speed_responses_%d'%ecc_bin))):
			speed_ma_this_bin[ri] = np.mean(np.hstack(eval('speed_responses_%d'%ecc_bin))[:(ri+1)])
		speed_moving_accuracy.append(speed_ma_this_bin)

		fix_ma_this_bin = np.zeros(len(np.hstack(eval('fix_responses_%d'%ecc_bin))))
		for ri, response in enumerate(np.hstack(eval('fix_responses_%d'%ecc_bin))):
			fix_ma_this_bin[ri] = np.mean(np.hstack(eval('fix_responses_%d'%ecc_bin))[:(ri+1)])
		fix_moving_accuracy.append(fix_ma_this_bin)
	fix_no_stim_accuracy = np.zeros(len(np.hstack(fix_no_stim_responses)))
	for ri, response in enumerate(np.hstack(fix_no_stim_responses)):
		fix_no_stim_accuracy[ri] = np.mean(np.hstack(fix_no_stim_responses)[:(ri+1)])

	f = pl.figure(figsize=(12,8))
	colors = [(c, 1-c, 1-c) for c in np.linspace(0.0,1.0,3)]
	s = f.add_subplot(421)
	pl.title('Staircase Color')
	for ecc_bin in np.arange(3):
		pl.plot(np.abs(np.hstack(eval('color_staircase_%d'%ecc_bin))),color=colors[ecc_bin],label='bin %d'%ecc_bin)
	pl.legend()
	pl.ylim(ymin=0)
	s = f.add_subplot(423)
	pl.title('Staircase Speed')
	for ecc_bin in np.arange(3):
		pl.plot(np.abs(np.hstack(eval('speed_staircase_%d'%ecc_bin))),color=colors[ecc_bin],label='bin %d'%ecc_bin)
	pl.ylim(ymin=0)
	pl.legend()
	s = f.add_subplot(425)
	pl.title('Staircase Fix')
	for ecc_bin in np.arange(3):
		pl.plot(np.abs(np.hstack(eval('fix_staircase_%d'%ecc_bin))),color=colors[ecc_bin],label='bin %d'%ecc_bin)
	pl.legend()
	pl.ylim(ymin=0)
	s = f.add_subplot(427)
	pl.title('Staircase Fix no stim')
	pl.plot(np.hstack(fix_no_stim_staircase))
	pl.ylim(ymin=0)

	s = f.add_subplot(422)
	pl.title('Moving accuracy Color')
	for ecc_bin in np.arange(3):
		pl.plot(color_moving_accuracy[ecc_bin],color=colors[ecc_bin],label='bin %d'%ecc_bin)
	pl.legend()
	pl.ylim(0.5,1)
	pl.axhline(0.83,linestyle='--',color='k')
	s = f.add_subplot(424)
	pl.title('Moving accuracy Speed')
	for ecc_bin in np.arange(3):
		pl.plot(speed_moving_accuracy[ecc_bin],color=colors[ecc_bin],label='bin %d'%ecc_bin)
	pl.ylim(0.5,1)
	pl.legend()
	pl.axhline(0.83,linestyle='--',color='k')
	s = f.add_subplot(426)
	pl.title('Moving accuracy Fix')
	for ecc_bin in np.arange(3):
		pl.plot(fix_moving_accuracy[ecc_bin],color=colors[ecc_bin],label='bin %d'%ecc_bin)
	pl.axhline(0.83,linestyle='--',color='k')
	pl.ylim(0.5,1)
	pl.legend()
	s = f.add_subplot(428)
	pl.title('Moving accuracy Fix no stim')
	pl.axhline(0.83,linestyle='--',color='k')
	pl.plot(fix_no_stim_accuracy)
	pl.ylim(0.5,1)

	pl.tight_layout()

	pl.savefig('data/%s_%d_staircase_plot.pdf'%(initials,run_nr))







