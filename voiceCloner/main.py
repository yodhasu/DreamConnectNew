import torch
import TTS
import os
from TTS.api import TTS

device = "cuda" if torch.cuda.is_available() else "cpu"

chardir = "voice/Character/"
char = "March"
lang = "en"
charvoice = f"{char}_{lang}.wav"
ref_clips = ""
for voice in os.listdir(chardir):
    print(voice)
    if voice == charvoice:
        ref_clips = chardir + voice

ref_clips

# List available 🐸TTS models
mode_list = TTS().list_models()

# download all model
# for model in mode_list:
#     TTS(model).to(device)

# Init TTS
tts = TTS("tts_models/it/mai_female/vits").to(device)

# cloner tts
model = "voice_conversion_models/multilingual/vctk/freevc24"
text = "This is a text to test voice cloning capability of the current model"
charvoice = "voice/Character/VO_JA_Archive_March_7th_1.wav"
# cloner = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True).to(device)

cloner = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True).to(device)
cloner.tts_with_vc_to_file(text=text, speaker_wav = ref_clips, file_path= "voice/Output/March1.wav")