import asyncio
from io import BytesIO
import sys
import time

from numpy import save
import pygame
from speechRecognition.sr import SpeakerVerification
from speechRecognition.record import BackgroundAudioRecorder
from myTTS.simpletts import SimpleTTS
from chatbot.context_logger import ContextLogger
import re
import os

class ListenToPrompt:
    def __init__(self, silence_timeout=2):
        self.recorder = BackgroundAudioRecorder()
        self.silence_timeout = silence_timeout  # Time to wait before saving
        self.buffer = BytesIO()  # Store audio in memory before saving
        self.last_sound_time = None
        self.speakverif = SpeakerVerification(reference_audio_path=r"C:\Users\Axioo Pongo\OneDrive\Documents\Sound Recordings\reference_speaker.wav")
        self.save_audio = "speechRecognition/recorded.wav"
        self.audio_name = "recorded.wav"
        self.tts = SimpleTTS()
        self.context = ContextLogger()
        
    def remove_asterisk_phrases(self, text):
        # Regular expression to match text between two asterisks
        return re.sub(r'\*.*?\*', '', text).strip()


    def start_listening(self, chat_module, api, filelike):
        
        """
        Start listening and process audio, saving it after silence timeout.
        """
        try:
            chat_module.retrieve_memory()
            while True:
                if len(self.context.get_context_log()) == 15:
                    chat_module.retrieve_memory()
                self.recorder.record_audio()
                verify = self.speakverif.verify(self.save_audio)
                try:
                    print(f"Score: {verify['score']}, Prediction: {verify['pred']}")
                    time.sleep(3)
                    # filepath = ""
                    if verify['pred'] or verify['score'] > 0.3:
                        # for root, dirs, files in os.walk("."):
                        #     if self.audio_name in files:
                        #         filepath = os.path.abspath(os.path.join(root, self.audio_name))
                        #         print(f"File found: {filepath}")
                        #         break
                        print(f"recording saved to {self.save_audio}")
                        time.sleep(3)
                        # Play the audio using pygame
                        print("Playing audio...")
                        pygame.mixer.init()
                        pygame.mixer.music.load(self.save_audio)
                        pygame.mixer.music.play()

                        # Wait for the audio to finish playing
                        while pygame.mixer.music.get_busy():
                            pass
                        
                        pygame.mixer.music.unload()
                        print("Audio playback complete")
                        time.sleep(3)
                        prompt = self.speakverif.stt(self.save_audio)
                        print(f"Prompt: {prompt}")
                        time.sleep(3)
                        response = chat_module.makeChat(usr_input=prompt, api_key=api, imagelike=filelike)
                        asyncio.run(self.tts.createTTS(self.remove_asterisk_phrases(response)))
                        
                        os.remove("myTTS/voiceline_pcm.wav")
                                    
                        if "bye" in response.lower() or "end session" in response.lower() or "session terminate" in response.lower():
                            chat_module.save_logs()
                            sys.exit(0)
                    else:
                        print(f"Score: {verify['score']}, Prediction: {verify['pred']}")
                except Exception as e:
                    print(f"Error occured: {e}")
                    pass
                    
        except KeyboardInterrupt:
            print("Stopping...")
            chat_module.save_logs()
            # stop_listening()  # Stop the background listener
            return


# Start the background recorder
# recorder = BackgroundAudioRecorder(silence_timeout=2)
# recorder.start_listening()
