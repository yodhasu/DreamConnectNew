import os
from chatbot import useOllama
from chatbot import useGroq
from chatbot import useOpenAI
from chatbot import sendToBackend
from chatbot import context_logger
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
            + " "
            +self.get_time_of_day()
            +"\n"
            + (context or "")       
        )
        self.system_prompt = system_prompt
        self.memory_retrieved = False
        self.user_prompt = user_prompt
        self.system_prompt_from_directory = sys_prompt_dir or "chatbot/system_prompt.txt"
        self.user_prompt_from_directory = usr_prompt_dir or "chatbot/user_prompt.txt"
        self.back = sendToBackend.backend()
        self.logger = context_logger.ContextLogger()
        self.getPromptFromDir()
        
    # Funtion to setup prompt
    def getPromptFromDir(self):
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
    
    
    # Define chat engine based on user
    def defineEngine(self, engine = None, api_key = None, chat_model = None, parameter = None):
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
                self.chatClient = useOllama.ChatEngine(model=chat_model, params=parameter)
            case "groq":
                self.chatClient = useGroq.ChatEngine(api_key=api_key, model=chat_model, params=parameter)
            case "openai":
                self.chatClient = useOpenAI.ChatEngine(api_key=api_key, model=chat_model, params=parameter)
            case _:
                raise ValueError("Wrong engine/engine provided")
    
    # chat function
    def makeChat(self, usr_input = None, api_key = None):
        self.getPromptFromDir()
        
        self.input = usr_input
        # Formating input to prompt
        
        local_system_prompt = self.system_prompt
        local_user_prompt = self.user_prompt
        
        local_user_prompt=local_user_prompt.format(
            context = self.logger.get_context_log() or self.context,
            affection = self.affection,
            question = usr_input or self.input
        )
        if not self.memory_retrieved:
            local_user_prompt = "Previous memory:"+ "\n"+ self.retrieve_memory(api_key=api_key) or ""+ "\n" + local_user_prompt
        
        self.memory_retrieved = True
        self.defineEngine(api_key=api_key)
        
        # print(f"Context: {local_user_prompt}\n")
        response = self.chatClient.generate_response(context=local_user_prompt, rules=local_system_prompt)
        self.back.send_to_space(response)
        # Debugging print to check the response
        # print(f"Generated response: {response}")
        
        if response is None:
            print("No response generated.")
            return
        
        print(f"{self.charater}: {response}\n")
        self.logger.log_context(usr_input, response)
        self.context += "\n"+'\n'.join(self.logger.get_context_log())
    
    def save_logs(self):
        self.logger.save_context_log(f"chatbot/logs/logfile_{str(datetime.now())}")
    
    def retrieve_memory(self, api_key = None):
        memory  = []
        for logs in os.listdir("chatbot/logs/"):
            collectlogs = ""
            with open(logs, "r") as logfiles:
                collectlogs = logfiles.read()
            memory.append(collectlogs)
        memory = "".join(memory)
        
        params = {
            'temperature': 0.85,
            'max_tokens': 50,
            'frequency_penalty': 1.7,
            'presence_penalty': 1.7,
        }
        
        self.defineEngine(api_key=api_key, parameter=params)
        
        summarize_prompt = "User input is a log file of a chat. Summarize what happened in short but detail"
        
        retrieved_memory = self.chatClient.generate_response(context="", rules=summarize_prompt)
        
        return retrieved_memory
    
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
                