import joblib
import os

path = os.path.abspath(__file__)
folder = os.path.dirname(path)

model = joblib.load(os.path.join(folder, "model_weights.joblib"))
