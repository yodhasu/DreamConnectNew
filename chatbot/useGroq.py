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
        self.GENERAL_MODEL = "llama-3.1-70b-versatile"
        self.UTILITY_TOOLS = "llama-3.1-70b-versatile"

        # Available tools
        self.tools = {
            "get_joke": get_joke,
            "calculate": calculate,
            "web_search": lambda query: google_web_search(query),
        }
        self.tools_details = [
            # {
            #     "type": "function",
            #     "function": {
            #         "name": "name",
            #         "description": "function description",
            #         "parameters": {
            #             "type": "object",
            #             "properties": {
            #                 # all parameters needed
                            
            #             },
            #             "required": ["required_parameters"],
            #         },
            #     },
            # },
            {
                "type": "function",
                "function": {
                    "name": "get_joke",
                    "description": "tell or generate random jokes",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            # all parameters needed
                            
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "ONLY TO Evaluate or calculate basic math problems, not for coding.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            # all parameters needed
                            "expression": {
                                "type": "string",
                                "description": "The mathematical expression to evaluate",
                            },
                        },
                        "required": ["expression"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search something on internet or Google, use Google search API.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            # all parameters needed
                            "query": {
                                "type": "string",
                                "description": "Things that needed to be search on Google or internet.",
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
        ]

    def route_query(self, query):
        """Determine whether tools are needed and which tool to use"""
        routing_prompt = f"""
        Given the following user query, determine if any tools are needed to answer it.
        If a specific tool is needed, respond with 'TOOL: <TOOL_NAME>'.
        Available tools are: {', '.join(self.tools.keys())}.
        If no tools are needed, respond with 'NO TOOL'.
        no tools for coding.

        User query: {query}

        Response:
        """
        response = self.client.chat.completions.create(
            model=self.ROUTING_MODEL,
            messages=[
                {"role": "system", "content":f"You are a routing assistant with this list of tools {self.tools}. Determine the correct tool based on the user query."},
                {"role": "user", "content": routing_prompt}
            ],
            max_tokens=20,
            temperature=0
        )
        routing_decision = response.choices[0].message.content.strip()
        print(routing_decision)
        if "TOOL:" in routing_decision:
            tool_name = routing_decision.split(":")[1].strip().lower()
            return tool_name if tool_name in self.tools else "no tool"
        return "no tool"

    def run_with_tool(self, tool_name, query):
        """Handle queries requiring tools using TOOL_USE_MODEL"""
        tool_messages = [
            {"role": "system", "content": f"You are an assistant using the {tool_name} tool to answer user queries. Use {tool_name} function to generate response. If you use 'web_search' tool make ssure to list the links you got. Only use tools if the purpose is related with the tool functionalities, other than that skip the tools."},
            {"role": "user", "content": query}
        ]
        response = self.client.chat.completions.create(
            model=self.TOOL_USE_MODEL,
            messages=tool_messages,
            max_tokens=4096,
            tools= self.tools_details,
            tool_choice="required"
        )
        first_message = response.choices[0].message
        tool_calls = first_message.tool_calls
        print("Call for tools: ", tool_calls)
        if tool_calls:
            try:
                tool_messages.append(first_message.content)
                for tool_call in tool_calls:
                    function_args = json.loads(tool_call.function.arguments)
                    print("Args: ", function_args)
                    # tool_response = self.tools[tool_name](**function_args)
                    match tool_name:
                        case "web_search":
                            funcion_response = google_web_search(function_args.get("query"))
                        case "evaluate":
                            funcion_response = calculate(function_args.get("expression"))
                        case "get_joke":
                            funcion_response =get_joke()
                    print("Function Response", funcion_response)
                    print("Old message", tool_messages)
                    tool_messages.pop()
                    print("Popped message", tool_messages)
                    print("Message len", len(tool_messages))
                    tool_messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": tool_name,
                            "content": funcion_response,
                        }
                    )
                    print("Message len", len(tool_messages))
                    print("New message: ", tool_messages)
                final_response = self.client.chat.completions.create(
                    model=self.TOOL_USE_MODEL,
                    messages=tool_messages
                )
                print("The tool is working")
                return final_response.choices[0].message.content
            except:
                return
                

    def generate_response(self, query, system_prompt):
        """Handle queries not requiring tools using the GENERAL_MODEL"""
        response = self.client.chat.completions.create(
            model=self.GENERAL_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.95,
            max_tokens=300,
            frequency_penalty=1.9,
            presence_penalty=0.7
        )
        return response.choices[0].message.content

    def process_query(self, query, system_prompt, inputs):
        """
        Routes the query and executes it using the appropriate tool or model.
        
        Args:
            query (str): The user's input query.
            system_prompt (str): The current system prompt state.
            inputs (dict): Additional inputs required by the tools.
        
        Returns:
            str: The generated response from the tool or model.
        """
        # Determine the routing destination for the query
        route = self.route_query(query)
        
        if route in self.tools:
            print("Tool used:", route)
            tool_response = self.run_with_tool(route, inputs)
            print("Tool Response:", tool_response)
            
            # Check if the tool response is valid
            if tool_response:
                # Update the system prompt with tool result
                system_prompt += (
                    "You just used a tool to do something and here is the result:\n"
                    f"{tool_response}\n"
                    "Based on this result, you are required to state and explain what you got.\n"
                )
            else:
                print("Tool did not return a valid response.")
        
        # Generate a response based on the updated system prompt
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
                max_tokens=200,
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