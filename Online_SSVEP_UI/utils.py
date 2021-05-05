import json


def read_tree(name='onlineUI.JSON'):
    params_file = open(name, )
    params = json.load(params_file)
    return params