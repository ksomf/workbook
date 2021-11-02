import pickle

import numpy as np

from flask import Flask, request, jsonify
import xgboost as xgb

model_file = 'model.bin'

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

app = Flask('churn')

@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()

    X = dv.transform([customer])
    d = xgb.DMatrix(X,feature_names=dv.get_feature_names())
    y_pred = model.predict(d)

    result = {
        'predicted_salary': np.expm1(y_pred).tolist()[0]
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
