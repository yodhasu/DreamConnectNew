import edge_tts
import langdetect
from langdetect import detect
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
import pygame
import os

class SimpleTTS:
    def __init__(self):
        self.audiofile = "myTTS/voiceline.wav"
        self.pcm_audiofile = "myTTS/voiceline_pcm.wav"
    
    def checkLang(self, text):
        detected = detect(text=text)
        lang_to_voice = {
            "en": "en-US-MichelleNeural",    # English (US)
            "es": "es-ES-ElviraNeural", # Spanish (Spain)
            "fr": "fr-FR-DeniseNeural", # French (France)
            "de": "de-DE-KatjaNeural",  # German (Germany)
            "ja": "ja-JP-NanamiNeural", # Japanese
            "zh": "zh-CN-XiaoxiaoNeural" # Chinese (Simplified)
        }
        # Default to English if language not supported
        return lang_to_voice.get(detected, "en-US-MichelleNeural")
    
    async def createTTS(self, text):
        lang = self.checkLang(text=text)
        tts = edge_tts.Communicate(text=text, voice=lang, rate="+13%", pitch="+15Hz")
        await tts.save(self.audiofile)
        
        # Convert to PCM format for pygame compatibility
        sound = AudioSegment.from_file(self.audiofile)
        sound.export(self.pcm_audiofile, format="wav")

        # Play the audio using pygame
        pygame.mixer.init()
        pygame.mixer.music.load(self.pcm_audiofile)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pass
        
        pygame.mixer.music.unload()
        