import torchaudio
import speechbrain
from speechbrain.inference.speaker import SpeakerRecognition
from transformers import pipeline

class SpeakerVerification:
    def __init__(self, model_source="speechbrain/spkrec-ecapa-voxceleb", reference_audio_path=None):
        # Load pretrained model only once
        self.model = SpeakerRecognition.from_hparams(source=model_source, savedir="tmp_model")
        self.sttmodel = pipeline("automatic-speech-recognition", model="openai/whisper-small")
        
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
        score, prediction = self.model.verify_files(input_signal, self.reference_signal)
        # return f"You with score {score}" if prediction == 1 else f"Not You with score {score}"
        return prediction

    def stt(self, input_audio_path):
        resultstt = self.sttmodel(input_audio_path, return_timestamps=True)
        return resultstt['text']


# # Initialize the SpeakerVerification class with a reference audio file
# reference_audio_path = r"C:\Users\Axioo Pongo\OneDrive\Documents\Sound Recordings\reference_speaker.wav"  # Replace with the actual path to your reference audio
# verifier = SpeakerVerification(reference_audio_path=reference_audio_path)

# # Simulate multiple verification requests
# input_audio_path = r"C:\Users\Axioo Pongo\OneDrive\Documents\Sound Recordings\tes_speaker.wav"  # Replace with the actual path to your input audio
# result = verifier.verify(input_audio_path)
# print(f"Verification Result: {result}")
