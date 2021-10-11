import pickle

from flask import Flask
from flask import request
from flask import jsonify

with open('model2.bin', 'rb') as f_in:  
    model = pickle.load(f_in)
	
with open('dv.bin', 'rb') as f_in:  
	dv = pickle.load(f_in)

app = Flask('churn')

@app.route('/predict', methods=['POST'])
def predict():
	customer = request.get_json()

	X = dv.transform([customer])
	y_pred = model.predict_proba(X)[0, 1]
	churn = y_pred >= 0.5

	result = {
		'churn_probability': float(y_pred),
		'churn': bool(churn)
	}
	return jsonify(result)

if __name__ == "__main__":
	#print(predict({"contract": "two_year", "tenure": 12, "monthlycharges": 19.7}))
	app.run(debug=True, host='0.0.0.0', port=9696)
