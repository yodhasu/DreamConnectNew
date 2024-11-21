import os
from elevenlabs import ElevenLabs, voices, save, play
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

# add timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

class ElevenLabsTTS:
    def __init__(self, api_key=None):
        """
        Initializes the ElevenLabs TTS system with the provided API key.

        Args:
            api_key (str, optional): Your ElevenLabs API key. If not provided,
                                      it will load from environment variables.
        """
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            raise ValueError("API key is missing. Please provide it through the environment variable ELEVENLABS_API_KEY.")
        
        # Initialize ElevenLabs client
        self.client = ElevenLabs(api_key=self.api_key)

        # Call voices to instantiate the client properly (required by ElevenLabs API)
        self.all_voices = self.client.voices.get_all()
        print(f"\nAll ElevenLabs voices: \n{self.all_voices.voices}\n")

    def get_all_voices(self):
        """Returns a list of all available voices."""
        return self.all_voices.voices

    def text_to_audio(self, input_text, voice="March 7th", model="eleven_multilingual_v2", save_as_wave=True, subdirectory="voiceCloner/voice/Output/"):
        """
        Converts text to audio and saves it to a file.

        Args:
            input_text (str): Text to convert to speech.
            voice (str): The voice model to use for the speech (default "March 7th").
            model (str): The model to use for the TTS conversion.
            save_as_wave (bool): Whether to save the file as `.wav` (default True).
            subdirectory (str): Directory where the audio file should be saved.

        Returns:
            str: Path to the saved audio file.
        """
        # Generate audio from text
        audio_saved = self.client.generate(
            text=input_text,
            voice=voice,
            model=model
        )

        # Determine file extension and name
        file_extension = "mp3"
        file_name = f"March.{file_extension}"
        tts_file = os.path.join(os.path.abspath(os.curdir), subdirectory, file_name)

        # Save the generated audio to the specified path
        save(audio_saved, tts_file)
        print(f"Audio saved to: {tts_file}")

        return file_name

    def text_to_audio_played(self, input_text, voice="March 7th", model="eleven_turbo_v2_5"):
        """
        Converts text to audio and plays it out loud.

        Args:
            input_text (str): Text to convert to speech.
            voice (str): The voice model to use for the speech (default "March 7th").
            model (str): The model to use for the TTS conversion.
        """
        # Generate audio from text
        audio = self.client.generate(
            text=input_text,
            voice=voice,
            model=model
        )

        # Play the generated audio
        play(audio)
        print("Playing the generated audio...")

