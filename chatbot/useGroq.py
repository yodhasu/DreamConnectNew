# from ast import match_case
# from groq import Groq
# from chatbot.tools.makeJokes import get_joke
# from chatbot.tools.makeCalculations import calculate
# from chatbot.tools.makeSearch import google_web_search
# import json

# class ChatEngine:
#     def __init__(self, model = "llama-3.1-70b-versatile", api_key = None, params=None):
#         if api_key:
#             self.client = Groq(api_key=api_key)
#         else:
#             raise ValueError("API KEY needed, please get your groq API key at https://console.groq.com/keys")
#         self.Model = model or "mixtral-8x7b-32768"
#         self.Params = params or {
#             'temperature': 0.95,
#             'max_tokens': 300,
#             'frequency_penalty': 1.7,
#             'presence_penalty': 1.7,
#         }

#     def generate_response_for_utils(self, context, rules):
#         message = [
#             {"role": "system", "content": rules},
#             {"role": "user", "content": context}
#         ]
#         try:
#             response = self.client.chat.completions.create(
#                 messages=message,
#                 model="llama3-groq-8b-8192-tool-use-preview",
#                 temperature=0,
#                 max_tokens=self.Params['max_tokens'],
#                 top_p = 0.9,
#                 frequency_penalty=self.Params['frequency_penalty'],
#                 presence_penalty=self.Params['presence_penalty'],
                
#             )
#             model_response = response.choices[0].message
            
#             return model_response.content
#         except Exception as e:
#             raise (f"Error generating response: {e}")

#     def generate_response(self, context, rules):
#         message = [
#             {"role": "system", "content": rules},
#             {"role": "user", "content": context}
#         ]
#         try:
#             response = self.client.chat.completions.create(
#                 messages=message,
#                 model=self.Model,
#                 temperature=self.Params['temperature'],
#                 max_tokens=self.Params['max_tokens'],
#                 top_p = 0.9,
#                 frequency_penalty=self.Params['frequency_penalty'],
#                 presence_penalty=self.Params['presence_penalty'],
#                 tools= [
#                     {
#                         "type": "function",
#                         "function": {
#                             "name": "get_joke",
#                             "description": "generate or tell jokes",
#                             "parameters": {},
#                             "required": {},
#                         }
#                     },
#                     {
#                         "type": "function",
#                         "function": {
#                             "name": "calculate",
#                             "description": "Evaluate a mathematical expression",
#                             "parameters": {
#                                     "expression": {
#                                         "type": "string",
#                                         "description": "The mathematical expression to evaluate"
#                                     }
#                                 },
#                             "required": ["expression"],
#                         }
#                     },
#                     {
#                         "type": "function",
#                         "function": {
#                             "name": "web_search",
#                             "description": "Perform a web search using the Google Custom Search JSON API",
#                             "parameters": {
#                                 "query": {
#                                     "type": "string",
#                                     "description": "The search query"
#                                 }
#                             },
#                             "required": ["query"]
#                         }
#                     },
#                 ],
#                 tool_choice="auto"
#             )
#             model_response = response.choices[0].message
#             # tool call variable
#             tool_calls = model_response.tool_calls
#             print("Prove that the model call for tools: ", tool_calls) # printing the response because I don't trust the AI using tools
#             # check if the model need to call tools
#             if tool_calls:
#                 available_functions = {
#                     "get_joke": get_joke,
#                     "calculate": calculate,
#                     "web_search": lambda query: google_web_search(query)
#                 }

#                 # Process each tool call
#                 for tool_call in tool_calls:
#                     function_name = tool_call.function.name
#                     function_to_call = available_functions[function_name]
#                     function_args = json.loads(tool_call.function.arguments)
                    
#                     # Call the tool and get the response
#                     # if function_name == "get_joke":
#                     #     function_response = function_to_call()
#                     # elif function_name == "get_weather":
#                     #     function_response = function_to_call(location=function_args.get("location"))
                    
#                     match function_name:
#                         case "get_joke":
#                             function_response = function_to_call()
#                         case "calculate":
#                             function_response = function_to_call(expression=function_args.get("expression"))
#                         case "web_search":
#                             function_response = function_to_call(query=function_args.get("query"))

#                     # Add the tool response to the conversation
#                     message.append(
#                         {
#                             "tool_call_id": tool_call.id,
#                             "role": "tool",  # Indicates this message is from tool use
#                             "name": function_name,
#                             "content": function_response,
#                         }
#                     )
#                     for msg in message:
#                         if msg["role"] == "user":
#                             msg["content"] += "summarize your findings in 50 to 150 tokens"

#                 # Make a second API call with the updated conversation
#                 second_response = self.client.chat.completions.create(
#                     model="llama-3.1-70b-versatile",
#                     messages=message,
#                     temperature=self.Params['temperature'],
#                     max_tokens=self.Params['max_tokens'],
#                     top_p=0.9,
#                     frequency_penalty=self.Params['frequency_penalty'],
#                     presence_penalty=self.Params['presence_penalty']
#                 )
#                 return second_response.choices[0].message.content
#             return response.choices[0].message.content
#         except Exception as e:
#             raise (f"Error generating response: {e}")
    
