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
from sklearn.svm import SVC, LinearSVC

DATA_PATH = "data/"
EXP_NAME = DATA_PATH+"Or_5_raw.fif" ## file name to run the anaylsis on
FS = 125 # sampling rate
T = 1/FS # sample time

cutoff = [0.5,4.0,7.0,12.0,30.0,45] # take the frq band from here

features = ['app_entropy', 'decorr_time', 'higuchi_fd',
            'hjorth_complexity', 'hjorth_complexity_spect', 'hjorth_mobility',
            'hjorth_mobility_spect', 'hurst_exp', 'katz_fd', 'kurtosis',
            'line_length', 'mean', 'ptp_amp', 'samp_entropy',
            'skewness', 'spect_edge_freq', 'spect_entropy', 'spect_slope',
            'std', 'svd_entropy', 'svd_fisher_info', 'teager_kaiser_energy',
            'variance', 'wavelet_coef_energy', 'zero_crossings', 'max_cross_corr',
            'nonlin_interdep', 'phase_lock_val', 'spect_corr', 'time_corr']



def preprocess():

    tmin, tmax = -1, 0.8 #: need to check the best
    
    raw = mne.io.read_raw_fif(EXP_NAME, preload=True)
    
    raw.filter(None, 40., fir_design='firwin', skip_by_annotation='edge')
    
    events = mne.find_events(raw, 'STI')
    
    picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                       exclude='bads')
    
    
    event_id = {'Left': 1, 'right': 2,'none': 3}
    
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
    len_eeg = len(arr[0])

    fft = scipy.fft.fft(arr)
    f = np.linspace(0, FS, len_eeg, endpoint=False)

    power_band = []
    for index in range(len(cutoff)-1):
        chosen_freq = np.where((f > cutoff[index]) & (f < cutoff[index + 1]))[0]
        fft_chosen_freq = fft[:, chosen_freq]
        power_band.append(abs(fft_chosen_freq.mean()))

    power_band = np.array(power_band)
    return np.array(power_band)


def train_mne_feature(data,labels,raw):
    pipe = Pipeline([('fe', FeatureExtractor(sfreq = raw.info['sfreq'],
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
                      return_train_score=True)
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
    n_estimators = [50, 100, 200]
    max_depth = [4, 5, 6]


    estimators = [
        ('rf', RandomForestClassifier(n_estimators=10, random_state=42)),
        ('SGD',SGDClassifier())]
    clf = StackingClassifier(
        estimators=estimators, final_estimator=LogisticRegression(),cv=5
    )
    pipe = Pipeline([('fe', FeatureExtractor(sfreq=raw.info['sfreq'],
                                             selected_funcs=selected_features)),
                     ('scaler', StandardScaler()),
                     ('clf', clf)])
    params_grid = {"clf__SGD__penalty": ["l1", "l2"], "clf__SGD__alpha": [0.002, 0.003, 0.004, 0.005, 0.01, 0.1],
                   "clf__SGD__max_iter": [100, 200, 300, 400, 500, 1000], "clf__rf__n_estimators" : n_estimators,
                   "clf__rf__max_depth" :max_depth}
    gs = GridSearchCV(estimator=pipe, param_grid=params_grid,
                      cv=StratifiedKFold(n_splits=5), n_jobs=1,
                      return_train_score=True)
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

def main():
    epochs,raw =  preprocess()
    
    
    labels = epochs.events[:, -1]

    # get MEG and EEG data
    epochs_data_train = epochs.get_data()
            
    pipe,scores = train_mne_feature_stack(epochs_data_train,labels,raw)
    
    transformed_data = pipe["fe"].fit_transform(epochs_data_train) #: transformed_data is matrix dim by the featuhers X events
    
    
    return pipe,transformed_data,scores

if __name__ == '__main__':
    pipe,transformed_data,scores = main()
    
