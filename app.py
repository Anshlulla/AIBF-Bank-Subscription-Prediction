from flask import Flask, request, jsonify, render_template
from src.utils.utils import *
import pandas as pd

MODEL_PATH = r"artifacts/model_trainer/model/model.pkl"

app = Flask(__name__)
model = load_pickle(MODEL_PATH)

def predict_single(model, input_data: dict):
    # Convert to DataFrame
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]
    return prediction

@app.route('/')
def home():
    return render_template("index.html")  # Optional form UI

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.get_json()
        
        # Load trained model
        model = load_pickle("artifacts/model_trainer/model/model.pkl")

        # Define expected columns
        expected_cols = [
            'age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous',
            'job_blue-collar', 'job_entrepreneur', 'job_housemaid', 'job_management',
            'job_retired', 'job_self-employed', 'job_services', 'job_student',
            'job_technician', 'job_unemployed', 'job_unknown',
            'marital_married', 'marital_single',
            'education_secondary', 'education_tertiary', 'education_unknown',
            'default_yes', 'housing_yes', 'loan_yes',
            'contact_telephone', 'contact_unknown',
            'month_aug', 'month_dec', 'month_feb', 'month_jan', 'month_jul',
            'month_jun', 'month_mar', 'month_may', 'month_nov', 'month_oct', 'month_sep',
            'poutcome_other', 'poutcome_success', 'poutcome_unknown'
        ]

        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])

        # Add missing columns with 0
        for col in expected_cols:
            if col not in input_df.columns:
                input_df[col] = 0

        # Reorder columns
        input_df = input_df[expected_cols]

        # Predict
        prediction = model.predict(input_df)[0]
        return jsonify({'prediction': int(prediction)})
    
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run(debug=True)
