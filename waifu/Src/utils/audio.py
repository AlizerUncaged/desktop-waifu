import pyaudio
import wave
import keyboard
import utils.hotkeys
import io, os, tempfile, audioop

CHUNK = 1024

FORMAT = pyaudio.paInt16

CHANNELS = 1

RATE = 44100

# For some reason this doesn't work.
# FILENAME = os.path.join(tempfile.gettempdir(), "recording.wav")
FILENAME = "recording.wav"



# Plays wav file
def play(path, audio_level_callback = None):
    audio_file = wave.open(path, "rb")

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream to play the audio
    stream = p.open(format=p.get_format_from_width(audio_file.getsampwidth()),
                    channels=audio_file.getnchannels(),
                    rate=audio_file.getframerate(),
                    output=True)

    # Read the audio data in chunks and play it
    chunk_size = 1024
    data = audio_file.readframes(chunk_size)
    while data:
        stream.write(data)
        data = audio_file.readframes(chunk_size)
        if audio_level_callback is not None:
            volume = audioop.rms(data, 2)
            audio_level_callback(volume / 10000)

    stream.stop_stream()
    stream.close()
    p.terminate()

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
    