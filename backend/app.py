from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from flask import jsonify

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the timeout configuration for your Flask app
app.config["TIMEOUT"] = 120  # 120 seconds (2 minutes)


@app.route("/api/query", methods=["POST"])
def process_query():
    try:
        data = request.get_json()
        form_data = data.get("formData")

        if not form_data:
            return jsonify({"error": "Query not provided"}), 400

        result = execute_query(form_data)
        print(result)
        # Assuming result is a string, you can modify this based on the actual output format
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def execute_query(form_data):
    # Load the CSV file
    df = pd.read_csv("Crop_recommendation.csv")

    # Separate features and labels
    X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]
    y = df["label"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train a model (RandomForestClassifier in this case)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train_scaled, y_train)

    # Prepare the form data for prediction
    N = form_data["nitrogen"]
    P = form_data["phosphorus"]
    K = form_data["potassium"]
    temp = form_data["temperature"]
    humidity = form_data["humidity"]
    ph = form_data["ph"]
    rainfall = form_data["rainfall"]

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)

    # Scale the input features
    single_pred_scaled = scaler.transform(single_pred)

    # Make a prediction
    prediction = model.predict(single_pred_scaled)

    # Map the prediction to a crop name
    crop_dict = {
        "rice": "Rice",
        "maize": "Maize",
        "jute": "Jute",
        "cotton": "Cotton",
        "coconut": "Coconut",
        "papaya": "Papaya",
        "orange": "Orange",
        "apple": "Apple",
        "muskmelon": "Muskmelon",
        "watermelon": "Watermelon",
        "grapes": "Grapes",
        "mango": "Mango",
        "banana": "Banana",
        "pomegranate": "Pomegranate",
        "lentil": "Lentil",
        "blackgram": "Blackgram",
        "mungbean": "Mungbean",
        "mothbeans": "Mothbeans",
        "pigeonpeas": "Pigeonpeas",
        "kidneybeans": "Kidneybeans",
        "chickpea": "Chickpea",
        "coffee": "Coffee",
    }

    crop = crop_dict.get(prediction[0], "Unknown")
    result = "{} is the best crop to be cultivated right there".format(crop)

    return result


if __name__ == "__main__":
    app.run(debug=False, port=5000, host="0.0.0.0")  # Run the Flask app in debug mode
