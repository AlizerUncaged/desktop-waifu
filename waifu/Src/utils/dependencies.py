import os, humanize, requests, py7zr, zipfile
from colorama import *

VOICEVOX_DIR = "voicevox"

NODE = "node"

CHARACTERAI_PORT = 40102

TEMP_FILE = "voicevox.tmp"

FFMPEG_DIRECT_LINK = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
VOICEVOX_DIRECT_LINK = "https://github.com/VOICEVOX/voicevox_engine/releases/download/0.14.4/voicevox_engine-windows-nvidia-0.14.4.7z.001"

HARDCODED_VOICEVOX_ARCHIVE_ROOT_FOLDER = "windows-nvidia"
VOICE = os.environ.get("VOICE") 

def donwload(url, temp):
    response = requests.get(url, stream=True)

    total_size = int(response.headers.get('content-length', 0))

    block_size = 1024 * 8
    print(Fore.BLUE + "(" + humanize.naturalsize(total_size) + ") ", end="")
    if os.path.exists(temp) and os.path.getsize(temp) == total_size:
        print("Already exists!")
    else:
        print()
        with open(temp, 'wb') as file:
            downloaded = 0
            for data in response.iter_content(block_size):
                file.write(data)
                downloaded += len(data)
                percent = downloaded * 100 / total_size
                print(Fore.RESET + f"Downloaded {Fore.BLUE}{humanize.naturalsize(downloaded)}/{humanize.naturalsize(total_size)}{Fore.YELLOW} ({percent:.2f}%){Fore.RESET}   ", end='\r')
    
    print(Fore.YELLOW + "Unzipping..." + Fore.RESET, end="", flush=True)

# Checks if voicevox is intalled, if not, download and extract it.
def start_check(voice):
    if not os.path.isdir(VOICEVOX_DIR) and voice == "voicevox":

        print(Fore.YELLOW + "Installing voicevox..." + Fore.RESET, end="", flush=True)

        donwload(VOICEVOX_DIRECT_LINK, TEMP_FILE)
            
        with py7zr.SevenZipFile(TEMP_FILE, 'r') as archive:
            archive.extractall(path="./")
            
        # Clean
        os.rename(HARDCODED_VOICEVOX_ARCHIVE_ROOT_FOLDER, VOICEVOX_DIR)
        os.remove(TEMP_FILE)

    elif voice == "elevenlabs":
        ffmpeg_required = ["ffmpeg.exe", "ffprobe.exe"]
        for i in ffmpeg_required:
            if not os.path.exists(i):
                # Donwload ffmpeg for pyaudio mp3
                donwload(FFMPEG_DIRECT_LINK, TEMP_FILE)
                
                with zipfile.ZipFile(TEMP_FILE) as archive, open(i, "wb") as f:
                    f.write(archive.read(f"ffmpeg-master-latest-win64-gpl/bin/{i}"))


required_variables = ["CHARACTERAI_CHARACTER", "OPENAI_KEY", "TORCH_DEVICE", "VOICE"]

# Check variables
for i in required_variables:
    if not os.environ.get(i) or not os.environ.get(i).strip():
        print(f"Please set the required variable {Fore.YELLOW + Style.BRIGHT}{i}{Style.RESET_ALL} or provide a value: ", end="")
        value = input()
        os.environ[i] = value