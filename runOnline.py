from inputModule import SignalReader


def runOnline():
    signalReader = SignalReader()
    signalReader.start_experiment()

if __name__ == '__main__':
    runOnline()