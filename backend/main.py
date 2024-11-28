from flask import Flask, request, jsonify
from chat_handler import GeminiChatHandler
from chat_schema import *
import copy

# Initialize flask app
app = Flask(__name__)

chat_handler = GeminiChatHandler()
        

@app.route("/api/gemini/request", methods=['POST'])
def handle_user_request():
    data = request.json
    user_input = data.get("prompt", "")

    if not user_input:
        return jsonify("Prompt is required"), 400
    
    response, status_code = chat_handler.send_message(user_input)
    return jsonify(response), status_code


@app.route("/api/gemini/new_chat", methods=['POST'])
def start_new_chat():
        response, status_code = chat_handler.start_new_chat()
        print("New Session ID: ", response)
        return jsonify(response), status_code


@app.route("/api/gemini/load_chat", methods=['POST'])
def load_chat():
    data = request.json
    session_id = data.get("sessionId", "")
    
    if not session_id:
        return jsonify("Session ID is required"), 400
    
    response, status_code = chat_handler.load_chat(session_id)
    return jsonify(response), status_code



@app.route("/api/gemini/current_session_id", methods=['GET'])
def get_current_session_id():
    session_id = chat_handler.get_current_session_id()
    return jsonify(session_id), 200


@app.route("/api/gemini/all_chat_summaries", methods=['GET'])
def get_all_chat_summaries():
    all_chats = copy.deepcopy(chat_handler.get_all_chats()) # create a copy of handler's all_chats
    chat_summaries = [{"sessionId": chat.sessionId, "summary": chat.summary, "timestamp": chat.timestamp} for chat in all_chats.chats.values()]
    
    return jsonify(chat_summaries), 200

@app.route("/api/gemini/delete_chats", methods=['DELETE'])
def delete_chats():
    data = request.json
    session_ids = data.get("sessionIds", "")
    
    if not session_ids:
        return jsonify("Session ID is required"), 400
    
    response, status_code = chat_handler.delete_chats(session_ids)
    return jsonify(response), status_code

# TODO: Is this needed? Or should this be called server-side?
@app.route("/api/gemini/close", methods=['POST'])
def close_app():
    """
    Call this function when mobile app is closed. The server will figure out which chat sessions were updated,
    generate new summaries, and then save all chats to a file. 
    
    Returns a list of sessions that were updated.
    """
    print("closing handler")
    response, status_code = chat_handler.close_handler()
    
    if status_code != 200:
        print(f"Something went wrong when closing the handler.\nError {status_code}: {response}")
        
    return jsonify(response), status_code
    
    

if __name__ == "__main__":
    app.run(debug=True); # for testing and debugging
    # app.run(host="0.0.0.0", port=8080) # google expects app to run on port 8080