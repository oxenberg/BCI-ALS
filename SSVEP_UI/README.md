# SSVEP_UI

To initialize the UI, you need to run "online_UI_main.py"
 from it's directory.
 
 This will create a window containing a number of buttons to choose from.
 To make a choice we use the computer mouse (clicking twice as default, can be changed at self.choiceTH in MainWindow).
 
 The content and the number of the buttons is set according to a JSON file with decision tree (built using dictionary inside dictionary).
 The current JSON file is named "online_UI_example".
 
 The buttons are flickering but this is not enough for SSVEP stimuli (as we found out). The current flickering settings are at "params_offline.JSON" together with the positions settings.
 