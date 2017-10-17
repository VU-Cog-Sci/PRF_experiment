from __future__ import division

from matplotlib import pyplot as pl 
import numpy as np 
import pickle
import seaborn as sn
import glob
import time

from IPython import embed as shell

def analyze_behavior(initials,run_nr,task):
    filename = glob.glob('data/%s_%s_%d_%d*'%(initials,task,run_nr,time.gmtime()[0]))[-1]
    ipf = open(filename)
    picklefile = pickle.load(ipf)
    ipf.close()

    events = []
    for event_array in picklefile['eventArray']:
        for event in event_array:
            events.append(event)

    accuracy = []
    for i, event in enumerate(events):
        if 'signal' in event:
            answer_found = False
            for subevent in events[i+1:]:
                if 'signal' in subevent:
                    accuracy.append(0)
                    answer_found = True
                elif 'accuracy' in subevent:
                    sign = int(subevent.split(' ')[2][:-1])
                    response = int(subevent.split(' ')[4][:-1])
                    accuracy.append((sign*response+1)/2)
                    answer_found = True
                elif subevent == events[-1]:
                    accuracy.append(0)
                    answer_found = True

                if answer_found == True:
                    break

    f=pl.figure(figsize=(6,3))
    s = f.add_subplot(111)
    pl.plot(np.cumsum(accuracy)/(np.arange(len(accuracy))+1))
    pl.xlabel('trial #')
    pl.ylabel('accuracy')
    pl.ylim(0,1)
    pl.axhline(0.5,color='k',linestyle='--')
    sn.despine(offset=10)
    pl.tight_layout()
    pl.savefig('data/%s_%d_%s_accuracy.pdf'%(initials,run_nr,task))
