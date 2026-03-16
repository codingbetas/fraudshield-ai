from sklearn.ensemble import IsolationForest
import numpy as np

model = IsolationForest(contamination=0.05)

def detect_anomaly(features):

    # prediction = model.predict(np.array(features).reshape(1, -1))

    # return prediction[0] == -1

    return False