from rvc_python.infer import RVCInference
from chatbot.voiceCloner import edgexrvc

rvc = RVCInference(device="cuda")
# rvc.f0up_key = 3 parameter for reine
tts = edgexrvc.TextToSpeech(voice="ja-JP-NanamiNeural")
tts.synthesize("今日の写真の整理が終わったから、ウチはもう寝るね。アンタもゲームで夜更かししないように！", "testoutput.wav")
rvc.load_model("march7th/model.pth", index_path="march7th/model.index")
rvc.infer_file(input_path="testoutput.wav", output_path="outputmarch.wav")