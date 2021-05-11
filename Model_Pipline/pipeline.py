from Offline import createModel
from mne import Epochs, pick_types
import mne
import joblib
from inputModule.utils import read_params
import numpy as np

MODEL_PATH = "../Model_Pipline/model_pip.pkl"


class ModelPipeline:
    def __init__(self):
        self.params = read_params('../SSVEP_UI/params_offline.JSON')
        try:
            self.model = joblib.load(MODEL_PATH)
        except ValueError:
            print("Oops! Couldn't find existing model")

    def predict(self, data):
        _, raw = self.preprocess(data)
        prediction_data = np.array([raw.get_data()])
        label = self.model.predict(prediction_data)
        return label

    def create_raw_data(self, results, stim=None):
        ch_names = ['EEG ' + str(ID) for ID in range(self.params["CH_AMOUNT"])]
        ch_type = 'eeg'
        info = mne.create_info(ch_names, self.params["SAMPLE_RATE"], ch_type)
        rawData = mne.io.RawArray(results, info)
        #: add events data to raw
        if not stim is None:
            stim_info = mne.create_info(['STI'], rawData.info['sfreq'], ['stim'])
            stim = np.expand_dims(stim, axis=0)
            stim_raw = mne.io.RawArray(stim, stim_info)
            rawData.add_channels([stim_raw], force_update_info=True)
            # eventsData = mne.find_events(rawData, stim_channel='STI')
        return rawData

    def create_epochs(self,raw):
        tmin, tmax = self.params["T_MIN"], self.params["T_MAX"]

        events = mne.find_events(raw, 'STI')
        # picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
        #                    exclude='bads')
        participant_events = list(map(str, set(events[:, -1])))
        event_id = self.params["ACTIONS"]

        event_id = {your_key: event_id[your_key] for your_key in participant_events}

        event_id = dict([(value, int(key)) for key, value in event_id.items()])
        epochs = Epochs(raw, events, event_id, tmin, tmax, proj=True,
                        baseline=None, preload=True)
        epochs.pick_types(eeg=True, exclude='bads')  # remove stim and EOG
        return epochs

    def preprocess(self, data=None, label=None, read_from_file=False):
        drop_ch = []
        epochs = None
        data = np.array(data).T
        DATA_PATH = "data/"
        EXP_NAME = DATA_PATH + "or_5_raw.fif"  # file name to run the analysis on
        if read_from_file:
            raw = mne.io.read_raw_fif(EXP_NAME, preload=True)
            epochs = self.create_epochs(raw)
        elif label == None:
            raw = self.create_raw_data(data)
            raw.drop_channels(drop_ch)
            raw.filter(2, 40., fir_design='firwin', skip_by_annotation='edge')
        else:
            raw = self.create_raw_data(data, label)
            raw.drop_channels(drop_ch)
            epochs = self.create_epochs(raw)

        return epochs, raw


