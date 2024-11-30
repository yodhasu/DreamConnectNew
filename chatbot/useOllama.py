import json
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
from chatbot.tools.makeJokes import get_joke
from chatbot.tools.makeCalculations import calculate
from chatbot.tools.makeSearch import google_web_search

class ChatEngine:
    def __init__(self, model="llama3.2:1b", base_url="http://localhost:8000"):
        """
        Initialize the ChatOllama client with the specified model and base URL.
        """
        self.client = ChatOllama(model=model, temperature=0, repeat_penalty=1, top_p=0.5, top_k=1, num_predict=500)

        # Available tools
        self.tools = {
            "get_joke": get_joke,
            "calculate": calculate,
            "web_search": lambda query: google_web_search(query),
        }

    def route_query(self, query):
        """
        Determine whether tools are needed and which tool to use.
        """
        routing_prompt = f"""
        You are a routing assistant. Based on the user query, decide if a tool is needed.
        If a specific tool is required, respond with 'TOOL: <TOOL_NAME>'.
        Available tools: {', '.join(self.tools.keys())}.
        If no tools are required, respond with 'NO TOOL'.

        User query: {query}

        Response:
        """
        messages = [
            SystemMessage(content="You are a routing assistant."),
            HumanMessage(content=routing_prompt)
        ]
        response = self.client.invoke(messages)
        routing_decision = response.content.strip()
        print(f"Routing decision: {routing_decision}")
        if "TOOL:" in routing_decision:
            tool_name = routing_decision.split(":")[1].strip().lower()
            return tool_name if tool_name in self.tools else "no tool"
        return "no tool"

    def run_with_tool(self, tool_name, query):
        """
        Handle queries requiring tools.
        """
        tool_function = self.tools.get(tool_name)
        if not tool_function:
            raise ValueError(f"Tool {tool_name} not found.")

        # Execute the tool and get the response
        tool_response = tool_function(query)
        return f"Tool '{tool_name}' response: {tool_response}"

    def generate_response(self, query, system_prompt):
        """
        Generate response using the ChatOllama model.
        """
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
        response = self.client.invoke(messages)
        return response.content

    def process_query(self, query, system_prompt):
        """
        Route the query and process it with tools or directly with the model.
        """
        route = self.route_query(query)
        if route in self.tools:
            print(f"Using tool: {route}")
            tool_response = self.run_with_tool(route, query)
            final_query = f"{query}\n\nTool result: {tool_response}"
            response = self.generate_response(final_query, system_prompt)
        else:
            response = self.generate_response(query, system_prompt)
        return response
   
    # def ollama_vision(self, img_path):
    #     """Process an image using Ollama's vision capabilities (if supported)"""
    #     response = ChatResponse(
    #         model="llava",
    #         messages=[
    #             {"role": "user", "content": {
    #                 "type": "image",
    #                 "path": img_path
    #             }},
    #             {"role": "user", "content": "Describe the image in a short and concise way."}
    #         ],
    #         max_tokens=200
    #     )
    #     return response.content if response else "No description available."
