from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for the app

# MongoDB setup using the connection string from the .env file
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)


# Check MongoDB connection on app startup
try:
    client.server_info()  # Triggers a call to MongoDB to test the connection
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Connection to MongoDB failed: {e}")

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

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    print("Received data:", data)  # Debug print to check received data
    username = data.get('username')
    phone_number = data.get('phone_number')

    if username and phone_number:
        # Storing data in MongoDB
        user_data = {'username': username, 'phone_number': phone_number,'visited': False}
        try:
            collection.insert_one(user_data)
            print("Data inserted successfully:", user_data)  # Debug print to confirm insertion
            return jsonify({"status": "success"}), 200
        except Exception as e:
            print(f"Failed to insert data: {e}")
            return jsonify({"status": "error", "message": "Failed to insert data"}), 500
    else:
        print("Invalid data received.")  # Debug print for invalid data
        return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(debug=True)
