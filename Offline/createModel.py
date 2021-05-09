# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 21:38:29 2020

@author: oxenb
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy
import numpy as np
import scipy.io
from mne_features.feature_extraction import FeatureExtractor
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import (GridSearchCV, cross_val_score,
                                     StratifiedKFold)
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, StackingClassifier
from mne import Epochs, pick_types, events_from_annotations
import mne
from scipy import signal

from sklearn.svm import SVC, LinearSVC

DATA_PATH = "data/"
EXP_NAME = DATA_PATH+"or_SSVEP_1_raw.fif" ## file name to run the anaylsis on
FS = 125 # sampling rate
T = 1/FS # sample time
tmin, tmax = 1.2, 5

cutoff = [4,40] # take the frq band from here

features = ['app_entropy', 'decorr_time', 'higuchi_fd',
            'hjorth_complexity', 'hjorth_complexity_spect', 'hjorth_mobility',
            'hjorth_mobility_spect', 'hurst_exp', 'katz_fd', 'kurtosis',
            'line_length', 'mean', 'ptp_amp', 'samp_entropy',
            'skewness', 'spect_edge_freq', 'spect_entropy', 'spect_slope',
            'std', 'svd_entropy', 'svd_fisher_info', 'teager_kaiser_energy',
            'variance', 'wavelet_coef_energy', 'zero_crossings', 'max_cross_corr',
            'nonlin_interdep', 'phase_lock_val', 'spect_corr', 'time_corr']



def preprocess():
    # assuming zero means the instant moment when the cue starts
    # blinking to let the subject know which direction to do the MI, and blink duration is 1 sec

    raw = mne.io.read_raw_fif(EXP_NAME, preload=True)

    raw.filter(None, 40., fir_design='firwin', skip_by_annotation='edge')
    
    events = mne.find_events(raw, 'STI')
    
    picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                       exclude='bads')
    
    
    event_id = {"1": 1, "2": 2, "3": 3,"4": 4, "5": 5, "6": 6,"7": 7, "8": 8, "9": 9}
    
    epochs = Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks,
                    baseline=None, preload=True)
    epochs.pick_types(eeg=True, exclude='bads')  # remove stim and EOG

    return epochs,raw

# TODO add function the get power band features
def power_band(arr):
    """Median filtered signal as features.

    Parameters
    ----------
    arr : ndarray, shape (n_channels, n_times)

    Returns
    -------
    output : (n_channels * n_times,)
    """
    times_index = [[1,2]]

    len_eeg = len(arr[0])

    freqs, times, spectrogram = signal.spectrogram(arr, fs=125,nperseg = 32)

    time_signal = np.linspace(tmin, tmax, len(times), endpoint=False)
    power_band = []
    for index in range(len(cutoff)-1):
        for time_index in times_index:

            chosen_times = np.where((time_signal > time_index[0]) & (time_signal < time_index[1]))[0]
            chosen_freq = np.where((freqs > cutoff[index]) & (freqs < cutoff[index + 1]))[0]
            spectrogram_area = spectrogram[:,chosen_freq,:].T

            # arr_sample = arr[:2,chosen_times] # we choose 2 first chs
            # f = np.linspace(0, FS, len(arr_sample), endpoint=False)
            # fft = scipy.fft.fft(arr_sample)
            # chosen_freq = np.where((f > cutoff[index]) & (f < cutoff[index + 1]))[0]
            # fft_chosen_freq = fft[:, chosen_freq]
            power_band.extend(spectrogram_area.flatten())

    power_band = np.array(power_band)
    return np.array(power_band)


