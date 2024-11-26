import ollama
from ollama import chat

class ChatEngine:
    def __init__(self, model="llama3", params=None):
        self.model = model or "llama3"
        self.params = params or {
            'temperature': 0.85,
            'max_tokens': 64,
            'frequency_penalty': 1.7,
            'presence_penalty': 1.7,
        }

    def generate_response(self, context, rules):
        message = [
            {"role": "system", "content": rules},
            {"role": "user", "content": context}
        ]
        try:
            response = chat(model=self.model, messages=message)
            return response.message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
