
from matplotlib import pyplot as pl 
import numpy as np 
import pickle
import glob
import seaborn as sn

from IPython import embed as shell


def plot_staircases(input_files):

    for eccen_bin in np.arange(3):
        exec("color_staircase_%d=[]"%eccen_bin)
        exec("color_responses_%d =[]"%eccen_bin)

    for ri in range(run_nr):

        filename = glob.glob('data/%s_%d_2016*'%(initials,ri+1))[-1]
        ipf = open(filename)
        picklefile = pickle.load(ipf)
        ipf.close()

        color_staircase_0.append(np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: Color ecc bin: 0' in e) * (picklefile['parameterArray'][i]['task_index'] == 0)]) for i in range(len(picklefile['eventArray']))])  )
        color_responses_0.append(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Color bin 0' in e]) for i in range(len(picklefile['eventArray']))]))
        color_staircase_1.append(np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: Color ecc bin: 1' in e) * (picklefile['parameterArray'][i]['task_index'] == 0)]) for i in range(len(picklefile['eventArray']))])  )
        color_responses_1.append(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Color bin 1' in e]) for i in range(len(picklefile['eventArray']))]))
        color_staircase_2.append(np.concatenate([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: Color ecc bin: 2' in e) * (picklefile['parameterArray'][i]['task_index'] == 0)]) for i in range(len(picklefile['eventArray']))])  )
        color_responses_2.append(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase Color bin 2' in e]) for i in range(len(picklefile['eventArray']))]))

    color_moving_accuracy = []
    for ecc_bin in np.arange(3):
        color_ma_this_bin = np.zeros(len(np.hstack(eval('color_responses_%d'%ecc_bin))))
        for ri, response in enumerate(np.hstack(eval('color_responses_%d'%ecc_bin))):
            color_ma_this_bin[ri] = np.mean(np.hstack(eval('color_responses_%d'%ecc_bin))[:(ri+1)])
        color_moving_accuracy.append(color_ma_this_bin)

    f = pl.figure(figsize=(8,4))
    colors = [(c, 1-c, 1-c) for c in np.linspace(0.0,1.0,3)]
    s = f.add_subplot(121)
    pl.title('Staircase Color')
    for ecc_bin in np.arange(3):
        pl.plot(np.abs(np.hstack(eval('color_staircase_%d'%ecc_bin))),color=colors[ecc_bin],label='bin %d'%ecc_bin)
    pl.legend()
    pl.ylabel('staircase value')
    pl.ylim(ymin=0)


    s = f.add_subplot(122)
    pl.title('Moving accuracy Color')
    for ecc_bin in np.arange(3):
        pl.plot(color_moving_accuracy[ecc_bin],color=colors[ecc_bin],label='bin %d'%ecc_bin)
    pl.legend()
    pl.ylim(0.5,1)
    pl.axhline(0.83,linestyle='--',color='k')
    pl.ylabel('proportion correct')

    pl.tight_layout()
    pl.savefig('data/%s_%d_staircase_plot.pdf'%(initials,run_nr))







