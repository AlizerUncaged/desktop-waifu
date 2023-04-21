from colorama import *
import openai, humanize, os, sys, time, threading, asyncio
from rich.console import Console

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

import utils.audio
import utils.hotkeys
import utils.transcriber
import utils.voicevox
import utils.dependencies
import utils.characterAi
import utils.vtube_studio
import utils.speech
from rich.markdown import Markdown

utils.speech.prepare()
utils.characterAi.run_async()
utils.dependencies.start_check()
utils.voicevox.run_async()
utils.speech.silero_tts("hello", "en", "v3_en", "en_21")

if bool(os.environ.get("VTUBE_STUDIO_ENABLED", "False")):
    utils.vtube_studio.run_async()

print(Fore.RESET + Style.BRIGHT + "Welcome back, to speak press " + 
      (", ".join([Fore.YELLOW + x + Fore.RESET for x in utils.hotkeys.KEYS]) + " at the same time." if len(utils.hotkeys.KEYS) > 1 else utils.hotkeys.KEYS[0]))

semaphore = threading.Semaphore(0)

console = Console()


# We need to wait for this to end until the next
# input.
def character_replied(message):
    print(f"\r{Style.RESET_ALL + Style.BRIGHT + Fore.YELLOW}Character {Fore.RESET + Style.RESET_ALL}> ", end="")
    console.print(Markdown(message))

    audio_path = utils.speech.silero_tts(message)

    utils.audio.play(audio_path, utils.vtube_studio.set_audio_level)

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