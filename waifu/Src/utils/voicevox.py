import os, subprocess, atexit, threading, asyncio
from colorama import *

import utils.dependencies

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

async def handle_output(stream, suffix):
    while True:
        line = await stream.readline()
        if not line:
            break
        print(Style.DIM + f"voicevox: {line.decode().rstrip()}" + Style.RESET_ALL)

async def start():
    global process

    process = await asyncio.create_subprocess_exec(
        utils.dependencies.VOICEVOX_DIR + "/run.exe",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    if os.environ.get("VOICEVOX_LOG") == "True":
        tasks = [
            asyncio.create_task(handle_output(process.stdout, "stdout")),
            asyncio.create_task(handle_output(process.stderr, "stderr")),
        ]

        await asyncio.gather(*tasks)

    return await process.wait()

from concurrent.futures import ThreadPoolExecutor

def run_async():    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    t = threading.Thread(target=lambda: loop.run_until_complete(start()))
    t.start()
    return t