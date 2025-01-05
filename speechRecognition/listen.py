import speech_recognition as sr
import asyncio
import time
from io import BytesIO
from speechRecognition.sr import SpeakerVerification
from myTTS.simpletts import SimpleTTS
from chatbot.context_logger import ContextLogger
import os

class BackgroundAudioRecorder:
    def __init__(self, silence_timeout=2):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.silence_timeout = silence_timeout  # Time to wait before saving
        self.buffer = BytesIO()  # Store audio in memory before saving
        self.last_sound_time = None
        self.speakverif = SpeakerVerification(reference_audio_path=r"C:\Users\Axioo Pongo\OneDrive\Documents\Sound Recordings\reference_speaker.wav")
        self.save_audio = "speechRecognition/recorded.wav"
        self.tts = SimpleTTS()
        self.context = ContextLogger()

    def save_audio_to_file(self):
        # Write buffered audio data to a WAV file
        filename = self.save_audio
        with open(filename, "wb") as f:
            f.write(self.buffer.getvalue())
        print(f"Audio saved to {filename}")
        self.buffer = BytesIO()  # Clear the buffer

    def process_audio(self, recognizer, audio):
        try:
            # Reset the buffer if new audio is detected
            self.last_sound_time = time.time()
            self.buffer.write(audio.get_wav_data())
        except Exception as e:
            print(f"Error processing audio: {e}")

    def start_listening(self, chat_module, api, filelike):
        print("Adjusting for ambient noise, please wait...")
        chat_module.retrieve_memory()
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust noise threshold
            print("Listening for audio...")
        
        # Start background listening
        stop_listening = self.recognizer.listen_in_background(
            self.microphone, self.process_audio
        )

        # Monitor silence timeout in the background
        try:
            
            while True:
                if len(self.context.get_context_log()) == 15:
                    chat_module.retrieve_memory()
                current_time = time.time()
                if (
                    self.last_sound_time
                    and (current_time - self.last_sound_time > self.silence_timeout)
                    and self.buffer.getvalue()
                ):
                    print("Silence detected. Saving audio...")
                    self.save_audio_to_file()
                    self.last_sound_time = None
                    checkspeaker = self.speakverif.verify(self.save_audio)
                    if checkspeaker:
                        # print(score)
                        prompt = self.speakverif.stt(self.save_audio)
                        response = chat_module.makeChat(usr_input=prompt, api_key=api, imagelike=filelike)
                        asyncio.run(self.tts.createTTS(response))
                        os.remove("myTTS/voiceline_pcm.wav")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Stopping...")
            stop_listening()  # Stop the background listener
                


# Start the background recorder
# recorder = BackgroundAudioRecorder(silence_timeout=2)
# recorder.start_listening()
