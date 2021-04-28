import numpy as np
import mne

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


epochs = mne.Epochs(rawData, events, event_id=event_dict, tmin=-0.8, tmax=1, preload=True)
epochs = epochs["RIGHT"]
epochs = epochs.get_data()
times_to_cut = [0.7,1]
frq_cutoff = [1,30] # take the frq band from here


electrode = 2
for electrode_id in np.arange(1):
    spectrograms = []
    for i in np.arange(epochs.shape[0]):
        freqs, times, spectrogram = signal.spectrogram(epochs[i][electrode_id],fs = 125, nperseg = 10)

        spectrograms.append(spectrogram)

    t = np.linspace(-0.8, 1, len(times), endpoint=False)
    chosen_times = np.where((t > times_to_cut[0]) & (t < times_to_cut[1]))[0]
    chosen_freq = np.where((freqs > frq_cutoff[0]) & (freqs < frq_cutoff[1]))[0]
    spectrograms = np.array(spectrograms)

    plt.pcolormesh(t[chosen_times],freqs[chosen_freq], spectrograms.mean(axis = 0)[chosen_freq,chosen_times[:,np.newaxis]].T, shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title(f"electrod{electrode_id}")
    plt.show()

x  = spectrograms