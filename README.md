
# Churn Prediction API

This repository provides an API for predicting customer churn based on various customer data points. The model analyzes the data and predicts whether a customer is likely to churn or not.

## API Endpoints

### 1. **Predict Churn**

#### Endpoint: `/predict`
- **Method**: `POST`
- **Description**: This endpoint accepts customer data, processes it through the churn prediction model, and returns whether the customer is predicted to churn or not.

#### Request Body:
The data should be sent as a JSON object with the following fields:

| Field              | Type     | Description                                        |
|--------------------|----------|----------------------------------------------------|
| `gender`           | string   | Customer gender: 'Male' or 'Female'                |
| `SeniorCitizen`    | boolean  | Whether the customer is a senior citizen (1 = Yes, 0 = No) |
| `Partner`          | boolean  | Whether the customer has a partner (1 = Yes, 0 = No) |
| `Dependents`       | boolean  | Whether the customer has dependents (1 = Yes, 0 = No) |
| `tenure`           | integer  | The number of months the customer has been with the service |
| `PhoneService`     | boolean  | Whether the customer has phone service (1 = Yes, 0 = No) |
| `MultipleLines`    | boolean  | Whether the customer has multiple lines (1 = Yes, 0 = No) |
| `InternetService`  | string   | Type of internet service: 'DSL', 'Fiber optic', or 'No' |
| `OnlineSecurity`   | boolean  | Whether the customer has online security (1 = Yes, 0 = No) |
| `OnlineBackup`     | boolean  | Whether the customer has online backup (1 = Yes, 0 = No) |
| `TechSupport`      | boolean  | Whether the customer has tech support (1 = Yes, 0 = No) |
| `Contract`         | string   | Type of contract: 'Month-to-month', 'One year', 'Two year' |
| `PaperlessBilling` | boolean  | Whether the customer has paperless billing (1 = Yes, 0 = No) |
| `PaymentMethod`    | string   | Payment method: 'Electronic check', 'Mailed check', 'Bank transfer' |
| `MonthlyCharges`   | float    | The amount the customer is charged monthly |
| `TotalCharges`     | float    | The total amount the customer has paid over time |

#### Example Request:
```json
{
  "gender": "Male",
  "SeniorCitizen": 1,
  "Partner": 0,
  "Dependents": 0,
  "tenure": 1,
  "PhoneService": 1,
  "MultipleLines": 0,
  "InternetService": "Fiber optic",
  "OnlineSecurity": 0,
  "OnlineBackup": 0,
  "TechSupport": 0,
  "Contract": "Month-to-month",
  "PaperlessBilling": 1,
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 120.0,
  "TotalCharges": 120.0
}
```

#### Example Response:
```json
{
  "prediction": 1,
  "message": "Churn predicted"
}
```
- **`prediction`**: 1 indicates churn, 0 indicates no churn.
- **`message`**: Provides a brief message regarding the prediction.

---

### 2. **Health Check**

#### Endpoint: `/health`
- **Method**: `GET`
- **Description**: This endpoint checks if the API is running and healthy. It can be used for monitoring or debugging.

#### Request Body: None

#### Example Response:
```json
{
  "status": "OK",
  "message": "Service is up and running"
}
```

---




#### Example Response:
```json
{
  "model_version": "v1.0",
  "features": [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "TechSupport",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges"
  ]
}
```

---


---



---

## Interacting with the API

To interact with the API:

1. **Send a POST request** to `/predict` with customer data in JSON format.
2. **Check the prediction** in the response. If the prediction is `1`, the customer is predicted to churn; if it is `0`, they are predicted to stay.
3. Optionally, you can use the `/health` and `/metadata` endpoints to check the service status or retrieve model metadata.

This API provides a simple, effective way to integrate churn prediction into your application or service.


## Deployment

The API is deployed and can be accessed at [https://custormer-churn.onrender.com/](https://custormer-churn.onrender.com/).
