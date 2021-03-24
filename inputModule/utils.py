import json

def read_params():
    params_file = open('../params.JSON', )
    params = json.load(params_file)

    # fill more params with explanation
    uVolts_per_count = (4500000) / 24 / (2 ** 23 - 1)  # uV/count
    params["uVolts_per_count"] = uVolts_per_count
    return params