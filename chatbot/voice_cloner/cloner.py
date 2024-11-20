import os
import torch
from TTS.api import TTS
import re

class VoiceCloner:
    def __init__(self, character_dir="voiceCloner/voice/Character/", device=None):
        """
        Initialize the Voice Cloner library.
        
        Args:
            character_dir (str): Path to the directory containing character voice files.
            device (str): Device to run the model on ('cuda' or 'cpu'). If not specified, auto-detects.
        """
        self.character_dir = character_dir
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tts_model = None
        self.cloner_model = None

    def get_character_voice_path(self, character_name, language="en"):
        """
        Retrieve the path to the specified character's voice file.

        Args:
            character_name (str): The name of the character.
            language (str): The language code for the character's voice file.

        Returns:
            str: Path to the voice file, or an empty string if not found.
        """
        voice_file_name = f"{character_name}_{language}.wav"
        for voice_file in os.listdir(self.character_dir):
            if voice_file == voice_file_name:
                return os.path.join(self.character_dir, voice_file)
        return ""

    def initialize_tts(self, tts_model="tts_models/en/ljspeech/tacotron2-DDC"):
        """
        Initialize the TTS model.

        Args:
            tts_model (str): Model name or path.
        """
        self.tts_model = TTS(tts_model).to(self.device)

    def initialize_cloner(self, cloner_model="tts_models/en/ljspeech/tacotron2-DDC"):
        """
        Initialize the voice cloner model.

        Args:
            cloner_model (str): Model name or path for voice cloning.
        """
        self.cloner_model = TTS(cloner_model, progress_bar=True).to(self.device)

    def clone_voice(self, text, character_name, output_path, language="en"):
        """
        Generate a cloned voice file.

        Args:
            text (str): The text to be synthesized.
            character_name (str): The name of the character to clone.
            output_path (str): Path to save the generated audio.
            language (str): Language of the character's voice file.
        """
        # Get the reference voice file
        ref_voice_path = self.get_character_voice_path(character_name, language)
        if not ref_voice_path:
            raise FileNotFoundError(f"Voice file for character '{character_name}' not found.")

        # Ensure the cloner model is initialized
        if not self.cloner_model:
            raise RuntimeError("Cloner model is not initialized. Call `initialize_cloner()` first.")

        # Clone the voice
        self.cloner_model.tts_with_vc_to_file(
            text=text,
            speaker_wav=ref_voice_path,
            file_path=output_path,
        )

    @staticmethod
    def sanitize_text(text):
        """
        Remove unsupported characters from the input text.
        Args:
            text (str): The text to sanitize.
        Returns:
            str: Cleaned text.
        """
        # Replace smart quotes and other non-ASCII characters
        text = text.replace("’", "'").replace("“", '"').replace("”", '"')
        # Remove any remaining unsupported characters
        text = re.sub(r'[^\x00-\x7F]+', '', text)  # Keep only ASCII characters
        text = re.sub(r"\*.*?\*", "", text) # Remove text between asterisks
        result = " ".join(text.split())
        return result
    
    @staticmethod
    def list_available_models():
        """
        List all available TTS models.
        """
        return TTS().list_models()
