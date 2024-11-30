from ast import match_case
from groq import Groq
from chatbot.tools.makeJokes import get_joke
from chatbot.tools.makeCalculations import calculate
from chatbot.tools.makeSearch import google_web_search
import json

class ChatEngine:
    def __init__(self, model = "llama-3.1-70b-versatile", api_key = None, params=None):
        if api_key:
            self.Client = Groq(api_key=api_key)
        else:
            raise ValueError("API KEY needed, please get your groq API key at https://console.groq.com/keys")
        self.Model = model or "llama-3.1-70b-versatile"
        self.Params = params or {
            'temperature': 0.95,
            'max_tokens': 300,
            'frequency_penalty': 1.7,
            'presence_penalty': 1.7,
        }

    def generate_response(self, context, rules):
        message = [
            {"role": "system", "content": rules},
            {"role": "user", "content": context}
        ]
        try:
            response = self.Client.chat.completions.create(
                messages=message,
                model=self.Model,
                temperature=self.Params['temperature'],
                max_tokens=self.Params['max_tokens'],
                top_p = 0.9,
                frequency_penalty=self.Params['frequency_penalty'],
                presence_penalty=self.Params['presence_penalty'],
                tools= [
                    {
                        "type": "function",
                        "function": {
                            "name": "get_joke",
                            "description": "generate or tell jokes",
                            "parameters": {},
                            "required": {},
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "calculate",
                            "description": "Evaluate a mathematical expression",
                            "parameters": {
                                    "expression": {
                                        "type": "string",
                                        "description": "The mathematical expression to evaluate"
                                    }
                                },
                            "required": ["expression"],
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "web_search",
                            "description": "Perform a web search using the Google Custom Search JSON API",
                            "parameters": {
                                "query": {
                                    "type": "string",
                                    "description": "The search query"
                                }
                            },
                            "required": ["query"]
                        }
                    },
                ],
                tool_choice="auto"
            )
            model_response = response.choices[0].message
            # tool call variable
            tool_calls = model_response.tool_calls
            print("Prove that the model call for tools: ", tool_calls) # printing the response because I don't trust the AI using tools
            # check if the model need to call tools
            if tool_calls:
                available_functions = {
                    "get_joke": get_joke,
                    "calculate": calculate,
                    "web_search": lambda query: google_web_search(query)
                }

                # Process each tool call
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Call the tool and get the response
                    # if function_name == "get_joke":
                    #     function_response = function_to_call()
                    # elif function_name == "get_weather":
                    #     function_response = function_to_call(location=function_args.get("location"))
                    
                    match function_name:
                        case "get_joke":
                            function_response = function_to_call()
                        case "calculate":
                            function_response = function_to_call(expression=function_args.get("expression"))
                        case "web_search":
                            function_response = function_to_call(query=function_args.get("query"))

                    # Add the tool response to the conversation
                    message.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",  # Indicates this message is from tool use
                            "name": function_name,
                            "content": function_response,
                        }
                    )
                    for msg in message:
                        if msg["role"] == "user":
                            msg["content"] += "summarize your findings in 100 to 200 tokens"

                # Make a second API call with the updated conversation
                second_response = self.Client.chat.completions.create(
                    model="llama3-groq-8b-8192-tool-use-preview",
                    messages=message,
                    temperature=self.Params['temperature'],
                    max_tokens=self.Params['max_tokens'],
                    top_p=0.9,
                    frequency_penalty=self.Params['frequency_penalty'],
                    presence_penalty=self.Params['presence_penalty']
                )
                return second_response.choices[0].message.content
            return response.choices[0].message.content
        except Exception as e:
            raise (f"Error generating response: {e}")
    
    def groqVision(self, img_path):
        completion = self.Client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe what's in the image in short. Your token is limited to 100"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": img_path
                            }
                        }
                    ]
                }
            ],
            temperature=0,
            max_tokens=500,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
        