from chatbot import useOllama
from chatbot import useGroq
from chatbot import useOpenAI
from chatbot import sendToBackend
from datetime import datetime

class interactiveChat:
    def __init__(self, affection = 10, user=None, bio=None, context = None, char = "AI Girlfriend", chat_engines = "groq", system_prompt = None, user_prompt = None, sys_prompt_dir = None, usr_prompt_dir = None):
        if user is None or bio is None:
            raise ValueError("'user' and 'bio' must be provided.")
        
        self.engine = chat_engines.lower()
        if self.engine.lower() not in ["ollama", "g4f", "openai", "groq"]:
            raise ValueError(" Current available chat engines are: 'Ollama', 'openai', 'g4f', 'Groq'")
        
        self.charater = char
        self.affection = affection
        self.user = user
        self.bio = bio
        self.context = (
            "Current date and time: "
            +str(datetime.now())
            +self.get_time_of_day()
            +"\n"
            + (context or "")       
        )
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.system_prompt_from_directory = sys_prompt_dir or "chatbot/system_prompt.txt"
        self.user_prompt_from_directory = usr_prompt_dir or "chatbot/user_prompt.txt"
        self.back = sendToBackend.backend()
        
    # Funtion to setup prompt
    def getPromptFromDir(self, question):
        # get system prompt
        try:
            # print(self.system_prompt_from_directory)
            if self.system_prompt is None:
                with open(self.system_prompt_from_directory, "r") as sysprompt:
                    self.system_prompt = sysprompt.read()
        except Exception as e:
            raise(f"Error opening system prompt with error: {e}")
        # get user prompt
        try:
            # print(self.user_prompt_from_directory)
            if self.user_prompt is None:
                with open(self.user_prompt_from_directory, "r") as usrprompt:
                    self.user_prompt = usrprompt.read()
        except Exception as e:
            raise(f"Error opening user prompt with error: {e}")
        
        # Formating input to prompt
        self.system_prompt=self.system_prompt.format(
            char = self.charater,
            user = self.user,
            userbio = self.bio
        )
        
        self.user_prompt=self.user_prompt.format(
            context = self.context,
            affection = self.affection,
            question = question
        )
    
    
    # Define chat engine based on user
    def defineEngine(self, engine = None, api_key = None, chat_model = None):
        if self.engine is None:
            if engine is None:
                raise ValueError("engine can't be empty")
            self.engine = engine
        else:
            pass
        
        if self.engine.lower() not in ["ollama", "g4f", "openai", "groq"]:
            raise ValueError(" Current available chat engines are: 'Ollama', 'openai', 'g4f', 'Groq'")
        
        # make different case depends on engine
        self.chatClient = None
        match self.engine:
            case "ollama":
                self.chatClient = useOllama.ChatEngine(model=chat_model)
            case "groq":
                self.chatClient = useGroq.ChatEngine(api_key=api_key, model=chat_model)
            case "openai":
                self.chatClient = useOpenAI.ChatEngine(api_key=api_key, model=chat_model)
            case _:
                raise ValueError("Wrong engine/engine provided")
    
    # chat function
    def makeChat(self, usr_input = None, api_key = None):
        self.getPromptFromDir(question=usr_input)
        self.defineEngine(api_key=api_key)
        response = self.chatClient.generate_response(context=self.user_prompt, rules=self.system_prompt)
        self.back.send_to_space(response)
        # Debugging print to check the response
        # print(f"Generated response: {response}")
        
        if response is None:
            print("No response generated.")
            return
        
        print(f"{self.charater}: {response}")
    
    @staticmethod
    def get_time_of_day():
        """Return the current time of day."""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        else:
            return "night"
                