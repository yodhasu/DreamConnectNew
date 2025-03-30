# import time
# from groq import Groq
# import json
# from googleSearch import google_web_search

# class AIengine:
#     def __init__(self, key=None):
#         self.client = Groq(api_key=key)
        
#         # Define models
#         self.ROUTING_MODEL = "llama-3.1-8b-instant"
#         self.TOOL_USE_MODEL = "llama3-70b-8192"
#         self.GENERAL_MODEL = "gemma2-9b-it"
#         self.UTILITY_TOOLS = "llama3-70b-8192"

#         # Available tools
#         self.tools = {
#             "web_search": lambda query: google_web_search(query),
#         }
#         self.tools_details = [
#             {
#                 "type": "function",
#                 "function": {
#                     "name": "web_search",
#                     "description": "Search something on internet or Google, use Google search API.",
#                     "parameters": {
#                         "type": "object",
#                         "properties": {
#                             "query": {
#                                 "type": "string",
#                                 "description": "Things that needed to be search on Google or internet.",
#                             },
#                         },
#                         "required": ["query"],
#                     },
#                 },
#             }
#         ]
    
#     def route_query(self, query):
#         """Determine whether tools are needed and which tool to use"""
#         routing_prompt = f"""
#         Given the following user query, determine if any tools are needed to answer it.
#         If a specific tool is needed, respond with 'TOOL: <TOOL_NAME>'.
#         Available tools are: {', '.join(self.tools.keys())}.
#         If no tools are needed, respond with 'NO TOOL'.
#         no tools for coding.

#         User query: {query}

#         Response:
#         """
#         response = self.client.chat.completions.create(
#             model=self.ROUTING_MODEL,
#             messages=[
#                 {"role": "system", "content":f"You are a routing assistant with this list of tools {self.tools}. Determine the correct tool based on the user query. No permission needed to use any tools"},
#                 {"role": "user", "content": routing_prompt}
#             ],
#             max_tokens=20,
#             temperature=0
#         )
#         routing_decision = response.choices[0].message.content.strip().lower()
#         tool_name = "no tool"

#         # Check for 'tool: <name>' pattern
#         if 'tool:' in routing_decision:
#             tool_part = routing_decision.split('tool:', 1)[1].strip()
#             # Extract first word after tool: marker
#             tool_candidate = tool_part.split()[0].strip()
#             if tool_candidate in self.tools:
#                 tool_name = tool_candidate
#         else:
#             # Check if any tool name appears in the response
#             for tool in self.tools.keys():
#                 if tool in routing_decision:
#                     tool_name = tool
#                     break

#         return tool_name if tool_name in self.tools else "no tool"

#     def run_with_tool(self, tool_name, query):
#         """Handle queries requiring tools using TOOL_USE_MODEL"""
#         try:
#             tool_messages = [
#                 {"role": "system", "content": f"You are an assistant using the {tool_name} tool to answer user queries. Use {tool_name} function to generate response. If you use 'web_search' tool make sure to list the links you got. No permission needed to access every tools"},
#                 {"role": "user", "content": query}
#             ]
#             response = self.client.chat.completions.create(
#                 model=self.TOOL_USE_MODEL,
#                 messages=tool_messages,
#                 max_tokens=4096,
#                 tools= self.tools_details,
#                 tool_choice="auto"
#             )
#             first_message = response.choices[0].message
#             tool_calls = first_message.tool_calls
#             if tool_calls:
#                 try:
#                     tool_messages.append(first_message)
#                     for tool_call in tool_calls:
#                         function_args = json.loads(tool_call.function.arguments)
#                         if tool_name == "web_search":
#                             funcion_response = google_web_search(function_args.get("query"))
#                         # Add other tools here if needed
                        
#                         tool_messages.append(
#                             {
#                                 "tool_call_id": tool_call.id,
#                                 "role": "tool",
#                                 "content": str(funcion_response),
#                             }
#                         )
#                     final_response = self.client.chat.completions.create(
#                         model=self.TOOL_USE_MODEL,
#                         messages=tool_messages,
#                         tool_choice="auto",
#                         max_tokens=4096
#                     )
#                     return final_response.choices[0].message.content
#                 except Exception as e:
#                     return f"Can not use tool {tool_name} because of an error with message {e}"
#         except Exception as e:
#             return f"Can not use tool {tool_name} because of an error with message {e}"

#     # ... rest of the class methods remain unchanged (generate_response, process_query, etc) ...

#     def generate_response(self, query, system_prompt):
#         """Handle queries not requiring tools using the GENERAL_MODEL"""
#         response = self.client.chat.completions.create(
#             model=self.GENERAL_MODEL,
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": query}
#             ],
#             temperature=0.85,
#             max_tokens=2042,
#             frequency_penalty=1.9,
#             presence_penalty=0.7
#         )
#         return response.choices[0].message.content

#     def process_query(self, usr_prompt, system_prompt, input):
#         time.sleep(1)
#         route = self.route_query(input)
        
#         if route in self.tools:
#             print("Tool used:", route)
#             tool_response = self.run_with_tool(route, input)
#             print("Tool Response:", tool_response)
            
#             if tool_response:
#                 usr_prompt += f"You just used a tool to do something and here is the result:\n{tool_response}\nBased on this result, you are required to state and explain in detail what you got. If you got links show the links.\n"
#             else:
#                 usr_prompt += "\nNo tool is used\n"
        
#         response = self.generate_response(usr_prompt, system_prompt)
#         return response

#     def generate_response_for_utils(self, context, rules):
#         message = [
#             {"role": "system", "content": rules},
#             {"role": "user", "content": context}
#         ]
#         try:
#             response = self.client.chat.completions.create(
#                 messages=message,
#                 model=self.UTILITY_TOOLS,
#                 temperature=0,
#                 max_tokens=100,
#                 top_p = 0.9,
#                 frequency_penalty=1.7,
#                 presence_penalty=0.7,
                
#             )
#             model_response = response.choices[0].message
            
#             return model_response.content
#         except:
#             raise Exception

#     def groqVision(self, query, img_path):
#             completion = self.client.chat.completions.create(
#                 model="llama-3.2-11b-vision-preview",
#                 messages=[
#                     {
#                         "role": "user",
#                         "content": [
#                             {
#                                 "type": "text",
#                                 "text": query
#                             },
#                             {
#                                 "type": "image_url",
#                                 "image_url": {
#                                     "url": img_path
#                                 }
#                             }
#                         ]
#                     }
#                 ],
#                 temperature=0,
#                 max_tokens=1024,
#                 top_p=1,
#                 stream=False,
#                 stop=None,
#             )
#             return completion.choices[0].message.content