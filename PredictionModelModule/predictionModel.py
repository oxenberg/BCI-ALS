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
PARAMS = read_params()


class PredictionModel:
    def __init__(self):
        if path.exists(MODEL_PATH):
            print("Couldn't find existing model. Creating new one")
            self.model = joblib.load(MODEL_PATH)
        else:
            createInitialModel()
            self.model = joblib.load(MODEL_PATH)

    def updateModel(self, data, label):
        epochs = preprocess(data, label)
        labels = epochs.events[:, -1]
        update_data = epochs.get_data()
        self.model.fit(update_data, labels)
        joblib.dump(self.model, MODEL_PATH)

    def predict(self, data):
        epochs = preprocess(data)
        prediction_data = epochs.get_data()
        label = self.model.predict(prediction_data)
        return label


DATA_PATH = "data/"
EXP_NAME = DATA_PATH+"Or_3_raw.fif" ## file name to run the anaylsis on

features = ['app_entropy', 'decorr_time', 'higuchi_fd',
            'hjorth_complexity', 'hjorth_complexity_spect', 'hjorth_mobility',
            'hjorth_mobility_spect', 'hurst_exp', 'katz_fd', 'kurtosis',
            'line_length', 'mean', 'ptp_amp', 'samp_entropy',
            'skewness', 'spect_edge_freq', 'spect_entropy', 'spect_slope',
            'std', 'svd_entropy', 'svd_fisher_info', 'teager_kaiser_energy',
            'variance', 'wavelet_coef_energy', 'zero_crossings', 'max_cross_corr',
            'nonlin_interdep', 'phase_lock_val', 'spect_corr', 'time_corr']

selected_features = ["std", "mean", "kurtosis", "skewness"]  # can be changed to any feature


def preprocess(data=None, label=None):
    if data is None:
        raw = mne.io.read_raw_fif(EXP_NAME, preload=True)
    elif label is None:
        raw = create_raw_data(data)
    else:
        raw = create_raw_data(data, label)
    tmin, tmax = PARAMS.T_MIN, PARAMS.T_MAX
    raw.filter(None, 40., fir_design='firwin', skip_by_annotation='edge')
    events = mne.find_events(raw, 'STI')
    picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                       exclude='bads')
    event_id = PARAMS.ACTIONS  # {'Left': 1, 'right': 2, 'none': 3}  #TODO: notice different order from JSON
    epochs = Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                    baseline=None, preload=True)
    epochs.pick_types(eeg=True, exclude='bads')  # remove stim and EOG
    return epochs, raw


def train_mne_feature(data, labels, raw):
    pipe = Pipeline([('fe', FeatureExtractor(sfreq=raw.info['sfreq'],
                                             selected_funcs=selected_features)),
                     ('scaler', StandardScaler()),
                     ('logreg', LogisticRegression())])
    y = labels
    # params_grid = {'fe__app_entropy__emb': np.arange(2, 5)} #: can addd gradinet boost hyperparametrs
    params_grid = {}  #: can addd gradinet boost hyperparametrs
    gs = GridSearchCV(estimator=pipe, param_grid=params_grid,
                      cv=StratifiedKFold(n_splits=5, random_state=42), n_jobs=1,
                      return_train_score=True)
    gs.fit(data, y)
    scores = pd.DataFrame(gs.cv_results_)
    print(scores[['params', 'mean_test_score', 'mean_train_score']])
    # Best parameters obtained with GridSearchCV:
    print(gs.best_params_)

    joblib.dump(gs, MODEL_PATH)
    #: run the best model maybe need to create test separate dataset
    # gs_best = gs.best_estimator_
    # new_scores = cross_val_score(gs_best, data, y, cv=skf)
    # print('Cross-validation accuracy score (with optimized parameters) = %1.3f '
    #       '(+/- %1.5f)' % (np.mean(new_scores), np.std(new_scores)))
    return pipe


def createInitialModel():
    epochs, raw = preprocess()
    labels = epochs.events[:, -1]
    # get MEG and EEG data
    epochs_data_train = epochs.get_data()
    pipe = train_mne_feature(epochs_data_train, labels, raw)
    transformed_data = pipe["fe"].fit_transform(
        epochs_data_train)  #: transformed_data is matrix dim by the features X events
    return pipe, epochs_data_train

