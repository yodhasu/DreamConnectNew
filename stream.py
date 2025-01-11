from chatbot.interactive import interactiveChat
from dotenv import load_dotenv
import os
import speech_recognition as spr
from speechRecognition.listen import ListenToPrompt
import threading
from streamScreen.capsc import streamsc

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
local_image = ""
filelike = None
user = "Yodha"
userbio = "Your creator. Male, 5th semester college student,5 have pretty good knowledge in machine learning and AI. Loves to watch anime and of course a weeb"
char = "RIN-207 (Responsive Intelligence Nexus)"
nickname = "Rin"
input_audio_path = "speechRecognition/recorded.wav"

# Initialize chatbot
chat = interactiveChat(user=user, bio=userbio, char=char, charnickname=nickname)
recog = spr.Recognizer()
listener = ListenToPrompt(silence_timeout=5)


capture_proc = threading.Thread(target=streamsc)
listen_proc = threading.Thread(target=listener.start_listening, args=(chat, api_key, None))

capture_proc.start()
listen_proc.start()

capture_proc.join()
listen_proc.join()
# listener.start_listening(chat, api=api_key, filelike=None)