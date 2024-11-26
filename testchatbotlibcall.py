from chatbot.interactive import interactiveChat
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

user = "Yodha"
userbio = "Your husband. Master in machine learning and AI. Loves to watch anime and of course a weeb"
char = "March 7th"
context = "I just got home after a long day at work"

chat = interactiveChat(user=user, bio=userbio, char=char, context=context)
chat.makeChat("*open up front door* Honey, I'm home!", api_key=api_key)