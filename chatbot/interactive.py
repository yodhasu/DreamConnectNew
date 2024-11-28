import os
import re
from chatbot import useOllama
from chatbot import useGroq
from chatbot import useOpenAI
from chatbot import sendToBackend
from chatbot import context_logger
from datetime import datetime
from urlextract import URLExtract
import base64

extractor = URLExtract()
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
        self.context = context or ""
        self.system_prompt = system_prompt
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
    
    def classifyFeedback(self, text):
        feedtext = ""
        feedtext = text
        if feedtext.lower() in ["y", "yes"]:
            return "good"
        elif feedtext.lower() in ["n", "no"]:
            return "bad"
        else:
            return "neutral"
    
    def getFeedback(self):
        usr_feed = input("Good? (y/n)").lower()
        return usr_feed
    
    # chat function
    def makeChat(self, usr_input = None, api_key = None):
        self.getPromptFromDir()
        curr_memory = "Previous memory:"+ "\n"+ self.retrieve_memory(api_key=api_key) or ""+ "\n"
        intention = self.intentIdentifier(usr_input, api_key)
        self.input = usr_input
        # Formating input to prompt
        
        local_system_prompt = self.system_prompt
        local_user_prompt = self.user_prompt
        
        local_user_prompt=local_user_prompt.format(
            intention = intention,
            date = str(datetime.now()),
            time = self.get_time_of_day(),
            memory = curr_memory or "",
            context = self.logger.get_context_log() or self.context,
            affection = self.affection,
            question = usr_input or self.input
        )
        
        self.defineEngine(api_key=api_key)
        
        print(f"Context: {local_user_prompt}\n")
        response = self.chatClient.generate_response(context=local_user_prompt, rules=local_system_prompt)
        self.back.send_to_space(response)
        # Debugging print to check the response
        # print(f"Generated response: {response}")
        
        if response is None:
            print("No response generated.")
            return

        print(f"\n{self.charater}: {response}\n")
        usr_feed = self.getFeedback()
        classify = self.classifyFeedback(usr_feed)
        self.logger.log_context(usr_input, response, classify)
        self.context += "\n" + ' '.join(self.logger.get_context_log()) + "\n"
        return usr_feed
    
    def save_logs(self):
        filename = f"chatbot/logs/logfile_{str(datetime.now())}".replace(":", "-")
        filename = filename.replace(".", "-")
        self.logger.save_context_log(filename=f"{filename}.txt")
    
    def retrieve_memory(self, api_key = None):
        memory  = []
        for logs in os.listdir("chatbot/logs/"):
            collectlogs = ""
            with open(f"chatbot/logs/{logs}", "r") as logfiles:
                collectlogs = logfiles.read()
            memory.append(collectlogs)
        memory = "".join(memory)
        
        params = {
            'temperature': 0.1,
            'max_tokens': 100,
            'frequency_penalty': 1.7,
            'presence_penalty': 1.7,
        }
        
        self.defineEngine(api_key=api_key, parameter=params)
        
        summarize_prompt = f"User input is a log file of a chat between You as {self.charater} and the user itself with format context format: [Timestamp] User: user_response tone of response Character: character_response tone of response Off-topic: yes/no, Response indicator (good/bad). Summarize what happened in short but detail, don't retain the memory if the response indicator marks it as a bad response. your limit is 100 tokens. User message that are in caps lock means a very important detail in the memory so please insert it. Please summarize the reponse only. User is {self.user}, {self.bio}"
        
        retrieved_memory = self.chatClient.generate_response(context=summarize_prompt, rules=memory)
        
        return retrieved_memory
    
    def intentIdentifier(self, user_input, api_key):
        params = {
            'temperature': 0,
            'max_tokens': 100,
            'frequency_penalty': 1.7,
            'presence_penalty': 1.7,
        }
        prompt = """
        Identify the intention of the user's input
        """
        self.defineEngine(api_key=api_key, parameter=params)
        intent = self.chatClient.generate_response(context=prompt, rules=user_input)
        return intent
    
    @staticmethod
    def filterFilepath(textinput):
        path_pattern = path_pattern = r"'([A-Za-z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)*[^\\/:*?\"<>|\r\n]+)'"
        match = re.search(path_pattern, textinput)
        
        if match:
            file_path = match.group(1)
            
            # Replace backslashes with forward slashes in the file path
            processed_path = file_path.replace("\\", "/")
            
            # encode to base64
            with open(processed_path, "rb") as image_file:
                base64_image =  base64.b64encode(image_file.read()).decode('utf-8')
                return 1, f"data:image/jpeg;base64,{base64_image}"
        else:
            urls = extractor.find_urls(textinput)
            if urls == "":
                return 0, ""
            else:
                link =''.join(urls)
                return 2, link
    
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
                