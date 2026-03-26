import os
import json
import pickle
import numpy as np
from typing import Optional, Tuple, Dict


class MLModel:
    def __init__(self, model_path: str, report_path):
        self.model_path = model_path
        self.report_path = report_path
        self.model = None
        self.report = None
        self.class_names = ["setosa", "versicolor", "virginica"]


    def load_model(self):
    
        if not os.path.exists(self.model_path):
            raise FileNotFoundError("Le chemin du model est incorrect")

        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)

        with open(self.report_path, "r") as f:
                self.report = json.load(f)

    def predict(self, features: np.ndarray):
        if self.model is None:
            raise RuntimeError("Problème avec le model")

        pred_idx = self.model.predict(features)[0]
        probs = self.model.predict_proba(features)[0]

        prediction_class = self.class_names[pred_idx]
        confidence = float(probs[pred_idx])

        probs_dict = {
            self.class_names[i]: float(probs[i])
            for i in range(len(self.class_names))
        }

        return prediction_class, confidence, probs_dict

    def get_accuracy(self) -> Optional[float]:
        if self.report:
            return self.report["accuracy_score"]
        return None

if __name__ == "__main__":

    model = MLModel(model_path="./models/model.pkl", report_path="./models/training_report.json")
    model.load_model()
    print(model.get_accuracy())