# BCI-ALS

### how to run SSVEP UI with the EEG

1. Turn on the EEG

2. To collect data run offline_UI_main.py in SSVEP_UI and to config params use the params_offline.JSON in the
father directory, please change the "EXP_NAME" param in the JSON to the name of your experiment.
   
3. The window of the UI doesn't close by himself, take a look while running the experiment in the console to see if 
the experiment finished
   
4. Run the createModel.py and change the EXP_NAME varible to the name you used in the params_offline.JSON 
"EXP_NAME" param
   
5. Yay you create the pickle, you can see him in the Model_Pipline directory with the name model_pip.pkl
please run the online_UI_main.py and start to gaze to the right option.
   
