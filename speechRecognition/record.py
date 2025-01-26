import wave
import numpy as np
import pyaudio

class BackgroundAudioRecorder:
    def __init__(self, silence_timeout=2):
        self.silence_timeout = silence_timeout  # Time to wait before saving
        self.last_sound_time = None
        # self.speakverif = SpeakerVerification(reference_audio_path=r"C:\Users\Axioo Pongo\OneDrive\Documents\Sound Recordings\reference_speaker.wav")
        self.save_audio = "speechRecognition/recorded.wav"
        # self.tts = SimpleTTS()
        # self.context = ContextLogger()
        
    def is_silence(self, audio_chunk, silence_thresh, energy_thresh=750):
        # Convert the audio chunk to a NumPy array of 16-bit integers
        audio_chunk = np.frombuffer(audio_chunk, dtype=np.int16)
        print(f"Audio Chunk: {audio_chunk}")

        # Calculate the energy of the audio chunk
        energy = np.sum(audio_chunk.astype(np.float32)) / float(len(audio_chunk))
        print(f"Energy: {energy} ; Energy Threshold: {energy_thresh} ; Max: {np.max(audio_chunk)}")

        # Check if both energy and maximum absolute value are below thresholds
        return energy < energy_thresh and np.max(audio_chunk) < silence_thresh

    def record_audio(self, max_silence_duration=10000, sample_rate=16000, chunk_size=1024, silence_thresh=750):
        started = 0
        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Open a stream for recording audio
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

        # Initialize variables for storing audio frames and counting consecutive silence
        frames = []
        consecutive_silence_counter = 0

        print("Recording...")

        while True:
            # Read a chunk of audio data from the stream
            print("reading chunk")
            data = stream.read(chunk_size)
            frames.append(data)

            # Convert the audio chunk to a NumPy array
            audio_chunk = np.frombuffer(data, dtype=np.int16)

            # Check if the audio chunk is silence
            if self.is_silence(audio_chunk, silence_thresh=silence_thresh):
                consecutive_silence_counter += 1
                print("silence count:", consecutive_silence_counter)
                print("Chunk size:", chunk_size)
            else:
                consecutive_silence_counter = 0
                started = 1
                print("silence count:", consecutive_silence_counter)
                print("Chunk size:", chunk_size)

            # Break the loop if consecutive silence reaches the specified duration
            if consecutive_silence_counter >= (max_silence_duration // chunk_size) and started == 1:
                break
            # time.sleep(1)

        print("Recording finished.")

        # Stop and close the audio stream, and terminate PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Write the recorded frames to a WAV file
        with wave.open(self.save_audio, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

# if __name__ == "__main__":
#     # Path to the Vosk model
#     model_path = "path/to/vosk-model-en-us-0.22-lgraph"
    
#     # Path to the output audio file
#     output_file_path = "path to audio file"
    
#     bgrec = BackgroundAudioRecorder()
    
#     # Record audio and save it to the specified output file
#     audio_data = bgrec.record_audio()