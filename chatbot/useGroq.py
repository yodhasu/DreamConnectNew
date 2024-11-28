from groq import Groq

class ChatEngine:
    def __init__(self, model = "llama3-groq-70b-8192-tool-use-preview", api_key = None, params=None):
        if api_key:
            self.Client = Groq(api_key=api_key)
        else:
            raise ValueError("API KEY needed, please get your groq API key at https://console.groq.com/keys")
        self.Model = model or "llama3-groq-70b-8192-tool-use-preview"
        self.Params = params or {
            'temperature': 0.85,
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
                presence_penalty=self.Params['presence_penalty']
            )
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
        