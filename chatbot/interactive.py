import os
import re
import stat
from chatbot import useOllama
from chatbot import useGroq
from chatbot import useOpenAI
from chatbot import sendToBackend
from chatbot import context_logger
from datetime import datetime
from urlextract import URLExtract
from transformers import pipeline
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
    
    def imageVision(self, imgpath):
        print(f"Image path: {imgpath}")
        result = self.chatClient.groqVision(img_path=imgpath)
        return result
    
    # chat function
    def makeChat(self, usr_input = None, api_key = None):
        # get prompt
        self.getPromptFromDir()
        # get memory
        curr_memory = "Previous memory:"+ "\n"+ self.retrieve_memory(api_key=api_key) or ""+ "\n"
        # identify user's intention
        intention = self.intentIdentifier(usr_input, api_key)
        # check for images in user input
        img_summarized = ""
        status, img = self.filterFilepath(usr_input)
        print(status, img)
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
        # add image summary to the prompt
        if status != 0:
            img_summarized = self.imageVision(img)
            local_user_prompt += f"\n\nSummary of given image by user: {img_summarized}\n\nBy having summary of the image given by user that means you can SEE the image and please tell what you see."
        
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
            'max_tokens': 200,
            'frequency_penalty': 1.7,
            'presence_penalty': 1.7,
        }
        
        self.defineEngine(api_key=api_key, parameter=params)
        # print(memory)
        
        summarize_prompt = f"""
        "User input is a log file of a chat between you, as {self.charater}, and the user. The format is as follows:
        [Timestamp] User: user_response (tone of response)
        Character: character_response (tone of response)
        Off-topic: yes/no
        Response indicator: good/bad

        Summarize the conversation briefly but with detail, try to tell what already happened before. If the response indicator is marked as 'bad', do not retain the memory associated with it. Retain the most recent memory and topics, as they are more important.
        If the user message is in CAPITALS, it indicates a very important detail to be added to memory.

        Keep the summary under 100 tokens.
        User is {self.user}, {self.bio}"
        """
        
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
    
    
    def filterFilepath(self, textinput):
        path_pattern = r'["\']?([a-zA-Z]:[\\\/][^<>:"|?*]+(?:[\\\/][^<>:"|?*]+)*)["\']?'
        match = re.findall(path_pattern, textinput)
        urlfound = extractor.find_urls(textinput)
        
        if len(urlfound) >=1:
            return 2, urlfound[0]
        else:
            if match:
                file_path = match[0]
                
                # Replace backslashes with forward slashes in the file path
                processed_path = file_path.replace("\\", "/")
                
                # encode to base64
                encoded_image = self.encode_image(processed_path)
                local_image = f"data:image/jpeg;base64,{encoded_image}"
                
                return 1, local_image
            else:
                return 0, ""
    
    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
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
                