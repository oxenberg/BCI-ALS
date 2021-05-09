import json


freqs = [37.0, 31.0, 29.0, 23.0, 19.0, 17.0, 13.0, 11.0, 7.0]


def read_json(name='onlineUI.JSON'):
    params_file = open(name, )
    params = json.load(params_file)
    return params


def frequencyToLabel(freq):
    return freqs.index(freq) + 1


def labelToFrequency(label):
    return freqs[label - 1]
