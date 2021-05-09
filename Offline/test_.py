# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 20:24:18 2020

@author: oxenb
"""
import matplotlib.pyplot as plt
from mne.stats import bootstrap_confidence_interval
from mne.baseline import rescale

from pyOpenBCI import OpenBCICyton
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
import numpy as np
import mne
import random
import time
from inputModule import read_params

CH_AMOUNT = 16
TIME_BETWEEN_EVENTS = 3
SAMPLE_RATE = 125
TIME_BETWEEN_EVENTS_RATE = SAMPLE_RATE * TIME_BETWEEN_EVENTS

uVolts_per_count = (4500000) / 24 / (2 ** 23 - 1)  # uV/count
EXP_NAME = "../data/or_SSVEP_1_raw.fif"
rawData = mne.io.read_raw_fif(EXP_NAME, preload=True)

events = mne.find_events(rawData, stim_channel='STI')

event_dict =  {"1": 1, "2": 2, "3": 3,"4": 4, "5": 5, "6": 6,"7": 7, "8": 8, "9": 9}

rawData.plot_psd(fmax=50, spatial_colors=True)

fig = mne.viz.plot_events(events, event_id=event_dict, sfreq=rawData.info['sfreq'],
                          first_samp=rawData.first_samp)

reject_criteria = dict(eeg=150e-6)  # 250 µV

epochs = mne.Epochs(rawData, events, event_id=event_dict, tmin=-0.2, tmax=1.5, preload=True)

left_epochs = epochs['2']
right_epochs = epochs['3']
none_epochs = epochs['4']

left_epochs = left_epochs.average()
right_epochs = right_epochs.average()
none_epochs = none_epochs.average()

mne.viz.plot_compare_evokeds(dict(left=left_epochs, right=right_epochs, nothing=none_epochs),
                             legend='upper left', show_sensors='upper right')

epochs.plot_image(combine='mean')
event_id, tmin, tmax = 2, -0.5, 3.
baseline = None

iter_freqs = [
    ('Theta', 4, 7),
    ('Alpha', 8, 12),
    ('Beta', 13, 25),
    ('Gamma', 30, 45)
]

frequency_map = list()

for band, fmin, fmax in iter_freqs:
    # bandpass filter
    raw = rawData.copy()

    raw.filter(fmin, fmax, n_jobs=1,  # use more jobs to speed up.
               l_trans_bandwidth=1,  # make sure filter params are the same
               h_trans_bandwidth=1)  # in each band and skip "auto" option.

    # epoch
    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline=baseline,
                        preload=True)
    # remove evoked response
    epochs.subtract_evoked()

    # get analytic signal (envelope)
    epochs.apply_hilbert(envelope=True)
    frequency_map.append(((band, fmin, fmax), epochs.average()))


def stat_fun(x):
    """Return sum of squares."""
    return np.sum(x ** 2, axis=0)


# Plot
fig, axes = plt.subplots(4, 1, figsize=(10, 7), sharex=True, sharey=True)
colors = plt.get_cmap('winter_r')(np.linspace(0, 1, 4))
for ((freq_name, fmin, fmax), average), color, ax in zip(
        frequency_map, colors, axes.ravel()[::-1]):
    times = average.times * 1e3
    gfp = np.sum(average.data ** 2, axis=0)
    gfp = mne.baseline.rescale(gfp, times, baseline=(None, 0))
    ax.plot(times, gfp, label=freq_name, color=color, linewidth=2.5)
    ax.axhline(0, linestyle='--', color='grey', linewidth=2)
    ci_low, ci_up = bootstrap_confidence_interval(average.data, random_state=0,
                                                  stat_fun=stat_fun)
    ci_low = rescale(ci_low, average.times, baseline=(None, 0))
    ci_up = rescale(ci_up, average.times, baseline=(None, 0))
    ax.fill_between(times, gfp + ci_up, gfp - ci_low, color=color, alpha=0.3)
    ax.grid(True)
    ax.set_ylabel('GFP')
    ax.annotate('%s (%d-%dHz)' % (freq_name, fmin, fmax),
                xy=(0.95, 0.8),
                horizontalalignment='right',
                xycoords='axes fraction')
    ax.set_xlim(-500, 3000)
plt.show()
axes.ravel()[-1].set_xlabel('Time [ms]')
#########################












