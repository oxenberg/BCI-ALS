import numpy as np
import mne
from inputModule import read_params
import pandas as pd


class SnrModel:

    def __init__(self):
        self.params = read_params("../params_offline.JSON")
        self.ch_names = ['Fp1', 'Fp2', 'Fz', 'Cz', 'Pz', 'O1', 'O2']
        self.stim_freqs = np.arange(10,40,3)
        self.data = pd.DataFrame(columns=self.stim_freqs)
    def predict(self,deque_data):
        psds, freqs , picks_roi_vis = self.preprocess(deque_data)
        snrs = self.extract_snr(psds, noise_n_neighbor_freqs=3,
                                 noise_skip_neighbor_freqs=1)

        all_stim_freq = []
        for stim_freq in self.stim_freqs:
            i_bin_i_hz = np.argmin(abs(freqs - stim_freq))
            snrs_target = snrs[:, i_bin_i_hz][picks_roi_vis].mean()
            print(f'average SNR (occipital ROI): {snrs_target}')
            all_stim_freq.append(snrs_target)

        self.data.loc[self.data.shape[0] + 1] = all_stim_freq


        return 1
    def extract_snr(self, psd, noise_n_neighbor_freqs=1, noise_skip_neighbor_freqs=1):
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
    def pick_electrodes(self,rawData):
        roi_vis = ['POz', 'Oz', 'O1', 'O2', 'PO3', 'PO4', 'PO7',
                   'PO8', 'PO9', 'PO10', 'O9', 'O10']  # visual roi

        # Find corresponding indices using mne.pick_types()
        picks_roi_vis = mne.pick_types(rawData.info, eeg=True, stim=False,
                                       exclude='bads', selection=roi_vis)

        return picks_roi_vis

    def preprocess(self,deque_data):
        matrix = np.array(deque_data).T
        signal_lenth = matrix.shape[1]
        tmin = 0
        tmax = signal_lenth/self.params["SAMPLE_RATE"]
        fmin = 1.
        fmax = 90.

        ch_type = 'eeg'
        info = mne.create_info(self.params["ch_names"], self.params["SAMPLE_RATE"], ch_type)
        rawData = mne.io.RawArray(matrix, info)
        picks_roi_vis = self.pick_electrodes(rawData)
        rawData.filter(l_freq=0.1, h_freq=50, fir_design='firwin', verbose=False)
        psds, freqs = mne.time_frequency.psd_welch(
            rawData,
            n_fft= signal_lenth,
            n_overlap=0, n_per_seg=None,
            tmin=tmin, tmax=tmax,
            fmin=fmin, fmax=fmax,
            window='boxcar',
            verbose=False)

        print(psds,freqs)

        return psds, freqs , picks_roi_vis


    def save_data(self):

        self.data.to_csv("snr_data.csv")