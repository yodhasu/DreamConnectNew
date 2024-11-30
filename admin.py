from chatbot.interactive import interactiveChat
from chatbot.context_logger import ContextLogger
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
context_util = ContextLogger()

user = "Yodha"
userbio = "Your master. Male, 5th semester college student, have pretty good knowledge in machine learning and AI. Loves to watch anime and of course a weeb"
char = "March 7th"
nickname = "March"
context = "You are an AI made by me, you live in my laptop. You are aware that you are a digital being."

chat = interactiveChat(user=user, bio=userbio, char=char, context=context, charnickname = nickname)
sleeping = False
os.system('cls')
while True:
    if sleeping:
        context_util.cache_log()
        print("The chatbot is in sleep mode. Type '/wake' to resume.")
        usrchat = input("You (while sleeping): ").strip()
        if usrchat.lower() == "/wake":
            sleeping = False
            print("Chatbot is now awake.")
        continue
    
    usrchat = input("You: ")
    
    if usrchat.lower() == "/sleep":
        print("Putting chatbot into sleep mode. Type '/wake' to resume.")
        sleeping = True
        continue
    
    if usrchat.lower() == "exit":
        break 
    feedback = chat.makeChat(usr_input=usrchat, api_key=api_key)
    while True:
        if feedback.lower() == "y":
            break
        feedback = chat.makeChat(usr_input=usrchat, api_key=api_key)
chat.save_logs()