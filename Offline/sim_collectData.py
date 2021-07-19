import numpy as np
import mne
import seaborn as sns
import pandas as pd
from scipy import signal
import numpy as np
from matplotlib import pyplot as plt
import scipy.io
DATA_PATH = "../data/"
EXP_NAME = DATA_PATH+"or_SSVEP_2_raw.fif" #: give name to the expirement
# event_dict =  {"1": 1, "2": 2, "3": 3,"4": 4, "5": 5, "6": 6, "8": 8}
event_dict =  {"1": 1,"2":2}

tmin = -0.5
tmax = 4
fmin = 1.
fmax = 40.

def snr_spectrum(psd, noise_n_neighbor_freqs=1, noise_skip_neighbor_freqs=1):
    """Compute SNR spectrum from PSD spectrum using convolution.

    Parameters
    ----------
    psd : ndarray, shape ([n_trials, n_channels,] n_frequency_bins)
        Data object containing PSD values. Works with arrays as produced by
        MNE's PSD functions or channel/trial subsets.
    noise_n_neighbor_freqs : int
        Number of neighboring frequencies used to compute noise level.
        increment by one to add one frequency bin ON BOTH SIDES
    noise_skip_neighbor_freqs : int
        set this >=1 if you want to exclude the immediately neighboring
        frequency bins in noise level calculation

    Returns
    -------
    snr : ndarray, shape ([n_trials, n_channels,] n_frequency_bins)
        Array containing SNR for all epochs, channels, frequency bins.
        NaN for frequencies on the edges, that do not have enough neighbors on
        one side to calculate SNR.
    """
    # Construct a kernel that calculates the mean of the neighboring
    # frequencies
    averaging_kernel = np.concatenate((
        np.ones(noise_n_neighbor_freqs),
        np.zeros(2 * noise_skip_neighbor_freqs + 1),
        np.ones(noise_n_neighbor_freqs)))
    averaging_kernel /= averaging_kernel.sum()

    # Calculate the mean of the neighboring frequencies by convolving with the
    # averaging kernel.
    mean_noise = np.apply_along_axis(
        lambda psd_: np.convolve(psd_, averaging_kernel, mode='valid'),
        axis=-1, arr=psd
    )

    # The mean is not defined on the edges so we will pad it with nas. The
    # padding needs to be done for the last dimension only so we set it to
    # (0, 0) for the other ones.
    edge_width = noise_n_neighbor_freqs + noise_skip_neighbor_freqs
    pad_width = [(0, 0)] * (mean_noise.ndim - 1) + [(edge_width, edge_width)]
    mean_noise = np.pad(
        mean_noise, pad_width=pad_width, constant_values=np.nan
    )

    return psd / mean_noise


rawData = mne.io.read_raw_fif(EXP_NAME, preload=True)


rawData.info['bads'] = ["Fp1", "Fp2", "C3", "C4", "P7", "P8", "F7", "F8", "F3", "F4", "T7", "T8"]
# print(rawData.info)
# ch_names = ['Fp1', 'Fp2', 'C3', 'C4', 'P7', 'P8', 'O1', 'O2', 'F7', 'F8', 'F3', 'F4', 'T7', 'T8', 'P3', 'P4']
events = mne.find_events(rawData, stim_channel='STI')

frequencies = np.arange(2, 40, 0.1)
type = mne.pick_types(rawData.info, eeg=True)
epochs = mne.Epochs(rawData, events, picks = type, event_id=event_dict, tmin=tmin, tmax=tmax, preload=True)

sfreq = epochs.info['sfreq']


ep = epochs["2"]

psds, freqs = mne.time_frequency.psd_welch(
    ep,
    n_fft=int(sfreq * (tmax - tmin)),
    n_overlap=0, n_per_seg=None,
    tmin=tmin, tmax=tmax,
    fmin=fmin, fmax=fmax,
    window='boxcar',
    verbose=False)

snrs = snr_spectrum(psds, noise_n_neighbor_freqs=3,
                    noise_skip_neighbor_freqs=1)

fig, axes = plt.subplots(2, 1, sharex='all', sharey='none', figsize=(8, 5))
freq_range = range(np.where(np.floor(freqs) == 1.)[0][0],
                   np.where(np.ceil(freqs) == fmax - 1)[0][0])

psds_plot = 10 * np.log10(psds)
psds_mean = psds_plot.mean(axis=(0, 1))[freq_range]
psds_std = psds_plot.std(axis=(0, 1))[freq_range]
axes[0].plot(freqs[freq_range], psds_mean, color='b')
axes[0].fill_between(
    freqs[freq_range], psds_mean - psds_std, psds_mean + psds_std,
    color='b', alpha=.2)
axes[0].set(title="PSD spectrum", ylabel='Power Spectral Density [dB]')

# SNR spectrum
snr_mean = snrs.mean(axis=(0, 1))[freq_range]
snr_std = snrs.std(axis=(0, 1))[freq_range]

axes[1].plot(freqs[freq_range], snr_mean, color='r')
axes[1].fill_between(
    freqs[freq_range], snr_mean - snr_std, snr_mean + snr_std,
    color='r', alpha=.2)
axes[1].set(
    title="SNR spectrum", xlabel='Frequency [Hz]',
    ylabel='SNR', ylim=[-2, 30], xlim=[fmin, fmax])
fig.show()








#
#
# power = mne.time_frequency.tfr_morlet(ep, n_cycles=2, return_itc=False,
#                                               freqs=frequencies, decim=3)
# power.plot()

# for elc_num in range(2):
#     for event_id in list(event_dict.keys())[:-1]:
#         event_id_epochs = epochs[event_id]
#         power = mne.time_frequency.tfr_morlet(event_id_epochs, n_cycles=2, return_itc=False,
#                                               freqs=frequencies, decim=3)
#         power.plot(f"EEG {elc_num}", title=f"{event_id}{elc_num}")




# epochs = mne.Epochs(rawData, events, event_id=event_dict, tmin=-0.8, tmax=1, preload=True)
# epochs = scipy.io.loadmat(f'{DATA_PATH}right_data.mat')['rightData']
#
epochs = ep.get_data()
times_to_cut = [0.7,1]
frq_cutoff = [1,30] # take the frq band from here

#
for electrode_id in np.arange(4):
    spectrograms = []
    for i in np.arange(epochs.shape[0]):
        freqs, times, spectrogram = signal.spectrogram(epochs[i][electrode_id],fs = 128, nperseg = 24, noverlap = 0)
        # powerSpectrum, freqs, times, imageAxis = plt.specgram(epochs[i].T[electrode_id], Fs=32)
        spectrograms.append(spectrogram)

    t = np.linspace(0, 3.75, len(times), endpoint=False)
    chosen_times = np.where((t > times_to_cut[0]) & (t < times_to_cut[1]))[0]
    chosen_freq = np.where((freqs > frq_cutoff[0]) & (freqs < frq_cutoff[1]))[0]
    spectrograms = np.array(spectrograms)[chosen_freq,:]
#
#
#
    plt.pcolormesh(t,freqs, spectrograms.mean(axis = 0), shading='gouraud')
    # spectrograms = pd.DataFrame(data=spectrograms.mean(axis=0), index=freqs, columns=times)
    # f, ax = plt.subplots(figsize=(9, 6))
    # sns.heatmap(spectrograms, annot=False, ax=ax)
    # # ax.ylabel('Frequency [Hz]')
    # # plt.xlabel('Time [sec]')
    # plt.title(f"electrod{electrode_id}")
    # plt.gca().invert_yaxis()
    # plt.show()
