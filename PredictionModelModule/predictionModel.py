import pandas as pd
from mne_features.feature_extraction import FeatureExtractor
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import (GridSearchCV, StratifiedKFold)
from mne import Epochs, pick_types
import mne
from os import path
import joblib
from inputModule.utils import read_params
import numpy as np

# MODEL_PATH = "../gsModel.pkl"

MODEL_PATH = "gsModel.pkl"

class PredictionModel:
    def __init__(self):
        self.params = read_params()

        if not path.isfile(MODEL_PATH):
            print("Couldn't find existing model, Creating new one")
            self.createInitialModel()

        self.model = joblib.load(MODEL_PATH)

    def updateModel(self, data, label):
        epochs, _ = self.preprocess(data, label)
        labels = epochs.events[:, -1]
        update_data = epochs.get_data()
        # normalize and feature selection
        update_data = self.model["scalar"].transform(self.model["fe"].transform(update_data))
        self.model["model"].partial_fit(update_data, labels)
        # joblib.dump(self.model, MODEL_PATH)

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

    def preprocess(self, data=None, label=None, read_from_file = False):
        drop_ch = []
        epochs = None
        data = np.array(data).T
        DATA_PATH = "data/"
        EXP_NAME = DATA_PATH + "or_5_raw.fif"  ## file name to run the anaylsis on
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

    def train_mne_feature(self, data, labels, raw):
        selected_features = ["mean", "kurtosis", "skewness"]  # can be changed to any feature
        pipe = Pipeline([('fe', FeatureExtractor(sfreq=raw.info['sfreq'],
                                                 selected_funcs=selected_features)),
                         ('scalar', StandardScaler()),
                         ('model', SGDClassifier(max_iter=300,alpha=0.03,learning_rate='constant',
                                                 eta0=0.01))])
        y = labels
        # params_grid = {'fe__app_entropy__emb': np.arange(2, 5)} #: can addd gradinet boost hyperparametrs
        params_grid = {}  #: can add gradinet boost hyperparametrs
        # gs = GridSearchCV(estimator=pipe, param_grid=params_grid,
        #                   cv=StratifiedKFold(n_splits=5), n_jobs=1,
        #                   return_train_score=True)
        pipe.fit(data, y)
        # scores = pd.DataFrame(gs.cv_results_)
        # print(scores[['params', 'mean_test_score', 'mean_train_score']])
        # Best parameters obtained with GridSearchCV:
        # print(gs.best_params_)

        joblib.dump(pipe, MODEL_PATH)
        return pipe

    def createInitialModel(self):
        epochs, raw = self.preprocess(read_from_file=True)
        labels = epochs.events[:, -1]
        # get MEG and EEG data
        epochs_data_train = epochs.get_data()
        pipe = self.train_mne_feature(epochs_data_train, labels, raw)
        # transformed_data = pipe["fe"].fit_transform(
        #     epochs_data_train)  #: transformed_data is matrix dim by the features X events
        # return pipe, epochs_data_train









