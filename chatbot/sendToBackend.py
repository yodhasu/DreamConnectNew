from transformers import pipeline
import requests

class backend():
    def __init__(self):
        try:
            self.classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None, device=0)
        except:
            self.classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
    
    def classify_emotion(self, message):
        """Classify emotions of a response."""
        emotions = self.classifier(message)
        return [emotions[0][i]['label'] for i in range(3)]
    
    def send_to_space(self, message = None):
        """Send classified emotions to the backend."""
        emotion = self.classify_emotion(message=message)
        data = {'response': emotion}
        try:
            response = requests.post(
                'http://127.0.0.1:8080/send_message',
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error sending message to backend: {e}")
