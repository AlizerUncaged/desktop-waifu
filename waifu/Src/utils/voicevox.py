import os, subprocess, atexit, threading, asyncio, json
from colorama import *

import utils.dependencies
import utils.multi_thread

# Run voicevox
process = None

@atexit.register
def kill_process():
    global process
    print(Fore.RED + "voicevox terminating" + Fore.RESET, flush=True)
    try:
        process.terminate()
        
    except:
        pass

def handle_output(stream, suffix):
    while True:
        line = stream.readline()
        if not line:
            break
        print(Style.DIM + f"voicevox: {line.decode().rstrip()}" + Style.RESET_ALL)

def start():
    global process

    process = subprocess.Popen(
        utils.dependencies.VOICEVOX_DIR + "/run.exe",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if json.loads(os.environ.get("VOICEVOX_LOG",  "False").lower()):
        tasks = [
            threading.Thread(target=handle_output, args=(process.stdout, "stdout")),
            threading.Thread(target=handle_output, args=(process.stderr, "stderr")),
        ]

        for task in tasks:
            task.start()

        for task in tasks:
            task.join()

    # return process.wait()

def run_async():
    utils.multi_thread.run_in_new_thread(start)

    # return await process.wait()

from concurrent.futures import ThreadPoolExecutor
