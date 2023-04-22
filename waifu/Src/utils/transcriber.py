import utils.audio
import utils.vtube_studio

import openai, requests, urllib, os, wave, io

VOICEVOX_URL = os.environ.get("VOICEVOX_URL")

VOICEVOX_LOCAL_FILE = "test.wav"
def transcribe(filename):
    audio = open(filename, "rb")

    transcript = openai.Audio.transcribe("whisper-1", audio)

    message = transcript.text

    if message is None or len(message.strip()) == 0:
        return None
    
    return message

def speak_jp(text, speaker=46):
    global VOICEVOX_URL, VOICEVOX_LOCAL_FILE
    params_encoded = urllib.parse.urlencode({'text': text, 'speaker': speaker})
    request = requests.post(f'{VOICEVOX_URL}/audio_query?{params_encoded}')
    params_encoded = urllib.parse.urlencode({'speaker': 46, 'enable_interrogative_upspeak': True})
    request = requests.post(f'{VOICEVOX_URL}/synthesis?{params_encoded}', json=request.json())
    with io.BytesIO(request.content) as memfile:
        utils.audio.play(memfile, utils.vtube_studio.set_audio_level)
    