def train_mne_feature(data,labels,raw = None,sfreq = None):
    if not sfreq:

        sfreq = raw.info['sfreq']

    pipe = Pipeline([('fe', FeatureExtractor(sfreq = sfreq,
                                         selected_funcs = selected_features)),
                 ('scaler', StandardScaler()),
                 ('clf', SGDClassifier())])
    y = labels

    # params_grid = {'fe__app_entropy__emb': np.arange(2, 5)} #: can addd gradinet boost hyperparametrs
    params_grid = {"clf__penalty": ["l1","l2"], "clf__alpha" : [0.002,0.003,0.004,0.005,0.01,0.1],
                   "clf__max_iter" : [100,200,300,400,500,1000]} #: can addd gradinet boost hyperparametrs

    # params_grid = {} #: can addd gradinet boost hyperparametrs

    gs = GridSearchCV(estimator=pipe, param_grid=params_grid,
                      cv=StratifiedKFold(n_splits=5), n_jobs=1,
                      return_train_score=True,verbose=10)
    gs.fit(data, y)


    scores = pd.DataFrame(gs.cv_results_)
    print(scores[['params', 'mean_test_score', 'mean_train_score']])
    # Best parameters obtained with GridSearchCV:
    print(gs.best_params_)


    #: run the best model maybe need to create test seprate dataset
    # gs_best = gs.best_estimator_
    # new_scores = cross_val_score(gs_best, data, y, cv=skf)

    # print('Cross-validation accuracy score (with optimized parameters) = %1.3f '
    #       '(+/- %1.5f)' % (np.mean(new_scores), np.std(new_scores)))

    return pipe,scores

def train_mne_feature_stack(data,labels,raw):
    n_estimators = [50, 200]
    max_depth = [4]
    solvers = ['newton-cg', 'lbfgs', 'liblinear']
    penalty = ['l2']
    c_values = [100, 10, 1.0, 0.1, 0.01]

    estimators = [
        ('rf', RandomForestClassifier(n_estimators=10, random_state=42)),
        ('SGD',SGDClassifier())]
    clf = StackingClassifier(
        estimators=estimators, final_estimator=LogisticRegression()
    )
    pipe = Pipeline([('fe', FeatureExtractor(sfreq=raw.info['sfreq'],
                                             selected_funcs=selected_features)),
                     ('scaler', StandardScaler()),
                     ('clf', clf)])
    params_grid = {"clf__SGD__penalty": ["l1", "l2"], "clf__SGD__alpha": [0.003, 0.004],
                   "clf__SGD__max_iter": [100, 200, 300, 400, 500], "clf__rf__n_estimators" : n_estimators,
                   "clf__rf__max_depth" :max_depth, "clf__final_estimator__solver" : solvers,
                   "clf__final_estimator__penalty" : penalty,"clf__final_estimator__C" : c_values}
    gs = GridSearchCV(estimator=pipe, param_grid=params_grid,
                      cv=StratifiedKFold(n_splits=5),
                      return_train_score=True, verbose=10)
    gs.fit(data, labels)
    scores = pd.DataFrame(gs.cv_results_)
    print(scores[['params', 'mean_test_score', 'mean_train_score']])
    # Best parameters obtained with GridSearchCV:
    print(gs.best_params_)

    return pipe,scores


# TODO add power band
# https://mne.tools/mne-features/auto_examples/plot_user_defined_function.html#sphx-glr-auto-examples-plot-user-defined-function-py
# selected_features = [("my_func",compute_medfilt),"mean",'kurtosis','skewness'] # can be cgahnged to any feature


selected_features = [('power_band', power_band)] # can be changed to any feature

# selected_features = ["mean",'kurtosis','skewness',('power_band', compute_medfilt)] # can be cgahnged to any feature

def read_from_mat():
    '''
    we create epochs object that will contain the left and the
    right epochs from the mat file.

    for left we mark 0, for right we mark 1

    :return:
    '''
    mat_left = scipy.io.loadmat(f'{DATA_PATH}left_data.mat')['leftData']
    mat_right = scipy.io.loadmat(f'{DATA_PATH}right_data.mat')['rightData']
    labels = [0]*len(mat_left) + [1]*len(mat_right)

    epochs = np.concatenate((mat_left, mat_right), axis=0)

    return epochs,labels

def main():
    epochs,raw =  preprocess()
    #
    #
    labels = epochs.events[:, -1]
    #
    # # get MEG and EEG data
    epochs_data_train = epochs.get_data()

    # epochs_data_train, labels = read_from_mat()

    pipe,scores = train_mne_feature(epochs_data_train,labels,sfreq = 128)
    
    transformed_data = pipe["fe"].fit_transform(epochs_data_train) #: transformed_data is matrix dim by the featuhers X events

    joblib.dump(pipe, "../")

    return pipe,transformed_data,scores

if __name__ == '__main__':
    pipe,transformed_data,scores = main()
    
