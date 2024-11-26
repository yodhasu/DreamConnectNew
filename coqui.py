from TTS.api import TTS
import torch
import torch
import os
import gc
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
device = "cuda" if torch.cuda.is_available() else "cpu"
# print(device)
# gc.collect()
torch.cuda.empty_cache()
# print(TTS().list_models())
# with torch.cuda.device(0):
model = TTS("tts_models/multilingual/multi-dataset/xtts_v1.1").to(device=device)
model.tts_to_file(text="Hello World", speaker_wav="reinevoice.wav", file_path="output.wav", split_sentences=True, language="en")
torch.cuda.empty_cache()
gc.collect()