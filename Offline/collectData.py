# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 20:24:18 2020

@author: oxenb
"""
import matplotlib.pyplot as plt
from mne.stats import bootstrap_confidence_interval
from mne.baseline import rescale

from pyOpenBCI import OpenBCICyton
import numpy as np
import mne
import random
import time
from Offline.offlineUI import UI
from inputModule.utils import read_params
from inputModule import read_params


params_offline = read_params("params_offline.JSON")

CH_AMOUNT = params_offline["CH_AMOUNT"]
TIME_BETWEEN_EVENTS = params_offline["TIME_BETWEEN_EVENTS"]  # in seconds
SAMPLE_RATE = params_offline["SAMPLE_RATE"]
TIME_BETWEEN_EVENTS_RATE = SAMPLE_RATE * TIME_BETWEEN_EVENTS

uVolts_per_count = params_offline["uVolts_per_count"]  # uV/count

DATA_PATH = params_offline["DATA_PATH"]
EXP_FILE_NAME = params_offline["EXP_FILE_NAME"]
EXP_NAME = DATA_PATH + EXP_FILE_NAME  #: give name to the expirement
ch_names = params_offline["ch_names"]

EXPERIMENT_DURATION = params_offline["EXPERIMENT_DURATION"]
ITER = {"COUNT": 0}  # for cout the time
ACTIONS = { int(k): v for k,v in params_offline["ACTIONS"].items()}

RUN_EXP = params_offline["RUN_EXP"]  #: to collect data change to true

if RUN_EXP:
    board = OpenBCICyton(port=params_offline["port"], daisy=True)
start_time = time.time()
current_time = start_time
#########################

array_data = []
stim = []


#: create the raw object from array

def create_raw_data(results, stim):
    ch_type = 'eeg'
    info = mne.create_info(ch_names, SAMPLE_RATE, ch_type)
    rawData = mne.io.RawArray(results, info)
    #: add events data to raw
    stim_info = mne.create_info(['STI'], rawData.info['sfreq'], ['stim'])
    stim = np.expand_dims(stim, axis=0)
    stim_raw = mne.io.RawArray(stim, stim_info)
    rawData.add_channels([stim_raw], force_update_info=True)
    # eventsData = mne.find_events(rawData, stim_channel='STI')
    return rawData


def run_expirement(sample):
    data = np.array(sample.channels_data) * uVolts_per_count

    all_time = time.time() - start_time
    ITER["COUNT"] += 1
    if ITER["COUNT"] % TIME_BETWEEN_EVENTS_RATE == 0:
        int_action = random.randint(1, 3)
        print(ACTIONS[int_action])
        UIO.new_game(action=int_action, time_between=TIME_BETWEEN_EVENTS * 1000)
        print("")
        stim.append(int_action)
    else:
        stim.append(0)
    array_data.append(data)

    # print((all_time,event_time) )

    if int(all_time) >= EXPERIMENT_DURATION:
        board.stop_stream()


def start_expirement():
    global UIO
    UIO = UI()
    board.start_stream(run_expirement)
    board.disconnect()


if RUN_EXP:
    start_expirement()

    ##data exploration
    #: transform to array format
    array_data = np.array(array_data)
    array_data = array_data.transpose()
    array_data_v = array_data * 10 ** (-6)  #: to volt

    #: transform to raw (mne) format
    rawData = create_raw_data(array_data_v, stim)

    #: filter electrecy 50 hz freq
    rawData = rawData.filter(2, 45., fir_design='firwin')

    #: mainualy filtering
    events = mne.find_events(rawData, stim_channel='STI')

    annot_from_events = mne.annotations_from_events(
        events=events, event_desc=ACTIONS, sfreq=rawData.info['sfreq'])
    rawData.set_annotations(annot_from_events)

    rawData.plot()

    #: save data after cleaning
    rawData.save(EXP_NAME, overwrite=True)

else:
    rawData = mne.io.read_raw_fif(EXP_NAME, preload=True)
    # rawData = rawData.filter(1, 45., fir_design='firwin')
    print(rawData.info)
    events = mne.find_events(rawData, stim_channel='STI')

    event_dict = {'LEFT': 1, 'RIGHT': 2, 'NONE': 3}

    rawData.plot_psd(fmax=50, spatial_colors=True)

    fig = mne.viz.plot_events(events, event_id=event_dict, sfreq=rawData.info['sfreq'],
                              first_samp=rawData.first_samp)

    reject_criteria = dict(eeg=150e-6)  # 250 ??V

    epochs = mne.Epochs(rawData, events, event_id=event_dict, tmin=-0.2, tmax=1.5, preload=True)

    left_epochs = epochs['LEFT']
    right_epochs = epochs['RIGHT']
    none_epochs = epochs['NONE']

    left_epochs = left_epochs.average()
    right_epochs = right_epochs.average()
    none_epochs = none_epochs.average()

    mne.viz.plot_compare_evokeds(dict(left=left_epochs, right=right_epochs, nothing=none_epochs),
                                 legend='upper left', show_sensors='upper right')

    epochs.plot_image(combine='mean')
    event_id, tmin, tmax = 1, -0.5, 3.
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

    axes.ravel()[-1].set_xlabel('Time [ms]')

    # spectrogram
    frequencies = np.arange(2, 40, 0.1)
    epochs = mne.Epochs(rawData, events, event_id=event_dict, tmin=-0.8, tmax=3, preload=True)

    for event_id in event_dict.keys():
        event_id_epochs = epochs[event_id]
        power = mne.time_frequency.tfr_morlet(event_id_epochs, n_cycles=2, return_itc=False,
                                              freqs=frequencies, decim=3)
        power.plot("EEG 3", title=event_id)

#########################
