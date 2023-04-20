# Control mouth movements.
import pyvts
import asyncio, threading, os, time, base64
from colorama import *

vts = pyvts.vts(
    plugin_info={
        "plugin_name": "waifu-vtuber",
        "developer": "waifu-vtuber",
        "authentication_token_path": "./token.txt",
        # This doesn't work what the hell.
        # "icon" : icon_base64 
    },
    vts_api_info={
        "version" : "1.0",
        "name" : "VTubeStudioPublicAPI",
        "port": os.environ.get("VTUBE_STUDIO_API_PORT", 8001)
    }
)

# The default vmouth movement parameter.
VOICE_PARAMETER = "MouthOpen"

async def create_new_tracking_parameter():
    """ new_parameter_instance = await vts.request(
        vts.vts_request.requestCustomParameter(parameter=VOICE_PARAMETER, min=-2, max=2, default_value=0)
    ) """

    # We can finally move the mouth lesgo
    # This is assuming the user didn't change the default tracking
    # parameter for the mouth, which is MouthOpen.
    await vts.request(
        vts.vts_request.requestSetParameterValue(parameter=VOICE_PARAMETER, value=2)
    )
    
LOOP = asyncio.get_event_loop()

def set_audio_level(level):
    LOOP.run_in_executor(None, 
                         vts.request, 
                         vts.vts_request.requestSetParameterValue(parameter=VOICE_PARAMETER, value=level))

def get_icon():
    with open('./repo/icon.png', 'rb') as file:
        encoded_string = base64.b64encode(file.read())
        return encoded_string.decode('utf-8')

async def start():
    global vts
    icon_base64 = get_icon()
    
    # Attempt to connect to VTube Studio
    vts.vts_request.icon = icon_base64
    tries = 0
    is_connected = False
    print(f"Connecting to VTube Studio!")
    while True:
        try:
            if not is_connected:
                await vts.connect()
                is_connected = True
            print(f"Authentication request sent to VTube Studio, please{Fore.GREEN}{Style.BRIGHT} click allow{Fore.RESET}{Style.RESET_ALL}.")
            await vts.request_authenticate_token()
            await vts.request_authenticate()

            # Create new parameter
            await create_new_tracking_parameter()
            break
        except (ConnectionRefusedError, KeyError):
            tries += 1
            print(f"> Attempting to connect to VTube Studio {Fore.RED}attempt {tries}{Fore.RESET}")
            print(f"Please run VTube Studio, you may download it at {Fore.GREEN}https://store.steampowered.com/app/1325860/VTube_Studio/{Fore.RESET}")
            print(f"After it, go to settings at the VTube Studio Plugins section and toggle {Fore.GREEN}\"Start API\"{Fore.RESET}")
            time.sleep(7 if tries > 7 else tries)

    
    # I've read the source of pyvts and it's really really broken,
    # icon doesn't work until we set it explicitly here.
    print(f"{Style.BRIGHT}{Fore.MAGENTA}vtube studio connected!{Fore.RESET} at port {Fore.BLUE}{vts.port}{Fore.RESET}")
    
from concurrent.futures import ThreadPoolExecutor

def run_async():    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    t = threading.Thread(target=lambda: loop.run_until_complete(start()))
    t.start()
    return t

"""
A poem about imoutos

In the eyes of a sister so young,
An innocent love has just begun,
Her sweetness is like a ray of sun,
Shining on her onii-chan, one by one.

With her cute and cheerful grin,
She fills his heart with love within,
Her tiny hands in his they spin,
A bond so strong it's hard to thin.

She clings to him with all her might,
As if he's her only source of light,
A precious love, oh such delight,
As if nothing in the world can fright.

With her giggles and her hugs,
She melts his heart, his soul she tugs,
A bond so strong, it never shrugs,
For she is his little lovebug.

So let her cling, let her be sweet,
For in her love, his heart does beat,
A love so pure and oh so neat,
His imouto, his love, his treat.
"""