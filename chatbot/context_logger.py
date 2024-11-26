import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag
from datetime import datetime
import difflib
import os

nltk.data.clear_cache()
# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('maxent_ne_chunker_tab')
nltk.download('words')
nltk.download('vader_lexicon')

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

class ContextLogger:
    def __init__(self):
        # Initialize necessary components
        self.sia = SentimentIntensityAnalyzer()
        self.context_log = []
        self.previous_responses = []

    def extract_named_entities(self, text):
        """
        Extracts named entities from the given text using NLTK.
        """
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        named_entities = ne_chunk(pos_tags)
        
        entities = []
        for chunk in named_entities:
            if hasattr(chunk, 'label'):  # Extract named entity phrases
                entity = ' '.join(c[0] for c in chunk)
                entities.append((entity, chunk.label()))
        return entities

    def detect_emotion(self, text):
        """
        Detects the emotional tone of the given text using VADER sentiment analysis.
        """
        sentiment = self.sia.polarity_scores(text)
        if sentiment['compound'] > 0.5:
            return "positive emotion"
        elif sentiment['compound'] < -0.5:
            return "negative emotion"
        else:
            return "neutral tone"

    def detect_off_topic(self, user_message, character_response):
        """
        Detects if the character's response is off-topic based on user input using SpaCy.
        """
        # Process both the user message and character response using SpaCy
        user_doc = nlp(user_message)
        response_doc = nlp(character_response)
        
        # Extract named entities or keywords from user message
        user_keywords = [ent.text.lower() for ent in user_doc.ents]
        
        # Check if response contains any of the keywords or entities
        for keyword in user_keywords:
            if keyword in response_doc.text.lower():
                return False  # Response is on-topic
        return True  # Response is off-topic

    def check_response_length(self, response, max_length=50):
        """
        Checks if the response is too long.
        """
        word_count = len(response.split())
        if word_count > max_length:
            return "Response too long"
        return None

    def check_repetitiveness(self, response):
        """
        Checks if the response is repetitive compared to previous responses.
        """
        for prev_response in self.previous_responses:
            similarity = difflib.SequenceMatcher(None, response.lower(), prev_response.lower()).ratio()
            if similarity > 0.7:  # If the similarity is high (e.g., more than 70%)
                return "Repetitive"
        self.previous_responses.append(response)  # Store the response
        return None

    def classify_response(self, response):
        """
        Classifies the response as 'Good' or 'Bad' based on sentiment.
        """
        sentiment = self.sia.polarity_scores(response)
        if sentiment['compound'] > 0.1:
            return "Good Response"
        elif sentiment['compound'] < -0.1:
            return "Bad Response"
        return "Neutral Response"

    def log_context(self, user_message, character_response):
        """
        Processes a single dialogue and logs it with context information, including off-topic detection.
        """
        # Detect emotion and extract entities from both user and character responses
        entities_user = self.extract_named_entities(user_message)
        entities_response = self.extract_named_entities(character_response)
        emotion_user = self.detect_emotion(user_message)
        emotion_response = self.detect_emotion(character_response)
        
        # Detect off-topic based on the user message and character's response
        off_topic = self.detect_off_topic(user_message, character_response)

        # Check if response is too long, repetitive or good/bad
        response_length = self.check_response_length(character_response)
        repetitiveness = self.check_repetitiveness(character_response)
        response_quality = self.classify_response(character_response)

        # Create a timestamped log entry
        timestamp = datetime.now().strftime("%d/%m/%y - %H:%M:%S")

        # Create sentence for logging based on context
        # if entities_user or entities_response:
        #     user_entities = ', '.join(e[0] for e in entities_user)
        #     response_entities = ', '.join(e[0] for e in entities_response)
        #     sentence = f"[{timestamp}] User: {user_entities} mentioned, Response: {response_entities} mentioned, Emotion: {emotion_response}, Off-topic: {'Yes' if off_topic else 'No'}, {response_length if response_length else ''} {repetitiveness if repetitiveness else ''} {response_quality}"
        # else:
        sentence = f"[{timestamp}] User: '{user_message}' expressed {emotion_user}, Character: '{character_response}' expressed {emotion_response}, Off-topic: {'Yes' if off_topic else 'No'}, {response_length if response_length else ''} {repetitiveness if repetitiveness else ''} {response_quality}"

        # Add the dialogue to the context log
        self.context_log.append(sentence)

    def get_context_log(self):
        """
        Returns the full context log as a list of sentences.
        """
        return self.context_log

    def save_context_log(self, filename):
        """
        Saves the context log to a file.
        """
        with open(filename, "w") as file:
            for entry in self.context_log:
                file.write(f"{entry}\n")
