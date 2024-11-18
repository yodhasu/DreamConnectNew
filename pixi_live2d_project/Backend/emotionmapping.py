import json
from collections import Counter

def load_emotion_mapping(file_path):
    emotion_mapping = {}
    with open(file_path, 'r') as f:
        for line in f:
            original, narrowed = line.strip().split(' : ')
            emotion_mapping[original.strip("'")] = narrowed.strip("'")
    return emotion_mapping

def narrow_emotions(emotion_list, emotion_mapping):
    narrowed_emotions = [emotion_mapping.get(emotion, 'neutral') for emotion in emotion_list]
    return narrowed_emotions

def get_most_frequent_emotion(narrowed_emotions):
    emotion_counter = Counter(narrowed_emotions)
    most_frequent_emotion = emotion_counter.most_common(1)[0][0]
    return most_frequent_emotion
