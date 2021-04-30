import numpy as np
import mne
import seaborn as sns
import pandas as pd
DATA_PATH = "../data/"
EXP_NAME = DATA_PATH+"Or_5_raw.fif" #: give name to the expirement
event_dict = {'LEFT': 1, 'RIGHT': 2, 'NONE': 3}



rawData = mne.io.read_raw_fif(EXP_NAME, preload=True)
# print(rawData.info)
# ch_names = ['Fp1', 'Fp2', 'C3', 'C4', 'P7', 'P8', 'O1', 'O2', 'F7', 'F8', 'F3', 'F4', 'T7', 'T8', 'P3', 'P4']
events = mne.find_events(rawData, stim_channel='STI')

#
# frequencies = np.arange(2, 40, 0.1)
# epochs = mne.Epochs(rawData, events, event_id=event_dict, tmin=-0.8, tmax=1, preload=True)
#
#
# for elc_num in range(16):
#     for event_id in list(event_dict.keys())[:-1]:
#         event_id_epochs = epochs[event_id]
#         power = mne.time_frequency.tfr_morlet(event_id_epochs, n_cycles=2, return_itc=False,
#                                               freqs=frequencies, decim=3)
#         power.plot(f"EEG {elc_num}", title=f"{event_id}{elc_num}")


from scipy import signal
import numpy as np
from matplotlib import pyplot as plt
import scipy.io

# epochs = mne.Epochs(rawData, events, event_id=event_dict, tmin=-0.8, tmax=1, preload=True)
epochs = scipy.io.loadmat(f'{DATA_PATH}right_data.mat')['rightData']

# epochs = epochs.get_data()
times_to_cut = [0.7,1]
frq_cutoff = [1,30] # take the frq band from here





electrode = 2
for electrode_id in np.arange(1):
    spectrograms = []
    for i in np.arange(epochs.shape[0]):
        freqs, times, spectrogram = signal.spectrogram(epochs[i].T[electrode_id],fs = 128, nperseg = 32, noverlap = 0)
        # powerSpectrum, freqs, times, imageAxis = plt.specgram(epochs[i].T[electrode_id], Fs=32)
        spectrograms.append(spectrogram)

    t = np.linspace(0, 3.75, len(times), endpoint=False)
    chosen_times = np.where((t > times_to_cut[0]) & (t < times_to_cut[1]))[0]
    chosen_freq = np.where((freqs > frq_cutoff[0]) & (freqs < frq_cutoff[1]))[0]
    spectrograms = np.array(spectrograms)



    # plt.pcolormesh(t,freqs, spectrograms.mean(axis = 0), shading='gouraud')
    spectrograms = pd.DataFrame(data=spectrograms.mean(axis=0), index=freqs, columns=times)
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(spectrograms, annot=False, ax=ax)
    # ax.ylabel('Frequency [Hz]')
    # plt.xlabel('Time [sec]')
    plt.title(f"electrod{electrode_id}")
    plt.gca().invert_yaxis()
    plt.show()

x  = spectrograms