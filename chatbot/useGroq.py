from groq import Groq

class ChatEngine:
    def __init__(self, model = "llama3-groq-70b-8192-tool-use-preview", api_key = None, params=None):
        if api_key:
            self.Client = Groq(api_key=api_key)
        else:
            raise ValueError("API KEY needed, please get your groq API key at https://console.groq.com/keys")
        self.Model = model
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
            response = self.Client.chat.completions.create(
                messages=message,
                model=self.Model,
                temperature=self.Params['temperature'],
                max_tokens=self.Params['max_tokens'],
                top_p = 0.9,
                frequency_penalty=self.Params['frequency_penalty'],
                presence_penalty=self.Params['presence_penalty']
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
