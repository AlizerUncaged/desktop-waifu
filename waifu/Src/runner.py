from colorama import *
import openai, humanize, os, sys, time, threading, asyncio, signal, json
from rich.console import Console

# If user didn't rename example.env
if os.path.exists("example.env") and not os.path.exists(".env"):
    os.rename("example.env", ".env")

# Load settings from .env file
with open('.env') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, value = line.split('=', 1)
        os.environ[key] = value


# Set OpenAPI Key
if os.environ.get("OPENAI_KEY") is None:
    print(Fore.RED + Style.BRIGHT + "You didn't provide an OpenAI API Key!" + Style.RESET_ALL + " Things will not work.")
else:
    openai.api_key = os.environ.get("OPENAI_KEY")

# Check virtual env
print(Style.BRIGHT + Fore.GREEN)
if os.environ.get('VIRTUAL_ENV'):
    # The VIRTUAL_ENV environment variable is set
    print('You are in a virtual environment:', os.environ['VIRTUAL_ENV'])
elif sys.base_prefix != sys.prefix:
    # sys.base_prefix and sys.prefix are different
    print('You are in a virtual environment:', sys.prefix)
else:
    # Not in a virtual environment
    print(Fore.RED + 'You are not in a virtual environment, we\'ll continue anyways')

print(Style.RESET_ALL)

def signal_handler(sig, frame):
    print('Exiting...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

import utils.dependencies # Checks variables
import utils.audio
import utils.hotkeys
import utils.transcriber
import utils.characterAi
import utils.vtube_studio
import utils.translator
import utils.speech
import utils.punctuation_fixer

voice = os.environ.get("VOICE") 

utils.dependencies.start_check(voice)

if voice == "elevenlabs":
    import utils.elevenlabs
elif voice == "voicevox":
    import utils.voicevox
    utils.voicevox.run_async()

from rich.markdown import Markdown

utils.speech.prepare()
utils.characterAi.run_async()
utils.speech.silero_tts("hello", "en", "v3_en", "en_21")

# wtf
if json.loads(os.environ.get("VTUBE_STUDIO_ENABLED", "False").lower()):
    utils.vtube_studio.run_async()

print(Fore.RESET + Style.BRIGHT + "Welcome back, to speak press " + 
      (", ".join([Fore.YELLOW + x + Fore.RESET for x in utils.hotkeys.KEYS]) + " at the same time." if len(utils.hotkeys.KEYS) > 1 else utils.hotkeys.KEYS[0]))

semaphore = threading.Semaphore(0)

console = Console()


# We need to wait for this to end until the next
# input.
def character_replied(raw_message):
    print(f"{Style.DIM}raw message: {raw_message}")
    print(f"\r{Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW}Character {Fore.RESET + Style.RESET_ALL}> ", end="")
    
    # fix
    voice_message = utils.punctuation_fixer.fix_stops(raw_message)

    # Sometimes causes issues.
    console.print(Markdown(raw_message))

    # print(raw_message)

    if voice == "elevenlabs":
        utils.elevenlabs.speak(voice_message)
    elif voice == "voicevox":
        if json.loads(os.environ.get("TRANSLATE_TO_JP", "False").lower()):
            message_jp = utils.translator.translate_to_jp(voice_message)
            print(f"{Style.NORMAL + Fore.RED}jp translation {Style.RESET_ALL}> {message_jp}")
            if json.loads(os.environ.get("TTS_JP", "False").lower()):
                utils.transcriber.speak_jp(message_jp)

        if json.loads(os.environ.get("TTS_EN", "False").lower()):
            audio_path = utils.speech.silero_tts(voice_message)
            utils.audio.play_wav(audio_path, utils.vtube_studio.set_audio_level)

    # Set mouth to resting point
    utils.vtube_studio.set_audio_level(0)

    semaphore.release()

utils.characterAi.reply_callback = character_replied
# Main process loop
while True: 

    print(Style.RESET_ALL + Fore.RESET, end="")

    print("You" + Fore.GREEN + Style.BRIGHT + " (mic) " + Fore.RESET + ">", end="", flush=True)

    # Wait for audio input
    utils.hotkeys.audio_input_await()

    print("\rYou" + Fore.GREEN + Style.BRIGHT + " (mic " + Fore.YELLOW + "[Recording]" + Fore.GREEN +") " + Fore.RESET + ">", end="", flush=True)

    audio_buffer = utils.audio.record()

    # We need to keep track of the length of this message
    # because in Python we have no way to clear an entire line, wtf.
    try:
        tanscribing_log = "\rYou" + Fore.GREEN + Style.BRIGHT + " (mic " + Fore.BLUE + "[Transcribing (" + str(humanize.naturalsize(os.path.getsize(audio_buffer))) + ")]" + Fore.GREEN +") " + Fore.RESET + "> "
        print(tanscribing_log, end="", flush=True)
        transcript = utils.transcriber.transcribe(audio_buffer)
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "Error: " + str(e))
        continue


    # Clear the last line.
    print('\r' + ' ' * len(tanscribing_log), end="")
    print("\rYou" + Fore.GREEN + Style.BRIGHT + " (mic) " + Fore.RESET + "> ", end="", flush=True)

    print(f"{transcript.strip()}")    

    utils.characterAi.send_message_to_process_via_websocket(transcript)
    semaphore.acquire()

    # After use delete recording.
    try:
        # This causes ``[WinError 32] The process cannot access the file because it is being used by another process`` sometimes.
        # I don't know why.
        os.remove(audio_buffer)
    except:
        pass