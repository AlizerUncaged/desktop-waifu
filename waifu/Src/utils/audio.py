import pyaudio
import wave
import keyboard
from pydub import AudioSegment
import utils.hotkeys
import io, os, tempfile, audioop

CHUNK = 1024

FORMAT = pyaudio.paInt16

CHANNELS = 1

RATE = 44100

# For some reason this doesn't work.
# FILENAME = os.path.join(tempfile.gettempdir(), "recording.wav")
FILENAME = "recording.wav"

def play_mp3(path, audio_level_callback = None):
    audio_file = AudioSegment.from_file(path, format="mp3")
    play_mp3_memory(audio_file, audio_level_callback)

# Plays an MP3 file from memory
def play_mp3_memory(audio_file, audio_level_callback = None):
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream to play the audio
    stream = p.open(format=pyaudio.paInt16,
                    channels=audio_file.channels,
                    rate=audio_file.frame_rate,
                    output=True)

    # Read the audio data in chunks and play it
    chunk_size = 1024
    data = audio_file.raw_data
    while data:
        chunk = data[:chunk_size]
        stream.write(chunk)
        data = data[chunk_size:]
        if audio_level_callback is not None:
            volume = audioop.rms(chunk, 2)
            normalized_volume = (volume / 32767) * 100
            audio_level_callback(normalized_volume / 14)

    stream.stop_stream()
    stream.close()
    p.terminate()


def play_wav_memory(audio_file, audio_level_callback = None):
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


# Plays wav file
def play_wav(path, audio_level_callback = None):
    audio_file = wave.open(path)
    play_wav_memory(audio_file, audio_level_callback)

    

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
    