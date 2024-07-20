import joblib
import numpy as np

loaded_model = joblib.load('power_prediction.sav')
scale_model = joblib.load('scaler.pkl')

X_single = np.array([[416.328908,5.311336]])
x_single1 = scale_model.transform(X_single)
print(x_single1)

prediction = loaded_model.predict(x_single1)

print("Prediction for x =", X_single, ":", prediction)