#     def groqVision(self, img_path):
#         completion = self.client.chat.completions.create(
#             model="llama-3.2-11b-vision-preview",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {
#                             "type": "text",
#                             "text": "Describe what's in the image in short. Your token is limited to 100"
#                         },
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": img_path
#                             }
#                         }
#                     ]
#                 }
#             ],
#             temperature=0,
#             max_tokens=500,
#             top_p=1,
#             stream=False,
#             stop=None,
#         )
#         return completion.choices[0].message.content

from groq import Groq
import json
from chatbot.tools.makeJokes import get_joke
from chatbot.tools.makeCalculations import calculate
from chatbot.tools.makeSearch import google_web_search

class ChatEngine:
    def __init__(self, api_key=None, model = None):
        if not api_key:
            raise ValueError("API key is required to initialize Groq.")
        self.client = Groq(api_key=api_key)

        # Define models
        self.ROUTING_MODEL = "llama3-70b-8192"
        self.TOOL_USE_MODEL = "llama3-groq-70b-8192-tool-use-preview"
        self.GENERAL_MODEL = "gemma2-9b-it"
        self.UTILITY_TOOLS = "llama-3.1-70b-versatile"

        # Available tools
        self.tools = {
            "get_joke": get_joke,
            "calculate": calculate,
            "web_search": lambda query: google_web_search(query),
        }

    def route_query(self, query):
        """Determine whether tools are needed and which tool to use"""
        routing_prompt = f"""
        Given the following user query, determine if any tools are needed to answer it.
        If a specific tool is needed, respond with 'TOOL: <TOOL_NAME>'.
        Available tools are: {', '.join(self.tools.keys())}.
        If no tools are needed, respond with 'NO TOOL'.

        User query: {query}

        Response:
        """
        response = self.client.chat.completions.create(
            model=self.ROUTING_MODEL,
            messages=[
                {"role": "system", "content": "You are a routing assistant. Determine the correct tool based on the user query."},
                {"role": "user", "content": routing_prompt}
            ],
            max_tokens=20
        )
        routing_decision = response.choices[0].message.content.strip()
        print(routing_decision)
        if "TOOL:" in routing_decision:
            tool_name = routing_decision.split(":")[1].strip().lower()
            return tool_name if tool_name in self.tools else "no tool"
        return "no tool"

    def run_with_tool(self, tool_name, query):
        """Handle queries requiring tools using TOOL_USE_MODEL"""
        messages = [
            {"role": "system", "content": f"You are an assistant using the {tool_name} tool to answer user queries. Summarize your answer in 100 until 200 tokens"},
            {"role": "user", "content": query},
        ]
        response = self.client.chat.completions.create(
            model=self.TOOL_USE_MODEL,
            messages=messages,
            max_tokens=4096,
            tool_choice="auto"
        )
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            messages.append(response.choices[0].message)
            for tool_call in tool_calls:
                function_args = json.loads(tool_call.function.arguments)
                tool_response = self.tools[tool_name](**function_args)
                messages.append({"tool_call_id": tool_call.id, "role": "tool", "name": tool_name, "content": tool_response})

            final_response = self.client.chat.completions.create(
                model=self.TOOL_USE_MODEL,
                messages=messages
            )
            return final_response.choices[0].message.content
        return response.choices[0].message.content

    def generate_response(self, query, system_prompt):
        """Handle queries not requiring tools using the GENERAL_MODEL"""
        response = self.client.chat.completions.create(
            model=self.GENERAL_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.75,
            max_tokens=300,
            frequency_penalty=1.7,
            top_p=0.5,
            presence_penalty=0.5
        )
        return response.choices[0].message.content

    def process_query(self, query, system_prompt):
        """Route the query and execute it with the appropriate tool or model"""
        route = self.route_query(query)
        if route in self.tools:
            print("Tool used:", route)
            tool_response = self.run_with_tool(route, query)
            query += "You just used tool to do something and here is the result" + tool_response
            response = self.generate_response(query, system_prompt)
        else:
            response = self.generate_response(query, system_prompt)
        return response
    
    def generate_response_for_utils(self, context, rules):
        message = [
            {"role": "system", "content": rules},
            {"role": "user", "content": context}
        ]
        try:
            response = self.client.chat.completions.create(
                messages=message,
                model=self.UTILITY_TOOLS,
                temperature=0,
                max_tokens=500,
                top_p = 0.9,
                frequency_penalty=1.7,
                presence_penalty=0.7,
                
            )
            model_response = response.choices[0].message
            
            return model_response.content
        except Exception as e:
            raise (f"Error generating response: {e}")

    def groqVision(self, img_path):
            completion = self.client.chat.completions.create(
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