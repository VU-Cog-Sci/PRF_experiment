
from matplotlib import pyplot as pl 
import numpy as np 
import pickle
import glob
import time
# import seaborn as sn

from constants import *

from IPython import embed as shell

n_eccen_bins = standard_parameters['nr_staircases_ecc']

def plot_staircases(initials,run_nr):

    n_bar_runs=0
    n_fix_runs=0

    color_staircase = {}; fix_staircase = {}; color_responses = {};  fix_responses = {}; 
    for eccen_bin in np.arange(n_eccen_bins):
        color_staircase[eccen_bin] = []
        fix_staircase[eccen_bin] = []
        color_responses[eccen_bin] = []
        fix_responses[eccen_bin] = []

    for ri in range(run_nr):

        filename = glob.glob('data/%s_%d_%d*'%(initials,ri+1,time.gmtime()[0]))[-1]
        ipf = open(filename)
        picklefile = pickle.load(ipf)
        ipf.close()

        if (picklefile['parameterArray'][0]['task'] == 1):
            n_bar_runs +=1
        elif (picklefile['parameterArray'][0]['task'] == 0):
            n_fix_runs +=1

        for eccen_bin in np.arange(n_eccen_bins):

            color_staircase[eccen_bin].extend([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: bar ecc bin: %d'%eccen_bin in e) * (picklefile['parameterArray'][i]['task'] == 1)]) for i in range(len(picklefile['eventArray']))]) 
            fix_staircase[eccen_bin].extend([np.array([float(e.split(' ')[-4]) for e in picklefile['eventArray'][i]  if ('signal in feature: fix ecc bin: %d'%eccen_bin in e) * (picklefile['parameterArray'][i]['task'] == 0)]) for i in range(len(picklefile['eventArray']))]) 
            color_responses[eccen_bin].extend(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase bar bin %d'%eccen_bin in e]) for i in range(len(picklefile['eventArray']))]))
            fix_responses[eccen_bin].extend(np.concatenate([np.array([float(e.split(' ')[-3]) for e in picklefile['eventArray'][i]  if 'staircase fix bin %d'%eccen_bin in e]) for i in range(len(picklefile['eventArray']))]))

    color_moving_accuracy = []; fix_moving_accuracy = []
    for ecc_bin in np.arange(n_eccen_bins):
        if n_bar_runs>0:
            color_ma_this_bin = np.zeros(len(np.hstack(color_responses[ecc_bin])))
            for ri, response in enumerate(np.hstack(color_responses[ecc_bin])):
                color_ma_this_bin[ri] = np.mean(np.hstack(color_responses[ecc_bin])[:(ri+1)])
        color_moving_accuracy.append(color_ma_this_bin)

        if n_fix_runs >0:
            fix_ma_this_bin = np.zeros(len(np.hstack(fix_responses[ecc_bin])))
            for ri, response in enumerate(np.hstack(fix_responses[ecc_bin])):
                fix_ma_this_bin[ri] = np.mean(np.hstack(fix_responses[ecc_bin])[:(ri+1)])
            fix_moving_accuracy.append(fix_ma_this_bin)

    f = pl.figure(figsize=(12,8))
    colors = [(c, 1-c, 1-c) for c in np.linspace(0.0,1.0,n_eccen_bins)]
    s = f.add_subplot(221)
    pl.title('Staircase Color')
    if n_bar_runs >0:
        for ecc_bin in np.arange(n_eccen_bins):
            pl.plot(np.abs(np.hstack(color_staircase[ecc_bin])),color=colors[ecc_bin],label='bin %d'%ecc_bin)
        pl.legend(loc='best')
        pl.ylim(ymin=0)
    s = f.add_subplot(223)
    pl.title('Staircase Fix')
    if n_fix_runs >0:
        for ecc_bin in np.arange(n_eccen_bins):
            pl.plot(np.abs(np.hstack(fix_staircase[ecc_bin])),color=colors[ecc_bin],label='bin %d'%ecc_bin)
        pl.legend(loc='best')
    pl.ylim(ymin=0)

    s = f.add_subplot(222)
    pl.title('Moving accuracy Color')
    if n_bar_runs >0:
        for ecc_bin in np.arange(n_eccen_bins):
            pl.plot(color_moving_accuracy[ecc_bin],color=colors[ecc_bin],label='bin %d'%ecc_bin)
        pl.legend(loc='best')
    pl.ylim(0.5,1)
    pl.axhline(0.83,linestyle='--',color='k')
    s = f.add_subplot(224)
    pl.title('Moving accuracy Fix')
    if n_fix_runs >0:
        for ecc_bin in np.arange(n_eccen_bins):
            pl.plot(fix_moving_accuracy[ecc_bin],color=colors[ecc_bin],label='bin %d'%ecc_bin)
        pl.legend(loc='best')
    pl.axhline(0.83,linestyle='--',color='k')
    pl.ylim(0.5,1)

    pl.tight_layout()

    pl.savefig('data/%s_%d_staircase_plot.pdf'%(initials,run_nr))






