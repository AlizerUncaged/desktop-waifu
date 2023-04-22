import os, subprocess, atexit, threading, asyncio, websocket, json
from colorama import *

import utils.dependencies

ws = None
process = None
reply_callback = None

# gets called whenever the javascript characterai endpoint
# responded
def on_message(ws, message):
    if os.environ.get("CHARACTERAI_LOG") == "True":
        print(f"{Style.DIM}characterAI message: {message}")
    reply_callback(message)
    # print(f"recieved message {message}")

def on_close(ws):
    print(f"{Fore.RED + Style.BRIGHT}characterAI websocket closed!{Fore.RESET + Style.RESET_ALL}")

def run_websocket():
    global ws
    ws = websocket.WebSocketApp(f"ws://localhost:{utils.dependencies.CHARACTERAI_PORT}/",
                                on_message=on_message,
                                on_close=on_close)
    print(f"{Fore.GREEN}websocket connected!{Fore.RESET}")
    ws.run_forever()
    
def send_message_to_process_via_websocket(message):
    global ws
    ws.send(message)

async def send_message_to_process_via_stdin(message):
    global process

    process.stdin.write(message.encode() + b"\n")
    await process.stdin.drain()

@atexit.register
def kill_process():
    global process
    print(Fore.RED + "node js" + Fore.RESET, flush=True)
    try:
        process.terminate()
    except:
        pass

async def handle_output(stream, suffix):
    while True:
        line = await stream.readline()
        if not line:
            break
        print(Style.DIM + f"node js: {line.decode().rstrip()}" + Style.RESET_ALL)

async def start():
    global process

    process = await asyncio.create_subprocess_exec(
        utils.dependencies.NODE,
        "character_ai/runner.js",
        str(os.environ.get("CHARACTERAI_CHARACTER", "_PjRfiokij64UvriwbB7QCZ_QJfSoKXh1U7WqMT1A98")),
        str(utils.dependencies.CHARACTERAI_PORT),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    
    t = threading.Thread(target=run_websocket)
    t.start()

    if json.loads(os.environ.get("CHARACTERAI_LOG",  "False").lower()):
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
