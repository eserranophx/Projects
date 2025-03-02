# Flask - this app script integrates with frontend deployments and is useful for handeling Mesh functions
from flask import Flask, render_template, jsonify
import os
import requests
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

MESH_API_URL = os.getenv("MESH_API_URL")
MESH_CLIENT_ID = os.getenv("MESH_CLIENT_ID")
MESH_CLIENT_SECRET = os.getenv("MESH_CLIENT_SECRET")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/payment')
def payment():
    return render_template("payment.html")

@app.route('/get_link_token', methods=['POST'])
def get_link_token():
    headers = {
        "Content-Type": "application/json",
        "X-Client-Id": MESH_CLIENT_ID,
        "X-Client-Secret": MESH_CLIENT_SECRET
    }

    payload = {
        "userId": "Mesh",
        "integrationId": "", # Integration Here
        "transferOptions": {
        "amountInFiat": 50,
        "description": "",
        "toAddresses": [
                {
                    "address": "", # Wallet Address Here
                    "networkId": "", # Network ID Here
                    "symbol": "USDC"
                }
            ]
        }
    }

    response = requests.post(f"{MESH_API_URL}/api/v1/linktoken", json=payload, headers=headers)

    # Debug
    print("API Response:", response.status_code, response.text)

    # Decode
    if response.status_code == 200:
        data = response.json()
        encoded_url = data.get("content", {}).get("linkToken")

        if encoded_url:
            try:
                decoded_url = base64.b64decode(encoded_url).decode("utf-8")
                print(decoded_url) # Validate url is decoded properly
                return jsonify({"decodedLink": decoded_url}) # decodedLink for calling from site
            except Exception as e:
                return jsonify({"error": f"Error decoding linkToken: {str(e)}"}), 500
        else:
            return jsonify({"error": "No linkToken"}), 400
    else:
        return jsonify({"error": "Failed API Request", "statusCode": response.status_code, "response": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
