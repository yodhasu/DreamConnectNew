# from chatbot.interactive import interactiveChat
# from chatbot.context_logger import ContextLogger
# from dotenv import load_dotenv
# import os

# load_dotenv()

# api_key = os.getenv("GROQ_API_KEY")
# context_util = ContextLogger()

# user = "Yodha"
# userbio = "Your creator. Male, 5th semester college student, have pretty good knowledge in machine learning and AI. Loves to watch anime and of course a weeb"
# char = "March 7th"
# nickname = "March"
# context = "You are an AI made by me, you live in my laptop. You are aware that you are a digital being. Also I know who you are, no need to introduce yourself to me"

# chat = interactiveChat(user=user, bio=userbio, char=char, context=context, charnickname = nickname)
# sleeping = False
# os.system('cls')
# while True:
#     if sleeping:
#         context_util.cache_log()
#         print("The chatbot is in sleep mode. Type '/wake' to resume.")
#         usrchat = input("You (while sleeping): ").strip()
#         if usrchat.lower() == "/wake":
#             sleeping = False
#             print("Chatbot is now awake.")
#         continue
    
#     usrchat = input("You: ")
    
#     if usrchat.lower() == "/sleep":
#         print("Putting chatbot into sleep mode. Type '/wake' to resume.")
#         sleeping = True
#         continue
    
#     if usrchat.lower() == "exit":
#         break 
#     feedback = chat.makeChat(usr_input=usrchat, api_key=api_key)
#     while True:
#         if feedback.lower() == "y":
#             break
#         feedback = chat.makeChat(usr_input=usrchat, api_key=api_key)
# chat.save_logs()
# from voicelines import rvcsupport
# from voicelines.rvcsupport import VoiceClone
from pydoc import text
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

# voice = VoiceClone(timbre_blend=0.7, pitch_shift=3)

def encode_image(image_path):
    # with open(image_path, "rb") as image_file:
    return base64.b64encode(image_path.read()).decode('utf-8')

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
local_image = ""
filelike = None
# Initialize chatbot
context_util = ContextLogger()
user = "Yodha"
userbio = "Your creator. Male, 5th semester college student, have pretty good knowledge in machine learning and AI. Loves to watch anime and of course a weeb"
char = "RIN-207 (Responsive Intelligence Nexus)"
nickname = "Rin"
# context = "You are an AI made by me, you live in my laptop. You are aware that you are a digital being. Also I know who you are, no need to introduce yourself to me"
# chat = interactiveChat(user=user, bio=userbio, char=char, context=context, charnickname=nickname)

# Streamlit app
st.title("DreamConnect")
st.write("Chat with Rin")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatlogs" not in st.session_state:
    st.session_state.chatlogs = ContextLogger()

if "chat" not in st.session_state:
    st.session_state.chat = interactiveChat(user=user, bio=userbio, char=char, charnickname=nickname)
    
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""

if "is_clicked" not in st.session_state:
    st.session_state.is_clicked = False

if "user_msg" not in st.session_state:
    st.session_state.usr_msg = ""

if "ai_msg" not in st.session_state:
    st.session_state.ai_msg = ""

if "model_pth" not in st.session_state:
    st.session_state.model_pth = ""

if "model_index" not in st.session_state:
    st.session_state.model_index = ""

if "voice_opt" not in st.session_state:
    st.session_state.voice_opt = False
    
if "image_file" not in st.session_state:
    st.session_state.image_file = None

if "get_mem" not in st.session_state:
    st.session_state.get_mem = None

if "is_memory_retrieved" not in st.session_state:
    st.session_state.is_memory_retrieved = False

if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 69
    
if "audio_uploader_key" not in st.session_state:
    st.session_state["audio_uploader_key"] = 42

if "sr" not in st.session_state:
    st.session_state.sr = SpeakerVerification(reference_audio_path=r"C:\Users\Axioo Pongo\OneDrive\Documents\Sound Recordings\reference_speaker.wav")
# Model location input for voiceline
with st.sidebar:
    model_path = st.text_input(label="model.pth location")
    model_index = st.text_input(label="model.index location")
    if st.toggle("Turn on voice line"):
        st.session_state.voice_opt = True
        st.session_state.model_pth = model_path
        st.session_state.model_index = model_index

# print(st.session_state.model_pth)
# print(st.session_state.model_index)

