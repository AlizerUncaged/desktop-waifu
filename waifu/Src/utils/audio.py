import pyaudio
import wave
import keyboard
import utils.hotkeys
import io, os, tempfile

CHUNK = 1024

FORMAT = pyaudio.paInt16

CHANNELS = 1

RATE = 44100

# For some reason this doesn't work.
# FILENAME = os.path.join(tempfile.gettempdir(), "recording.wav")
FILENAME = "recording.wav"

def record():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    while utils.hotkeys.audio_input():
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    p.terminate()

    # Because of OpenAI's library implementations we need
    # to save this as a .wav file in the local disk, we can't
    # pass the BufferedReader on ``openai.Audio.transcribe``.

    wf = wave.open(FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return FILENAME
    