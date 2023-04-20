import os, humanize, requests, py7zr
from colorama import *

VOICEVOX_DIR = "voicevox"

NODE = "node"

CHARACTERAI_PORT = 40102

TEMP_FILE = "voicevox.tmp"

VOICEVOX_DIRECT_LINK = "https://github.com/VOICEVOX/voicevox_engine/releases/download/0.14.4/voicevox_engine-windows-nvidia-0.14.4.7z.001"

HARDCODED_VOICEVOX_ARCHIVE_ROOT_FOLDER = "windows-nvidia"

# Checks if voicevox is intalled, if not, download and extract it.
def start_check():
    if not os.path.isdir(VOICEVOX_DIR):

        print(Fore.YELLOW + "Installing voicevox..." + Fore.RESET, end="", flush=True)

        response = requests.get(VOICEVOX_DIRECT_LINK, stream=True)

        total_size = int(response.headers.get('content-length', 0))

        block_size = 1024 * 8
        print(Fore.BLUE + "(" + humanize.naturalsize(total_size) + ") ", end="")
        if os.path.exists(TEMP_FILE) and os.path.getsize(TEMP_FILE) == total_size:
            print("Already exists!")
        else:
            print()
            with open(TEMP_FILE, 'wb') as file:
                downloaded = 0
                for data in response.iter_content(block_size):
                    file.write(data)
                    downloaded += len(data)
                    percent = downloaded * 100 / total_size
                    print(Fore.RESET + f"Downloaded {Fore.BLUE}{humanize.naturalsize(downloaded)}/{humanize.naturalsize(total_size)}{Fore.YELLOW} ({percent:.2f}%){Fore.RESET}   ", end='\r')
        
        print(Fore.YELLOW + "Unzipping..." + Fore.RESET, end="", flush=True)
        with py7zr.SevenZipFile(TEMP_FILE, 'r') as archive:
            archive.extractall(path="./")
            
        # Clean
        os.rename(HARDCODED_VOICEVOX_ARCHIVE_ROOT_FOLDER, VOICEVOX_DIR)
        os.remove(TEMP_FILE)