import tortoise
import os

import tortoise.api as api
import tortoise.utils as utils

chardir = "voice/Character/"
char = "March"
lang = "jp"
charvoice = f"{char}_{lang}.wav"
ref_clips = ""
for voice in os.listdir(chardir):
    print(voice)
    if voice == charvoice:
        ref_clips = chardir + voice

ref_clips

# reference_clips = [utils.audio.load_audio(p, 22050) for p in chardir]
tts = api.TextToSpeech()
pcm_audio = tts.tts_with_preset("your text here", voice_samples=ref_clips, preset='fast')