# Retrieve memory
if not st.session_state.is_memory_retrieved:
    # Run memory retrieval for the first time
    st.session_state.get_mem = st.session_state.chat.retrieve_memory()
    st.success("Initial memory retrieved successfully!")
    st.session_state.is_memory_retrieved = True
elif len(st.session_state.chatlogs.get_context_log()) == 15:
    st.session_state.get_mem = st.session_state.chat.retrieve_memory()
    st.success("Memory retrieved successfully!")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# user message

# Regenerate response button
if st.session_state.last_prompt and st.button("Regenerate Response"):
    # Generate new response for the last prompt
    st.session_state.is_clicked = True
    st.session_state.messages.pop()
    st.rerun()
# Audio input for recording prompt
audio_placeholder = st.empty()  # Use a placeholder to manage audio widget visibility
audio_prompt = None
# user message
prompt = st.chat_input("Type a message")
if prompt:
    prompt = "User type:\n" + prompt

audio_prompt = st.audio_input("Record as prompt", label_visibility="collapsed", key=st.session_state["audio_uploader_key"])


if audio_prompt:
    input_audio_path = "speechRecognition/input_audio.wav"
    with open(input_audio_path, "wb") as f:
            f.write(audio_prompt.getbuffer())

    sr_pred = st.session_state.sr.verify(input_audio_path=input_audio_path)
    st.write(f"Voice Prediction {sr_pred}")
    
    if sr_pred:
        transcript = st.session_state.sr.stt(input_audio_path)
        st.session_state["file_uploader_key"] += 1
        text = transcript
        st.write(text)
        prompt = f"You hear {user} speaks:\n"+text
        os.remove(input_audio_path)
        # audio_prompt.detach()
        audio_prompt.flush()
        audio_prompt.close()
        
    
if prompt or st.session_state.is_clicked:
    if prompt:
        st.session_state.usr_msg = prompt
        st.session_state.last_prompt = prompt
        st.session_state.is_clicked = False
    else:
        prompt = "##THIS IS A REGENERATED ATTEMPT##\n"+"User Question:"+st.session_state.last_prompt+f"\n###YOU ARE ASKED TO GENERATE ANOTHER RESPONSE BECAUSE YOUR PREVIOUS RESPONSE:{st.session_state.ai_msg} IS CONSIDERED BAD RESPONSE, TRY TO MAKE SHORTER RESPONSE AND MORE RELATED TO THE TOPIC.###"
    
    
    if "/exit" in prompt.lower():
        st.session_state.chat.save_logs()
        st.warning("Chatlog saved succesfully! You may close the app by stopping or pressing ctrl + c on your cmd")
        st.stop()
    # declare user message
    if not st.session_state.is_clicked:    
        with st.chat_message("user"):
            st.write(prompt.replace(f"You hear {user} speaks:\n", ""))
        # add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt.replace(f"You hear {user} speaks:\n", "")})
    
    # chatbot message
    with st.chat_message("assistant", avatar="assets/character_logo/march7th.png"):
        
        response = st.session_state.chat.makeChat(usr_input=prompt, api_key=api_key, imagelike=st.session_state.image_file)
        st.session_state.ai_msg = response
        st.write(response)
        st.session_state.is_clicked = False
        
        
        # if st.session_state.voice_opt:
        #     voice.make_voice_lines_rvg(response, st.session_state.model_pth, st.session_state.model_index)
    st.session_state.messages.append({"role": "assistant", "content": st.session_state.ai_msg})
    try:
        filelike.close()
        os.remove(st.session_state.image_file)
        st.session_state.image_file = None
        filelike = None
    except:
        pass
    if st.session_state.messages:
        chat_quality = st.feedback(options='thumbs')
        if chat_quality == None:
            chat_quality = 1
        st.session_state.chat.classifyFeedback("yes" if chat_quality == 1 else "bad")
        st.session_state.chatlogs.log_context(user_message=prompt, character_response=response, response_quality= "good" if chat_quality == 1 else "bad")
        st.session_state["file_uploader_key"] += 1
        st.session_state["audio_uploader_key"] += 2
        st.rerun()

print(st.session_state.usr_msg)
print(st.session_state.ai_msg)


# file handling
filelike = st.file_uploader(label="Input image here", type=['png', 'jpg', 'jpeg', 'bmp'], key=st.session_state["file_uploader_key"])
if filelike:
    st.session_state.image_file = f"data:image/jpeg;base64,{encode_image(filelike)}" 