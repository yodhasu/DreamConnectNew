import asyncio
from io import BytesIO
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
        self.tts = SimpleTTS()
        self.context = ContextLogger()
        
    def remove_asterisk_phrases(self, text):
        # Regular expression to match text between two asterisks
        return re.sub(r"\*\*(.*?)\*\*", "", text)


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
                    if verify['score'] > 0.3 and verify['pred']:
                        prompt = self.speakverif.stt(self.save_audio)
                        response = chat_module.makeChat(usr_input=prompt, api_key=api, imagelike=filelike)
                        asyncio.run(self.tts.createTTS(self.remove_asterisk_phrases(response)))
                        
                        os.remove("myTTS/voiceline_pcm.wav")
                                    
                        if "bye" in response.lower() or "end session" in response.lower() or "session terminate" in response.lower():
                            chat_module.save_logs()
                            return
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
