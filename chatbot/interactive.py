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
import json
import g4f

extractor = URLExtract()
class interactiveChat:
    def __init__(self, affection = 10, user=None, bio=None, context = None, char = "AI Girlfriend", chat_engines = "groq", user_prompt = None, system_prompt = None, sys_prompt_dir = None, usr_prompt_dir = None, charnickname = None):
        if user is None or bio is None:
            raise ValueError("'user' and 'bio' must be provided.")
        
        self.engine = chat_engines.lower()
        if self.engine.lower() not in ["ollama", "g4f", "openai", "groq"]:
            raise ValueError(" Current available chat engines are: 'Ollama', 'openai', 'g4f', 'Groq'")
        
        self.charater = char
        self.affection = affection
        self.user = user
        self.usrintent = ""
        self.bio = bio
        self.context = context or ""
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.system_prompt_from_directory = sys_prompt_dir or "chatbot/system_prompt.txt"
        self.user_prompt_from_directory = usr_prompt_dir or "chatbot/user_prompt.txt"
        self.back = sendToBackend.backend()
        self.logger = context_logger.ContextLogger()
        self.getPromptFromDir()
        self.response = ""
        self.char_nick = charnickname
        self.feedback = ""
        self.back.send_to_space(["neutral"])
        self.currmem = ""
        
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
                self.chatClient = useOllama.ChatEngine()
            case "groq":
                self.chatClient = useGroq.ChatEngine(api_key=api_key)
            case "openai":
                self.chatClient = useOpenAI.ChatEngine(api_key=api_key)
            case _:
                raise ValueError("Wrong engine/engine provided")
    
    def classifyFeedback(self, text):
        if text in ["y", "yes"]:
            self.feedback = "good"
        elif text in ["n", "no"]:
            self.feedback= "bad"
        else:
            self.feedback = "neutral"
    
    def imageVision(self, imgpath):
        print(f"Image path: {imgpath}")
        result = self.chatClient.groqVision(img_path=imgpath)
        return result
    
    # chat function
    def makeChat(self, usr_input = None, api_key = None, imagelike = None):
        intention = None
        # define engine
        self.defineEngine(api_key=api_key)
        # auto update memory logs
        if len(self.logger.get_context_log()) == 15:
            self.save_logs()
        # identify user's intention
        if "REGENERATED ATTEMPT" not in usr_input:
            intention = self.intentIdentifier(usr_input, self.response, api_key, self.currmem)
            self.usrintent = intention
        # check for images in user input
        img_summarized = ""
        # status, img = self.filterFilepath(usr_input)
        # print(status, img)
        # Formating input to prompt
        
        local_system_prompt = self.system_prompt
        local_user_prompt = self.user_prompt
        
        local_system_prompt = local_system_prompt.format(
            user = self.user,
            userbio = self.bio,
            char = self.charater
        )
        
        local_user_prompt=local_user_prompt.format(
            intention = intention or self.usrintent,
            date = str(datetime.now()),
            time = self.get_time_of_day(),
            memory = self.currmem or "None",
            context = self.logger.get_context_log() or self.context,
            affection = self.affection,
            question = usr_input
        )
        # add image summary to the prompt
        if imagelike:
            try:
                img_summarized = self.imageVision(imagelike)
                local_user_prompt += f"\n\nSummary of given image by user: {img_summarized}\n\nBy having summary of the image given by user that means you can SEE the image and please tell what you see."
            except:
                pass
        print(f"Context: {local_user_prompt}\n")
        response = self.chatClient.process_query(query=local_user_prompt, system_prompt=local_system_prompt, inputs=usr_input)
        imagelike = None
        img_summarized = None
        self.back.send_to_space(response)
        # Debugging print to check the response
        # print(f"Generated response: {response}")
        
        if response is None:
            print("No response generated.")
            return

        print(f"\n{self.charater}: {response}\n")
        self.response = response
        self.logger.log_context(usr_input, response, self.feedback)
        self.context = self.logger.get_context_log()
        return response
    
    def save_logs(self):
        filename = f"chatbot/logs/logfile_{str(datetime.now())}".replace(":", "-")
        filename = filename.replace(".", "-")
        self.logger.save_context_log(filename=f"{filename}.json")

    def retrieve_memory(self, api_key=None, log_dir="chatbot/logs/", max_logs=2):
        memory = ""

        # Get a list of all log files sorted by name (only JSON files now)
        log_files = sorted(
            [os.path.join(log_dir, log) for log in os.listdir(log_dir) if log.endswith(".json")],
            reverse=True  # Sort by name in descending order (latest logs first)
        )
        
        # Limit to the most recent `max_logs` files
        recent_logs = log_files[:max_logs]
        if not recent_logs:
            return "None"
        
        # Process the most recent logs
        for log_path in recent_logs:
            print("Processing log file at path:", log_path)
            with open(log_path, "r") as logfile:
                try:
                    # Read the log entries (assuming JSON format)
                    logs = json.load(logfile)
                    
                    # Iterate through each log entry and format it
                    for log in logs:
                        # Create a clean format for each log entry
                        log_text = (
                            f"Timestamp: {log['Timestamp']}\n"
                            f"User message: {self.preprocess_logs(log['User message'])}\n"
                            f"User emotion: {log['User emotion']}\n"
                            f"AI Response: {self.preprocess_logs(log['AI Response'])}\n"
                            f"AI emotion: {log['AI emotion']}\n"
                            f"Off-topic response: {log['Off topic response']}\n"
                            f"Response quality: {log['Overall Response quality']}\n"
                            f"Repetitive response: {log['Repetitive response']}\n\n"
                        )
                        memory += log_text
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {log_path}")
                    continue
        
        # Construct the summarize prompt
        summarize_prompt = f"""
        You are {self.charater}, also known as {self.char_nick}, an intelligent and advanced AI made by the user.

        I, {self.user}, also known as User, am your friend and creator. We were having a chat previously, and the chat history was saved in a log with the following format:

        - Timestamp
        - User message
        - User emotion
        - AI Response
        - AI emotion
        - Off-topic response
        - Response length
        - Repetitive response
        - Overall Response quality

        You must summarize the logs clearly in a narrative style. 
        - Focus on what happened during the conversation, important details, and your emotions or thoughts.
        - Identify examples of bad responses from the log and provide them in this format:  
        Bad Response: [response]
        - Identify examples of long responses from the log and provide them in this format:  
        Too Long Response (avoid): [response]
        

        Conclude your summary with:
        Chat ended in [last_timestamp].

        ### Important Instructions:
        - Do NOT include code syntax or interpret the log data as code.
        - Do NOT use structured or code-like formatting in your output.
        - Keep your response under 100 tokens for brevity.
        - Logs with recent timestamps are the most important one.
        - Always answer in english

        Start your summary below:
        """
        
        # Use the summarizer model to generate the summary of the memory
        # retrieved_memory = chatengine.generate_response(query=memory, system_prompt=summarize_prompt)
        retrieved_memory = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4o,
            messages=[
                {"role": "user", "content":memory},
                {"role": "system", "content": summarize_prompt}
            ]
        )
        self.currmem = retrieved_memory
        


    
    def intentIdentifier(self, user_input, char_response, memory, api_key):
        
        prompt = f"""
        This is the character and user's previous memory: {memory}
        if the previous memory is None or not available, state that this is the first time character and user chat.
        This is the character's previous input : {char_response}
        if there aren't any previous input it means that this is the first chat.
        Character's name: {self.charater}
        Character's nickname: {self.char_nick}
        you may use or not use it to do your task.
        IF NO PREVIOUS SYSTEM RESPONSE PROVIDED JUST FOCUS ON USER'S INPUT!
        
        
        Your task is:
        Identify the intention of the user's input.
        
        User's input {user_input}
        DO NOT USE ANY TOOLS! YOU ARE NOT ALLOWED TO USE ANY TOOLS!
        """
        system_prompt = "You are a smart AI that is used to identify intention of the user's input in a chat between character and user. Answer in paragraph but limit your answer to 20 - 70 token."

        intent = self.chatClient.generate_response_for_utils(context=prompt, rules=system_prompt)
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
    
    @staticmethod
    def preprocess_logs(log_text):
        """
        Preprocesses log text by removing code blocks and ensuring plain text.
        """
        # Remove code blocks (e.g., ```python ... ``` or any similar block)
        cleaned_text = re.sub(r"```.*?```", "", log_text, flags=re.DOTALL)
        
        # Optionally, remove any residual inline code or syntax-like snippets
        cleaned_text = re.sub(r"`[^`]+`", "", cleaned_text)
        
        return cleaned_text.strip()
                