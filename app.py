from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import pickle
import os

# Flask application setup
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for CSRF protection with Flask-WTF forms

# Load the pre-trained model
with open("model2.pkl", "rb") as file:
    model = pickle.load(file)

# Churn prediction form
class ChurnPredictionForm(FlaskForm):
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    SeniorCitizen = SelectField('Senior Citizen', choices=[('0', 'No'), ('1', 'Yes')], validators=[DataRequired()])
    Partner = SelectField('Partner', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    Dependents = SelectField('Dependents', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    tenure = IntegerField('Tenure (months)', validators=[DataRequired(), NumberRange(min=0)])
    PhoneService = SelectField('Phone Service', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    MultipleLines = SelectField('Multiple Lines', choices=[('Yes', 'Yes'), ('No', 'No'), ('No phone service', 'No phone service')], validators=[DataRequired()])
    InternetService = SelectField('Internet Service', choices=[('DSL', 'DSL'), ('Fiber optic', 'Fiber optic'), ('No', 'No')], validators=[DataRequired()])
    OnlineSecurity = SelectField('Online Security', choices=[('Yes', 'Yes'), ('No', 'No'), ('No internet service', 'No internet service')], validators=[DataRequired()])
    OnlineBackup = SelectField('Online Backup', choices=[('Yes', 'Yes'), ('No', 'No'), ('No internet service', 'No internet service')], validators=[DataRequired()])
    TechSupport = SelectField('Tech Support', choices=[('Yes', 'Yes'), ('No', 'No'), ('No internet service', 'No internet service')], validators=[DataRequired()])
    Contract = SelectField('Contract', choices=[('Month-to-month', 'Month-to-month'), ('One year', 'One year'), ('Two year', 'Two year')], validators=[DataRequired()])
    PaperlessBilling = SelectField('Paperless Billing', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    PaymentMethod = SelectField('Payment Method', choices=[
        ('Electronic check', 'Electronic check'),
        ('Mailed check', 'Mailed check'),
        ('Bank transfer (automatic)', 'Bank transfer (automatic)'),
        ('Credit card (automatic)', 'Credit card (automatic)')
    ], validators=[DataRequired()])
    MonthlyCharges = FloatField('Monthly Charges', validators=[DataRequired(), NumberRange(min=0)])
    TotalCharges = FloatField('Total Charges', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Predict Churn')

# Home route with form rendering and prediction
@app.route("/", methods=["GET", "POST"])
def predict_churn():
    form = ChurnPredictionForm()
    prediction = None

    if form.validate_on_submit():  # When the form is submitted and validated
        try:
            # Collect form data into a dictionary
            form_data = {
                'gender': form.gender.data,
                'SeniorCitizen': form.SeniorCitizen.data,
                'Partner': form.Partner.data,
                'Dependents': form.Dependents.data,
                'tenure': form.tenure.data,
                'PhoneService': form.PhoneService.data,
                'MultipleLines': form.MultipleLines.data,
                'InternetService': form.InternetService.data,
                'OnlineSecurity': form.OnlineSecurity.data,
                'OnlineBackup': form.OnlineBackup.data,
                'TechSupport': form.TechSupport.data,
                'Contract': form.Contract.data,
                'PaperlessBilling': form.PaperlessBilling.data,
                'PaymentMethod': form.PaymentMethod.data,
                'MonthlyCharges': form.MonthlyCharges.data,
                'TotalCharges': form.TotalCharges.data
            }

            # Preprocess the input data
            processed_data = preprocess_input(form_data)

            # Make prediction using the model
            prediction = model.predict([processed_data])[0]
            prediction = "Churn" if prediction == 1 else "No Churn"

        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template("index.html", form=form, prediction=prediction)

# Preprocess user input for the machine learning model
def preprocess_input(data):
    """
    Preprocess user input for the machine learning model.

    Args:
        data (dict): A dictionary containing user input.

    Returns:
        list: A list of processed input features ready for prediction.
    """
    # Define mappings for categorical data
    gender_mapping = {'Male': 0, 'Female': 1}
    yes_no_mapping = {'Yes': 1, 'No': 0}
    internet_service_mapping = {'DSL': 0, 'Fiber optic': 1, 'No': 2}
    contract_mapping = {'Month-to-month': 0, 'One year': 1, 'Two year': 2}
    payment_method_mapping = {
        'Electronic check': 0,
        'Mailed check': 1,
        'Bank transfer (automatic)': 2,
        'Credit card (automatic)': 3
    }

    # Convert input fields using mappings
    processed_data = [
        gender_mapping[data['gender']],
        int(data['SeniorCitizen']),  # Already 0 or 1
        yes_no_mapping[data['Partner']],
        yes_no_mapping[data['Dependents']],
        int(data['tenure']),  # Integer field
        yes_no_mapping[data['PhoneService']],
        {'Yes': 1, 'No': 0, 'No phone service': 2}[data['MultipleLines']],
        internet_service_mapping[data['InternetService']],
        {'Yes': 1, 'No': 0, 'No internet service': 2}[data['OnlineSecurity']],
        {'Yes': 1, 'No': 0, 'No internet service': 2}[data['OnlineBackup']],
        {'Yes': 1, 'No': 0, 'No internet service': 2}[data['TechSupport']],
        contract_mapping[data['Contract']],
        yes_no_mapping[data['PaperlessBilling']],
        payment_method_mapping[data['PaymentMethod']],
        float(data['MonthlyCharges']),  # Float field
        float(data['TotalCharges'])    # Float field
    ]

    return processed_data

if __name__ == "__main__":
    app.run()
