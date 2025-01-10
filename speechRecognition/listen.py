import speech_recognition as sr
import asyncio
import time
from io import BytesIO
from speechRecognition.sr import SpeakerVerification
from myTTS.simpletts import SimpleTTS
from chatbot.context_logger import ContextLogger
import os
import wave
import re

class BackgroundAudioRecorder:
    def __init__(self, silence_timeout=2):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.silence_timeout = silence_timeout  # Time to wait before saving
        self.buffer = BytesIO()  # Store audio in memory before saving
        self.last_sound_time = None
        self.speakverif = SpeakerVerification(reference_audio_path=r"C:\Users\Axioo Pongo\OneDrive\Documents\Sound Recordings\reference_speaker.wav")
        self.save_audio = "speechRecognition/recorded.mp3"
        self.tts = SimpleTTS()
        self.context = ContextLogger()
        
    def remove_asterisk_phrases(self, text):
        # Regular expression to match text between two asterisks
        return re.sub(r"\*\*(.*?)\*\*", "", text)
    
    def save_audio_to_file(self):
        """
        Save buffered audio data to a WAV file.
        """
        with open(self.save_audio, 'wb') as f:
            f.write(self.buffer.getvalue())


    # def process_audio(self, recognizer, audio):
    #     try:
    #         # Reset the buffer if new audio is detected
    #         self.last_sound_time = time.time()
    #         self.buffer.write(audio.get_wav_data())
    #     except Exception as e:
    #         print(f"Error processing audio: {e}")

    def start_listening(self, chat_module, api, filelike):
        
        """
        Start listening and process audio, saving it after silence timeout.
        """
        print("Adjusting for ambient noise, please wait...")
        chat_module.retrieve_memory()
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening for audio...")

        self.last_sound_time = time.time()
        try:
            while True:
                if len(self.context.get_context_log()) == 15:
                    chat_module.retrieve_memory()
                # current_time = time.time()
                # if (
                #     self.last_sound_time
                #     and (current_time - self.last_sound_time > self.silence_timeout)
                #     and self.buffer.getvalue()
                # ):
                with sr.Microphone() as sc:
                    # Listen for audio input
                    audio = self.recognizer.listen(sc)

                    # Check for silence
                    current_time = time.time()
                    self.buffer.write(audio.get_wav_data())  # Buffer audio data
                    
                    if current_time - self.last_sound_time > self.silence_timeout:
                        print("Silence detected. Saving audio...")
                        self.save_audio_to_file()
                        self.buffer = BytesIO()  # Reset the buffer for new recordings
                        self.last_sound_time = current_time
                    
                        myspeaker = self.speakverif.verify(self.save_audio)
                        try:
                            if myspeaker['pred'] and myspeaker['score'] > 0.3:
                                # print(score)
                                prompt = self.speakverif.stt(self.save_audio)
                                response = chat_module.makeChat(usr_input=self.remove_asterisk_phrases(prompt), api_key=api, imagelike=filelike)
                                asyncio.run(self.tts.createTTS(response))
                                os.remove("myTTS/voiceline_pcm.wav")
                                
                                if "bye" in response.lower() or "end session" in response.lower() or "session terminate" in response.lower():
                                    chat_module.save_logs()
                                    return
                            else:
                                print(f"Score: {myspeaker['score']}, Prediction: {myspeaker['pred']}")
                        except Exception as e:
                            print(e)
                            pass
                    else:
                        self.last_sound_time = current_time  # Reset the timer if sound is detected
                time.sleep(0.1)
                print('No sound detected')
        except KeyboardInterrupt:
            print("Stopping...")
            chat_module.save_logs()
            # stop_listening()  # Stop the background listener
            return


# Start the background recorder
# recorder = BackgroundAudioRecorder(silence_timeout=2)
# recorder.start_listening()
