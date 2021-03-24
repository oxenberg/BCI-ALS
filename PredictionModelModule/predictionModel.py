import pandas as pd
from mne_features.feature_extraction import FeatureExtractor
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import (GridSearchCV, StratifiedKFold)
from mne import Epochs, pick_types
import mne
from os import path
import joblib
from Offline import create_raw_data
from inputModule import read_params

MODEL_PATH = "gsModel.pkl"


class PredictionModel:
    def __init__(self):
        if path.exists(MODEL_PATH):
            print("Couldn't find existing model. Creating new one")
            self.model = joblib.load(MODEL_PATH)
        else:
            self.createInitialModel()
            self.model = joblib.load(MODEL_PATH)
        self.params = read_params()

    def updateModel(self, data, label):
        epochs = self.preprocess(data, label)
        labels = epochs.events[:, -1]
        update_data = epochs.get_data()
        self.model.fit(update_data, labels)
        joblib.dump(self.model, MODEL_PATH)

    def predict(self, data):
        epochs = self.preprocess(data)
        prediction_data = epochs.get_data()
        label = self.model.predict(prediction_data)
        return label

    def preprocess(self, data=None, label=None):
        DATA_PATH = "data/"
        EXP_NAME = DATA_PATH + "Or_3_raw.fif"  ## file name to run the anaylsis on
        if data is None:
            raw = mne.io.read_raw_fif(EXP_NAME, preload=True)
        elif label is None:
            raw = create_raw_data(data)
        else:
            raw = create_raw_data(data, label)
        tmin, tmax = self.params["T_MIN"], self.params["T_MAX"]
        raw.filter(None, 40., fir_design='firwin', skip_by_annotation='edge')
        events = mne.find_events(raw, 'STI')
        picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                           exclude='bads')
        event_id = self.params["ACTIONS"]
        event_id = dict([(value, key) for key, value in event_id.items()])
        epochs = Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                        baseline=None, preload=True)
        epochs.pick_types(eeg=True, exclude='bads')  # remove stim and EOG
        return epochs, raw

    def train_mne_feature(self, data, labels, raw):
        selected_features = ["std", "mean", "kurtosis", "skewness"]  # can be changed to any feature
        pipe = Pipeline([('fe', FeatureExtractor(sfreq=raw.info['sfreq'],
                                                 selected_funcs=selected_features)),
                         ('scaler', StandardScaler()),
                         ('logreg', LogisticRegression())])
        y = labels
        # params_grid = {'fe__app_entropy__emb': np.arange(2, 5)} #: can addd gradinet boost hyperparametrs
        params_grid = {}  #: can add gradinet boost hyperparametrs
        gs = GridSearchCV(estimator=pipe, param_grid=params_grid,
                          cv=StratifiedKFold(n_splits=5, random_state=42), n_jobs=1,
                          return_train_score=True)
        gs.fit(data, y)
        scores = pd.DataFrame(gs.cv_results_)
        print(scores[['params', 'mean_test_score', 'mean_train_score']])
        # Best parameters obtained with GridSearchCV:
        print(gs.best_params_)

        joblib.dump(gs, MODEL_PATH)
        return pipe

    def createInitialModel(self):
        epochs, raw = self.preprocess()
        labels = epochs.events[:, -1]
        # get MEG and EEG data
        epochs_data_train = epochs.get_data()
        pipe = self.train_mne_feature(epochs_data_train, labels, raw)
        transformed_data = pipe["fe"].fit_transform(
            epochs_data_train)  #: transformed_data is matrix dim by the features X events
        return pipe, epochs_data_train









