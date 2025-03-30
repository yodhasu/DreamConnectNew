import time
from speechbrain.inference.speaker import SpeakerRecognition
from transformers import pipeline
import whisper
import soundfile as sf
import io
import numpy as np

class SpeakerVerification:
    def __init__(self, model_source="speechbrain/spkrec-ecapa-voxceleb", reference_audio_path=None):
        # Load pretrained model only once
        self.model = SpeakerRecognition.from_hparams(source=model_source, savedir="tmp_model")
        try:
            # self.sttmodel = pipeline("automatic-speech-recognition", model="openai/whisper-medium", device='cuda')
            self.whispermodel = whisper.load_model(name="medium", device="cuda", download_root="speechRecognition/model", in_memory=False)
            print("Model loaded on GPU")
        except:
            # self.sttmodel = pipeline("automatic-speech-recognition", model="openai/whisper-medium", device='cpu')
            self.whispermodel = whisper.load_model(name="medium", device="cpu", download_root="speechRecognition/model", in_memory=False)
            print("Model loaded on CPU")
        
        # Preload reference audio
        if reference_audio_path:
            # self.reference_signal, _ = torchaudio.load(reference_audio_path)
            self.reference_signal = reference_audio_path
        else:
            self.reference_signal = None

    def verify(self, input_audio_path):
        if self.reference_signal is None:
            raise ValueError("Reference audio not loaded. Provide a valid reference audio during initialization.")
        
        # Load input audio for verification
        input_signal = input_audio_path
        
        # Perform speaker verification
        try:
            score, prediction = self.model.verify_files(input_signal, self.reference_signal)
            print(f"Score: {score} ; Prediction: {prediction}")
            time.sleep(3)
            # return f"You with score {score}" if prediction == 1 else f"Not You with score {score}"
            return {'score': score, 'pred': prediction}
        except Exception as e:
            print(f"Error warning: {e}")
            pass

    def stt(self, input_audio_path):
        # resultstt = self.sttmodel(input_audio_path, return_timestamps=True)
        # return resultstt['text']
        print(f"Input Audio Path: {input_audio_path}")
        file_path = input_audio_path
        with open(file_path, "rb") as f:
            wav_bytes = f.read()

        # Convert bytes to NumPy array
        wav_io = io.BytesIO(wav_bytes)
        data, samplerate = sf.read(wav_io, dtype="float32")

        # Convert to Whisper format (16kHz required)
        import librosa
        audio_16k = librosa.resample(data, orig_sr=samplerate, target_sr=16000).astype(np.float32)
        time.sleep(3)
        print(f"Transcribing {audio_16k}...")
        try:
            resultstt = self.whispermodel.transcribe(
                audio=audio_16k,
                temperature=0,
                word_timestamps=True,
            )
            print(f"Transcription: {resultstt['text']}")
            time.sleep(3)
            return resultstt["text"]
            
        except Exception as e:
            print(f"Error warning: {e}")
            pass


# # Initialize the SpeakerVerification class with a reference audio file
# reference_audio_path = r"C:\Users\Axioo Pongo\OneDrive\Documents\Sound Recordings\reference_speaker.wav"  # Replace with the actual path to your reference audio
# verifier = SpeakerVerification(reference_audio_path=reference_audio_path)

# # Simulate multiple verification requests
# input_audio_path = r"C:\Users\Axioo Pongo\OneDrive\Documents\Sound Recordings\tes_speaker.wav"  # Replace with the actual path to your input audio
# result = verifier.verify(input_audio_path)
# print(f"Verification Result: {result}")
