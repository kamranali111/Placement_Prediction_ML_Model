from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load the model
with open('Placement_Prediction.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return "Placement Prediction Model API"

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input features from the request
    data = request.json
    df = pd.DataFrame([data])
    
    # Predict using the model
    prediction = model.predict(df)[0]

    return jsonify({'prediction': int(prediction)})

if __name__ == "__main__":
    app.run(debug=True)
