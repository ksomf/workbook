import pickle

with open('model1.bin', 'rb') as f_in:  
    model = pickle.load(f_in)
	
with open('dv.bin', 'rb') as f_in:  
	dv = pickle.load(f_in)

def predict(customer):
	X = dv.transform([customer])
	y_pred = model.predict_proba(X)[0, 1]
	churn = y_pred >= 0.5

	result = {
		'churn_probability': y_pred,
		'churn': churn
	}
	return result

if __name__ == "__main__":
	print(predict({"contract": "two_year", "tenure": 12, "monthlycharges": 19.7}))
