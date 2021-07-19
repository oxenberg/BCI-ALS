from pyOpenBCI import OpenBCICyton

import numpy as np
import mne
import random
import time

# our modules
from inputModule import read_params


class OfflineDataCollector:
    '''
    get all the parameters from the params_offline.JSON

    used in the offline session the collect the data from the EEG device
    loop over the samples that  came from the device in 125 Hz
    activate the offline UI
    '''

    def __init__(self, UI):
        self.params_offline = read_params("../params_offline.JSON")
        # important params for calculate time

        self.time_between_events_rate = self.set_time_from_json()

        self.board = OpenBCICyton(port=self.params_offline["port"], daisy=True)
        self.start_time = time.time()
        self.counter = 0
        self.UI = UI
        self.button_options = self.params_offline["9_screen_params"]["positions"]
        self.ACTIONS = { int(k): v for k,v in self.params_offline["ACTIONS"].items()}

        self.all_eeg_data = []
        self.stim = []

        # self.start_expirement()

    def run_expirement(self, sample):
        """
        here we run all exp
        :param sample: array with all channels data
        """
        data = np.array(sample.channels_data) * self.params_offline["uVolts_per_count"]
        all_time = time.time() - self.start_time  # total time form exp beginning
        self.counter += 1  # count how many samples take until now

        if self.counter % self.time_between_events_rate == 0:
            # button_index = random.randint(1, self.params_offline["MAX_SSVEP_OPTIONS"])
            button_index = random.randint(1, 2)
            choosen_button_loc = self.button_options[button_index-1]
            # self.UI.layout_switcher(choosen_button_loc)

            self.stim.append(button_index)
            self.UI.update_loc.emit(choosen_button_loc)
        else:
            self.stim.append(0)

        self.all_eeg_data.append(data)

        if int(all_time) >= self.params_offline["EXPERIMENT_DURATION"]:
            self.board.stop_stream()

    def start_expirement(self):
        self.board.start_stream(self.run_expirement)
        self.save_data()

    def end_expirment(self):
        self.board.disconnect()

    def create_raw_data(self,results, stim):
        ch_type = 'eeg'
        info = mne.create_info(self.params_offline["ch_names"], self.params_offline["SAMPLE_RATE"], ch_type)
        rawData = mne.io.RawArray(results, info)
        #: add events data to raw
        stim_info = mne.create_info(['STI'], rawData.info['sfreq'], ['stim'])
        stim = np.expand_dims(stim, axis=0)
        stim_raw = mne.io.RawArray(stim, stim_info)
        rawData.add_channels([stim_raw], force_update_info=True)

        return rawData

    def save_data(self):
        array_data = np.array(self.all_eeg_data)
        array_data = array_data.transpose()
        array_data_v = array_data * 10 ** (-6)  #: to volt

        #: transform to raw (mne) format
        rawData = self.create_raw_data(array_data_v, self.stim)

        #: filter electrecy 50 hz freq
        rawData.info['bads'] = ["Fp1", "Fp2", "C3", "C4", "P7", "P8", "F7", "F8", "F3", "F4", "T7", "T8"] # add a list of channels

        rawData = rawData.filter(1, 45., fir_design='firwin')

        #: mainualy filtering
        events = mne.find_events(rawData, stim_channel='STI')

        annot_from_events = mne.annotations_from_events(
            events=events, event_desc=self.ACTIONS, sfreq=rawData.info['sfreq'])
        rawData.set_annotations(annot_from_events)

        rawData.plot()

        #: save data after cleaning
        rawData.save(f"../data/{self.params_offline['EXP_NAME']}_raw.fif", overwrite=True)

    def set_time_from_json(self):
        TIME_BETWEEN_EVENTS = self.params_offline["TIME_BETWEEN_EVENTS"]  # in seconds
        SAMPLE_RATE = self.params_offline["SAMPLE_RATE"]
        return SAMPLE_RATE * TIME_BETWEEN_EVENTS

