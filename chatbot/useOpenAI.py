import openai

class ChatEngine:
    def __init__(self, model="gpt-4", api_key=None, params=None):
        if api_key:
            openai.api_key = api_key
        else:
            raise ValueError("API key is required for OpenAI API.")
        
        self.Model = model or "gpt-4"
        self.Params = params or {
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
            response = openai.ChatCompletion.create(
                model=self.Model,
                messages=message,
                temperature=self.Params['temperature'],
                max_tokens=self.Params['max_tokens'],
                frequency_penalty=self.Params['frequency_penalty'],
                presence_penalty=self.Params['presence_penalty']
            )
            return response.choices[0].message['content']
        except Exception as e:
            print(f"Error generating response: {e}")
            return None