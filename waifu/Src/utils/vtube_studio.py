# control mouth movements
import pyvts
import asyncio, threading, os
from colorama import *
async def start():
    vts = pyvts.vts(
        plugin_info={
            "plugin_name": "waifu-vtuber",
            "developer": "Alizer",
            "authentication_token_path": "./token.txt",
            "icon" : "" # put
        },
        vts_api_info={
            "version" : "1.0",
            "name" : "VTubeStudioPublicAPI",
            "port": os.environ.get("VTUBE_STUDIO_API_PORT", 8001)
        }
    )

    await vts.connect()

    print(f"Authentication request sent to VTube Studio, please{Fore.GREEN}{Style.BRIGHT} click allow{Fore.RESET}{Style.RESET_ALL}.")
    
    await vts.request_authenticate_token()
    await vts.request_authenticate()

    print(f"{Style.BRIGHT}{Fore.MAGENTA}vtube studio connected!{Fore.RESET} at port {Fore.BLUE}{vts.port}")
    
from concurrent.futures import ThreadPoolExecutor

def run_async():    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    t = threading.Thread(target=lambda: loop.run_until_complete(start()))
    t.start()
    return t