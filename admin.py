from chatbot.interactive import interactiveChat
from chatbot.context_logger import ContextLogger
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
context_util = ContextLogger()

user = "Yodha"
userbio = "Your husband. Master in machine learning and AI. Loves to watch anime and of course a weeb"
char = "March 7th"
context = "I just got home after a long day at work"

chat = interactiveChat(user=user, bio=userbio, char=char, context=context)
os.system('cls')
while True:
    usrchat = input("You: ")
    if usrchat.lower() == "exit":
        break 
    chat.makeChat(usr_input=usrchat, api_key=api_key)
    while True:
        feedback = input("Good? (y/n)")
        if feedback.lower() == "y":
            break
        chat.makeChat(usr_input=usrchat, api_key=api_key)

context_util.save_context_log()