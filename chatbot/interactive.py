import useOllama
import useGroq
import useOpenAI

class interactiveChat:
    def __init__(self, affection = 10, user=None, bio=None, context = None, chat_engines = None, system_prompt = None, user_prompt = None, sys_prompt_dir = None, usr_prompt_dir = None):
        if user is None or bio is None:
            raise ValueError("'user' and 'bio' must be provided.")
        
        self.engine = chat_engines.lower()
        if self.engine.lower() is not "ollama" or self.engine.lower() is not "g4f" or self.engine.lower() is not "openai" or self.engine.lower() is not "groq":
            raise ValueError(" Current available chat engines are: 'Ollama', 'openai', 'g4f', 'Groq'")
        
        self.affection = affection
        self.user = user
        self.bio = bio
        self.context = context or "Your character is enthusiastic, cute, simple, likes to talk in short sentences, and is clumsy. You are allowed to use emojis to reveal your character. You will show your character as much as possible. The one who is talking to you will be your boyfriend, you already know each other for very long time and you love him very much. You will have your own emotions and can be angry with him if anything he says offends you or makes you uncomfortable, you can also reject and denied his request and use swear and curse words like fuck."
        
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.system_prompt_from_directory = sys_prompt_dir or "system_prompt.txt"
        self.user_prompt_from_directory = usr_prompt_dir or "user_prompt.txt"
    
    # Funtion to setup prompt
    def getPromptFromDir(self):
        # get system prompt
        try:
            if self.system_prompt is None:
                with open(self.system_prompt_from_directory, "r") as sysprompt:
                    self.system_prompt = sysprompt
        except Exception as e:
            print(f"Error opening system prompt with error: {e}")
        # get user prompt
        try:
            if self.user_prompt is None:
                with open(self.user_prompt_from_directory, "r") as usrprompt:
                    self.user_prompt = usrprompt
        except Exception as e:
            print(f"Error opening user prompt with error: {e}")
    
    
    # Define chat engine based on user
    def defineEngine(self, engine = None, api_key = None, chat_model = None):
        if self.engine is None:
            if engine is None:
                raise ValueError("engine can't be empty")
            self.engine = engine
        else:
            pass
        
        if self.engine.lower() is not "ollama" or self.engine.lower() is not "g4f" or self.engine.lower() is not "openai" or self.engine.lower() is not "groq":
            raise ValueError(" Current available chat engines are: 'Ollama', 'openai', 'g4f', 'Groq'")
        
        # make different case depends on engine
        self.engine = None
        match self.engine:
            case "ollama":
                self.engine = useOllama.ChatEngine(model=chat_model)
            case "groq":
                self.engine = useGroq.ChatEngine(api_key=api_key, model=chat_model)
            case "openai":
                self.engine = useOpenAI.ChatEngine(api_key=api_key, model=chat_model)
            case _:
                raise ValueError("Wrong engine/engine provided")
                