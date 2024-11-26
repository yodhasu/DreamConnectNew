import torch
import TTS
import os
from TTS.api import TTS
import asyncio
import edge_tts
import re

# device = "cuda" if torch.cuda.is_available() else "cpu"

# chardir = "voiceCloner/voice/Character/"
# char = "March"
# lang = "en"
# charvoice = f"{char}_{lang}.wav"
# ref_clips = ""
# for voice in os.listdir(chardir):
#     print(voice)
#     if voice == charvoice:
#         ref_clips = chardir + voice

# ref_clips

# # List available 🐸TTS models
# mode_list = TTS().list_models()

# # download all model
# # for model in mode_list:
# #     TTS(model).to(device)

# # Init TTS
# tts = TTS("tts_models/it/mai_female/vits").to(device)

# # cloner tts
# model = "voice_conversion_models/multilingual/vctk/freevc24"
# text = "This is a text to test voice cloning capability of the current model"
# charvoice = "voice/Character/VO_JA_Archive_March_7th_1.wav"
# # cloner = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True).to(device)

# cloner = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True).to(device)
# cloner.tts_with_vc_to_file(text=text, speaker_wav = ref_clips, file_path= "voiceCloner/voice/Output/March1.wav")

# EDGE TTS
class TextToSpeech:
    def __init__(self, voice="en-US-JennyNeural"):
        """
        Initialize the TextToSpeech class with a default voice.
        :param voice: The neural voice to use for TTS.
        """
        self.voice = voice

    async def _text_to_speech(self, text, output_file):
        """
        Convert text to speech and save as an MP3 file.
        :param text: The text to convert to speech.
        :param output_file: Path to save the generated MP3 file.
        """
        tts = edge_tts.Communicate(text, self.voice)
        with open(output_file, "wb") as file:
            async for chunk in tts.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])

    def synthesize(self, text, output_file):
        """
        Public method to synthesize speech from text.
        :param text: The text to convert to speech.
        :param output_file: Path to save the generated MP3 file.
        """
        asyncio.run(self._text_to_speech(text, output_file))

    def clean_text(self, input_text):
        """
        Removes text inside asterisks, the asterisks themselves, and unwanted characters or symbols.
        
        Args:
            input_text (str): The text to clean.
        
        Returns:
            str: The cleaned text.
        """
        # Remove text inside asterisks and the asterisks themselves
        no_asterisks = re.sub(r'\*.*?\*', '', input_text)

        # Remove unwanted symbols (non-alphanumeric except spaces)
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,!?\'\";:()-]', '', no_asterisks)

        # Remove extra whitespace
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        return cleaned_text