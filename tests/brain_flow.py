import argparse
import time
import numpy as np
import mne
import brainflow
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
import matplotlib
matplotlib.use('TkAgg')

board_id = BoardIds.CYTON_DAISY_BOARD.value
BoardShim.enable_dev_board_logger()
params = BrainFlowInputParams()
params.ip_port = 0
params.serial_port = 'com3'
board = BoardShim(board_id,params)
board.prepare_session()
eeg_channels = BoardShim.get_eeg_channels(board_id)

board.start_stream() # use this for default options
# board.start_stream(45000)
time.sleep(10)
# data = board.get_current_board_data (256) # get latest 256 packages or less, doesnt remove them from internal buffer
all_data = []
print(board.get_board_id())
print(eeg_channels)
ch_types = ['eeg'] * len(eeg_channels)
ch_names = BoardShim.get_eeg_names(board_id)
sfreq = BoardShim.get_sampling_rate(board_id)

info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)


# for _ in range(20):
#     data = board.get_board_data()  # get all data and remove it from internal buffer
#     eeg_data = data[eeg_channels, :]
#     eeg_data = eeg_data / 1000000  # BrainFlow returns uV, convert to V for MNE
#
#     all_data.append(eeg_data)


for i in range(10):
    time.sleep(1)
    board.insert_marker(i + 1)

time.sleep(3)
data = board.get_board_data()
# eeg_data = data[eeg_channels, :]
# eeg_data = eeg_data / 1000000
# board.stop_stream()
# board.release_session()
#
# # all_data = np.concatenate(all_data,axis=1)
# raw = mne.io.RawArray(eeg_data, info)
#
#
# raw.plot_psd(average=False)
# raw.plot(duration=5, n_channels=16)


