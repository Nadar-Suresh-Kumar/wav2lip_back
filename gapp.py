from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_cors import CORS
import logging

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for the app

# MongoDB setup using the connection string from the .env file
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Check MongoDB connection on app startup
try:
    client.server_info()  # Triggers a call to MongoDB to test the connection
    logger.info("Connected to MongoDB successfully.")
except Exception as e:
    logger.error(f"Connection to MongoDB failed: {e}")

# MongoDB collections
db = client['number']
collection = db['login']


@app.route('/')
def home():
    return "Welcome to the Flask App", 200


# Route to explicitly check MongoDB connection status
@app.route('/check_mongo', methods=['GET'])
def check_mongo():
    try:
        client.server_info()  # Triggers a call to MongoDB to test the connection
        return jsonify({"status": "success", "message": "Connected to MongoDB successfully."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Connection to MongoDB failed: {e}"}), 500


# Function to validate the input data
def validate_input(data):
    username = data.get('username')
    phone_number = data.get('phone_number')

    # Ensure both fields are provided and not empty
    if not username or not phone_number:
        return False, "Both username and phone_number are required."

    # Optionally, you can add more validation (e.g., phone number or email validation)
    return True, None


@app.route('/submit', methods=['POST'])
@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Parse the incoming request
        data = request.json
        logger.info(f"Received data: {data}")

        # Strip spaces from input
        data['username'] = data['username'].strip() if 'username' in data else None
        data['phone_number'] = data['phone_number'].strip() if 'phone_number' in data else None

        # Validate the input data
        is_valid, error_message = validate_input(data)
        if not is_valid:
            logger.warning(f"Invalid data: {error_message}")
            return jsonify({"status": "error", "message": error_message}), 400

        # Prepare the data to be inserted
        user_data = {'username': data['username'], 'phone_number': data['phone_number'], 'visited': False}

        # Insert data into MongoDB
        collection.insert_one(user_data)
        logger.info(f"Data inserted successfully: {user_data}")

        return jsonify({"status": "success"}), 200

    except Exception as e:
        logger.error(f"Failed to process request: {e}")
        return jsonify({"status": "error", "message": "Failed to process request."}), 500



if __name__ == '__main__':
    # Run the app, and Flask will handle multiple requests
    app.run(debug=True)
