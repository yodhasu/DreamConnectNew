import time
from groq import Groq
import json
from nltk.tokenize import word_tokenize
from numpy import append
from chatbot.tools.makeJokes import get_joke
from chatbot.tools.makeCalculations import calculate
from chatbot.tools.makeSearch import google_web_search
from chatbot.tools.seeImg import see_screenshot
# from chatbot.tools.taskReminderShort import TaskReminder

# reminder = TaskReminder()

class ChatEngine:
    def __init__(self, api_key=None, model = None):
        if not api_key:
            raise ValueError("API key is required to initialize Groq.")
        self.client = Groq(api_key=api_key)

        # Define models
        self.ROUTING_MODEL = "llama-3.1-8b-instant"
        self.TOOL_USE_MODEL = "llama3-70b-8192"
        self.GENERAL_MODEL = "llama-3.3-70b-specdec"
        self.UTILITY_TOOLS = "llama3-70b-8192"

        # Available tools
        self.tools = {
            "get_joke": get_joke,
            "calculate": calculate,
            "see_screenshot": lambda prompt: see_screenshot(prompt),
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
            {
                "type": "function",
                "function": {
                    "name": "see_screenshot",
                    "description": "view the user screen.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            # all parameters needed
                            "prompt": {
                                "type": "string",
                                "description": "Things that needed to be see or processed. Could be a specific task that the user wants or needs from the image.",
                            },
                        },
                        "required": ["prompt"],
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
                {"role": "system", "content":f"You are a routing assistant with this list of tools {self.tools}. Determine the correct tool based on the user query. No permission needed to use any tools"},
                {"role": "user", "content": routing_prompt}
            ],
            max_tokens=20,
            temperature=0
        )
        routing_decision = response.choices[0].message.content
        print(routing_decision)
        tokenize_route = [word for word in word_tokenize(routing_decision)]
        try:
            tool_name = [tools for tools in tokenize_route if tools in self.tools.keys()]
            return tool_name[0] if len(tool_name) != 0 and tool_name[0] in self.tools else "no tool"
        except:
            return "no tool"

    def run_with_tool(self, tool_name, query):
        """Handle queries requiring tools using TOOL_USE_MODEL"""
        try:
            tool_messages = [
                {"role": "system", "content": f"You are an assistant using the {tool_name} tool to answer user queries. Use {tool_name} function to generate response. If you use 'web_search' tool make ssure to list the links you got. No permission needed to access every tools"},
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
            print(f"Tools msg: {first_message}")
            print("Call for tools: ", tool_calls)
            time.sleep(1)
            if tool_calls:
                try:
                    tool_messages.append(first_message)
                    for tool_call in tool_calls:
                        function_args = json.loads(tool_call.function.arguments)
                        print("Args: ", function_args)
                        time.sleep(1)
                        # tool_response = self.tools[tool_name](**function_args)
                        match tool_name:
                            case "web_search":
                                funcion_response = google_web_search(function_args.get("query"))
                            case "evaluate":
                                funcion_response = calculate(function_args.get("expression"))
                            case "get_joke":
                                funcion_response =get_joke()
                            case "see_screenshot":
                                print("seeing image...")
                                funcion_response =see_screenshot(function_args.get("prompt"))
                        try:
                            if tool_messages['name'] is tool_name:
                                break
                        except:
                            pass
                        tool_messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "content": str(funcion_response),
                            }
                        )
                        print("Function Response", funcion_response)
                        time.sleep(1)
                    print("==================================\nMessage len", len(tool_messages))
                    print(f"All messages: {tool_messages}\n================================")
                    time.sleep(1)
                    final_response = self.client.chat.completions.create(
                        model=self.TOOL_USE_MODEL,
                        messages=tool_messages,
                        tool_choice="auto",
                        max_tokens=4096
                    )
                    print("The tool is working")
                    print(f"Tools Results:\n\n{final_response.choices[0].message.content}\n\n========================================")
                    time.sleep(1)
                    return final_response.choices[0].message.content
                except Exception as e:
                    print(f"Error occured: {e}")
                    return f"Can not use tool {tool_name} because of an error with message {e}"
        except Exception as e:
            print(f"Error occured: {e}")
            return f"Can not use tool {tool_name} because of an error with message {e}"
                

    def generate_response(self, query, system_prompt):
        """Handle queries not requiring tools using the GENERAL_MODEL"""
        print(f"\n\nQuery:\n\n{query}")
        response = self.client.chat.completions.create(
            model=self.GENERAL_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.85,
            max_tokens=2042,
            frequency_penalty=1.9,
            presence_penalty=0.7
        )
        return response.choices[0].message.content

    def process_query(self, query, system_prompt, input):
        """
        Routes the query and executes it using the appropriate tool or model.
        
        Args:
            query (str): The user's input query.
            system_prompt (str): The current system prompt state.
        
        Returns:
            str: The generated response from the tool or model.
        """
        print(f"Input query: {query}")
        time.sleep(1)
        # Determine the routing destination for the query
        route = self.route_query(input)
        
        if route in self.tools:
            print("Tool used:", route)
            tool_response = self.run_with_tool(route, input)
            print("Tool Response:", tool_response)
            
            # Check if the tool response is valid
            if tool_response:
                # Update the system prompt with tool result
                query +=f"""
                    \n\n
                    You just used a tool to do something and here is the result:\n
                    {tool_response}\n
                    Based on this result, you are required to state and explain what you got.\n     
                """
                    
                
            else:
                print("Tool did not return a valid response.")
                query += "\nNo tool is used\n"
        
        # Generate a response based on the updated system prompt
        print(f"Query fed into generate_response:\n{query}")
        time.sleep(1)
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
                max_tokens=100,
                top_p = 0.9,
                frequency_penalty=1.7,
                presence_penalty=0.7,
                
            )
            model_response = response.choices[0].message
            
            return model_response.content
        except:
            raise Exception

    def groqVision(self, img_path):
            completion = self.client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe the image. Your token is limited to 1000"
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
                max_tokens=2042,
                top_p=1,
                stream=False,
                stop=None,
            )
            return completion.choices[0].message.content