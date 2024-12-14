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
import streamlit as st
import base64
from chatbot.interactive import interactiveChat
from chatbot.context_logger import ContextLogger
from dotenv import load_dotenv
import os

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

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# user message
prompt = st.chat_input("Type a message")

if prompt or st.session_state.is_clicked:
    if prompt:
        st.session_state.usr_msg = prompt
        st.session_state.last_prompt = prompt
        st.session_state.is_clicked = False
    else:
        prompt = st.session_state.last_prompt
    
    
    if prompt.lower() == "/exit":
        st.session_state.chat.save_logs()
        st.warning("Chatlog saved succesfully! You may close the app by stopping or pressing ctrl + c on your cmd")
        st.stop()
    # declare user message
    if not st.session_state.is_clicked:    
        with st.chat_message("user"):
            st.markdown(prompt)
        # add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
    
    # chatbot message
    with st.chat_message("assistant", avatar="assets/character_logo/march7th.png"):
        response = st.session_state.chat.makeChat(usr_input=prompt, api_key=api_key, imagelike=local_image)
        st.session_state.ai_msg = response
        st.write(response)
        st.session_state.is_clicked = False
        # if st.session_state.voice_opt:
        #     voice.make_voice_lines_rvg(response, st.session_state.model_pth, st.session_state.model_index)
            
    st.session_state.messages.append({"role": "assistant", "content": st.session_state.ai_msg})
    try:
        filelike.close()
    except:
        pass
    if st.session_state.messages:
        chat_quality = st.feedback(options='thumbs')
        if chat_quality == None:
            chat_quality = 1
        st.session_state.chat.classifyFeedback("yes" if chat_quality == 1 else "bad")
        st.session_state.chatlogs.log_context(user_message=st.session_state.usr_msg, character_response=st.session_state.ai_msg, response_quality= "good" if chat_quality == 1 else "bad")

# Regenerate response button
if st.session_state.last_prompt and st.button("Regenerate Response"):
    # Generate new response for the last prompt
    st.session_state.is_clicked = True
    st.session_state.messages.pop()
    st.rerun()


print(st.session_state.usr_msg)
print(st.session_state.ai_msg)


# file handling
filelike = st.file_uploader(label="Input image here", type=['png', 'jpg', 'jpeg', 'bmp'])
if filelike:
    local_image = f"data:image/jpeg;base64,{encode_image(filelike)}" 