import createModel
from os import path
import joblib


MODEL_PATH = "gsModel.pkl"


class PredictionModel:
    def __init__(self):
        if path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
        else:
            _, self.model = createModel.main()
            joblib.dump(self.model, MODEL_PATH)

    def updateModel(self, data, label):
        self.model.fit(data, label)
        joblib.dump(self.model, MODEL_PATH)

    def predict(self, data):
        label = self.model.predict(data)
        return label

