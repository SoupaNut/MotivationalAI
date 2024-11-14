from flask import Flask, request, jsonify
import google.generativeai as gemini
from dotenv import load_dotenv
import os

app = Flask(__name__)

MODEL_NAME = "gemini-1.5-flash"
load_dotenv('.env')

# Initialize the Google Gemini API client
gemini.configure(api_key=os.getenv("API_KEY"))

@app.route('/api/gemini', methods=['GET', 'POST'])
def handle_gemini_request():
    print("Received a request at /api/gemini")  # Log when the endpoint is hit

    # Get data from the incoming request
    data = request.json
    print("Request JSON data:", data)  # Log the data received

    user_prompt = data.get("prompt", "")

    # Make sure there is a prompt provided
    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # Call the Google Gemini API
        response = gemini.generate_content(
            model=MODEL_NAME,  # Replace with your specific Gemini model
            prompt=user_prompt
        )

        # Extract the response from Gemini
        gemini_response = response.text
        print("Gemini response:", gemini_response)  # Log the Gemini API response

        # Send the response back to the client
        return jsonify({"response": gemini_response}), 200

    except Exception as e:
        print("Error:", e)  # Log any exceptions
        # Handle errors
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
