#!/usr/bin/env python
# coding: utf-8

# base script for homework exercises
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")

from neurodesign import optimisation,experiment
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import t
import seaborn as sns
import pandas as pd
import numpy as np

cycles = 5000 # try cycles=10 for testing and cycles=5000 for real applications
sims = 10

exercise = 'part4' # change this for each exercise

# define the experiment
EXP = experiment(
    TR=2,
    duration=300,
    P = [1.0/5.0, 1.0/5.0, 1.0/5.0, 1.0/5.0, 1.0/5.0],
    C = [[1.0, -1.0, 0, 0, 0], [0, 0, 1.0, -1.0, 0], [1.0, 1.0, -1.0, -1.0, 0]],
    n_stimuli = 5,
    rho = 0.3,
    resolution=0.1,
    stim_duration=1,
    ITImodel = 'exponential',
    ITImin = 1,
    ITImean = 2,
    ITImax=5,
    confoundorder=3, # this cannot be 0
    hardprob=True,
    )

# optimize the design for detection efficiency only using GA
POP_GA = optimisation(
    experiment=EXP,
    weights=[0,.5,.5,0],
    preruncycles = 2,
    cycles = cycles,
    seed=1,
    outdes=5,
    I=10,
    folder='/tmp/',
    optimisation='GA',
    R = [0.5, 0.5, 0.0]
    )

POP_GA.optimise()

# print the best model score
print("Score: %s " % POP_GA.optima[::-1][0])
print("N trials: %d " % len(POP_GA.bestdesign.onsets))


# Let's look at the resulting experimental designs.

# this plots the columns of the X matrix convolved with the HRF
plt.figure(figsize=(10, 7))
plt.plot(POP_GA.bestdesign.Xconv)
plt.savefig("/data/%s_Xconv.pdf" % exercise)
plt.close()

plt.figure()
plt.plot(POP_GA.bestdesign.Xnonconv)
plt.savefig("/data/%s_X.pdf" % exercise)
plt.close()


# save the onsets for the best GA design

trials = pd.DataFrame(dict(onset=POP_GA.bestdesign.onsets, trial_type=POP_GA.bestdesign.order, ITI=POP_GA.bestdesign.ITI))
trials.to_csv('/data/%s.csv' % exercise)

# save the onsets by conditon
# groups = trials.groupby('trial_type')
# for g in groups:
#     onsets = groups.get_group(g[0])
#     onsets['onset'].to_csv('/data/best_GA_' + str(g[0]) + '.csv', index=False, header=False)

