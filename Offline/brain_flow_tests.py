
from brainflow.board_shim import BoardShim, BoardIds
import mne
eeg_channels_num = 16

board_id = BoardIds.CYTON_DAISY_BOARD.value

ch_names = BoardShim.get_eeg_names(board_id)

print(ch_names)
