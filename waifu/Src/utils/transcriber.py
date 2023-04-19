import openai

def transcribe(filename):
    audio = open(filename, "rb")

    transcript = openai.Audio.transcribe("whisper-1", audio)

    message = transcript.text

    if message is None or len(message.strip()) == 0:
        return None
    
    return message