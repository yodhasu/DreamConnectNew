# from flask import Flask
# import time
# from flask_socketio import SocketIO, emit
# from Emo import sentanalysis  # Assuming you have a function to handle sentiment analysis

# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS for development

# last_action = None  # Store the last action to send it on reconnect

# @app.route('/')
# def index():
#     return "SocketIO Server Running"

# @socketio.on('connect')
# def handle_connect():
#     global last_action
#     # print("Client connected")
#     if last_action:
#         # Send the last action to the newly connected client
#         emit('model_action', {'action': last_action})
#         # print(f"Sent last action to frontend on connect: {last_action}")

# @socketio.on('disconnect')
# def handle_disconnect():
#     print("Client disconnected")

# def background_task():
#     global last_action
#     # while True:
#     action = sentanalysis()  # Your custom sentiment analysis logic
#     last_action = action  # Store the latest action for reconnects
#     socketio.emit('model_action', {'action': action})  # Emit the action to all connected clients
#     # print(f"Sent action to frontend: {action}")
#     time.sleep(1)  # Control loop timing (1 second delay here)

# if __name__ == '__main__':
#     # Start the background task in a non-blocking thread
#     socketio.start_background_task(target=background_task)  # Runs without blocking socketio.run

#     # Run the SocketIO server concurrently
#     socketio.run(app, host='127.0.0.1', port=9090)


# UPDATED. NOW USING CHATBOT

from flask import Flask, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import os
from flask_cors import CORS
import emotionmapping as ep

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode= 'threading')

emotion_map = ep.load_emotion_mapping("./emoclass.txt")

@app.route('/')
def index():
    return "SocketIO Server Running"

@app.route('/audio')
def get_audio():
    # Assuming the audio file is stored in the same directory as the Flask app
    # audio_path = os.path.join(app.root_path, "\speech.mp3")
    # print(audio_path)
    audio_path = get_latest_file("../../chatbot/voiceCloner/voice/Output")
    return send_file(audio_path, mimetype='audio/mpeg')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        emotion = data.get('response')
        
        if emotion == "reload":
            socketio.emit('model_action', {'action': emotion})
            print(f"Message: {emotion}\nsent!")
        else:
            narrowed = ep.narrow_emotions(emotion, emotion_map)
            
            top_emot = ep.get_most_frequent_emotion(narrowed)
            if emotion:
                socketio.emit('model_action', {'action': top_emot})
                print(f"Message: {top_emot}\nsent!")
                return jsonify({"status": "success"}), 200
            else:
                return jsonify({"status": "failed", "reason": "No emotion data provided"}), 400
    except Exception as e:
        return jsonify({"status": "error", "reason": str(e)}), 500

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

def get_latest_file(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if not files:
        return None
    
    files_with_mtime = [(f, os.path.getmtime(os.path.join(directory, f))) for f in files]
    sorted_files = sorted(files_with_mtime, key=lambda f: f[1], reverse=True)  # Sort by newest first
    
    latest_file = sorted_files[0][0]  # Get the latest file based on modification time
    return os.path.join(directory, latest_file)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=9090)
