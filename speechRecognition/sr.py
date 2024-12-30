import torchaudio
from speechbrain.pretrained import SpeakerRecognition

class SpeakerVerification:
    def __init__(self, model_source="speechbrain/spkrec-ecapa-voxceleb", reference_audio_path=None):
        # Load pretrained model only once
        self.model = SpeakerRecognition.from_hparams(source=model_source, savedir="tmp_model")
        
        # Preload reference audio
        if reference_audio_path:
            self.reference_signal, _ = torchaudio.load(reference_audio_path)
        else:
            self.reference_signal = None

    def verify(self, input_audio_path):
        if self.reference_signal is None:
            raise ValueError("Reference audio not loaded. Provide a valid reference audio during initialization.")
        
        # Load input audio for verification
        input_signal, _ = torchaudio.load(input_audio_path)
        
        # Perform speaker verification
        score = self.model.verify_batch(input_signal, self.reference_signal)
        return "You" if score > 0.5 else "Not You"


# Initialize the SpeakerVerification class with a reference audio file
reference_audio_path = "reference_audio.wav"  # Replace with the actual path to your reference audio
verifier = SpeakerVerification(reference_audio_path=reference_audio_path)

# Simulate multiple verification requests
input_audio_path = "user_input.wav"  # Replace with the actual path to your input audio
result = verifier.verify(input_audio_path)
print(f"Verification Result: {result}")
