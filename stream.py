import time
from click import prompt
from colorama import Back
import streamlit as st
import base64
from chatbot.interactive import interactiveChat
from chatbot.context_logger import ContextLogger
from dotenv import load_dotenv
import os
import assemblyai as aai
import speech_recognition as spr
from speechRecognition.sr import SpeakerVerification
from scipy.io.wavfile import write
from speechRecognition.listen import BackgroundAudioRecorder
import multiprocessing

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
local_image = ""
filelike = None
user = "Yodha"
userbio = "Your creator. Male, 5th semester college student, have pretty good knowledge in machine learning and AI. Loves to watch anime and of course a weeb"
char = "RIN-207 (Responsive Intelligence Nexus)"
nickname = "Rin"
input_audio_path = "speechRecognition/recorded.wav"

# Initialize chatbot
chat = interactiveChat(user=user, bio=userbio, char=char, charnickname=nickname)
recog = spr.Recognizer()
listener = BackgroundAudioRecorder(silence_timeout=1)

def encode_image(image_path):
    # with open(image_path, "rb") as image_file:
    return base64.b64encode(image_path.read()).decode('utf-8')
listener.start_listening(chat, api=api_key, filelike=None)