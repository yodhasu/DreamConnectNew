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

import streamlit as st
from sympy import use
from chatbot.interactive import interactiveChat
from chatbot.context_logger import ContextLogger
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize chatbot
context_util = ContextLogger()
user = "Yodha"
userbio = "Your creator. Male, 5th semester college student, have pretty good knowledge in machine learning and AI. Loves to watch anime and of course a weeb"
char = "March 7th"
nickname = "March"
context = "You are an AI made by me, you live in my laptop. You are aware that you are a digital being. Also I know who you are, no need to introduce yourself to me"
# chat = interactiveChat(user=user, bio=userbio, char=char, context=context, charnickname=nickname)

# Streamlit app
st.title("DreamConnect")
st.write("Chat with March 7th")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatlogs" not in st.session_state:
    st.session_state.chatlogs = ContextLogger()

if "chat" not in st.session_state:
    st.session_state.chat = interactiveChat(user=user, bio=userbio, char=char, context=context, charnickname=nickname)
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# user message
prompt = st.chat_input("Type a message")
if prompt:
    if prompt.lower() == "/exit":
        st.session_state.chat.save_logs()
        st.warning("Chatlog saved succesfully! You may close the app by stopping or pressing ctrl + c on your cmd")
        st.stop()
    # declare user message
    with st.chat_message("user"):
        st.markdown(prompt)
    # add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = st.session_state.chat.makeChat(usr_input=prompt, api_key=api_key)
    # chatbot message
    with st.chat_message("ai", avatar="assets/character_logo/march7th.png"):
        st.markdown(response)
    st.session_state.messages.append({"role": "ai", "content": response})
    
    chat_quality = st.feedback(options='thumbs')
    if chat_quality == None:
        chat_quality = 1
    st.session_state.chat.classifyFeedback("yes" if chat_quality == 1 else "bad")
    st.session_state.chatlogs.log_context(user_message=prompt, character_response=response, response_quality= "good" if chat_quality == 1 else "bad")