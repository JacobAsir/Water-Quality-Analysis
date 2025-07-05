import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
from chat import chatbot

# Load the SVM model
try:
    model = joblib.load("model.pkl")
except FileNotFoundError:
    print("Warning: model.pkl not found. Prediction functionality will not work.")
    model = None

def predict_potability(features):
    if model is None:
        return {"error": "Model not loaded"}
    
    # Convert input features to NumPy array
    input_data = np.array(features).reshape(1, -1)
    
    # Create and fit StandardScaler
    scaler = StandardScaler()
    # Note: In production, you should load a pre-fitted scaler
    scaler.fit(input_data)
    
    # Scale input data
    scaled_input_data = scaler.transform(input_data)
    
    # Make prediction
    prediction = model.predict(scaled_input_data)
    
    # Return prediction as integer (0 or 1)
    return int(prediction[0])

def get_chatbot_response(info, history, message, language="English"):
    try:
        response = chatbot(info, history, message, language)
        return response
    except Exception as e:
        return f"Error: {str(e)}"
