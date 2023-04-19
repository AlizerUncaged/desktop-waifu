import os
import sys
from colorama import *
import openai, humanize

# Load settings from .env file
with open('.env') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        key, value = line.split('=', 1)
        os.environ[key] = value


# Set OpenAPI Key
if os.environ.get("KEY") is None:
    print(Fore.RED + Style.BRIGHT + "You didn't provide an OpenAI API Key!" + Style.RESET_ALL + " Things will not work.")
else:
    openai.api_key = os.environ.get("KEY")

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

utils.dependencies.start_check()
utils.voicevox.run_async()

# Main process loop
while True: 
    print(Style.RESET_ALL)
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

    print(transcript)