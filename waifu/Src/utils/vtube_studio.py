# Control mouth movements.
import pyvts
import asyncio, threading, os, time, base64
from colorama import *
import utils.multi_thread

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


mouse_movement_semaphore = threading.Semaphore(0)

""" AUDIO_LEVEL = 0

async def audio_level_loop():
    global AUDIO_LEVEL
    while True:
        print()
        mouse_movement_semaphore.acquire()
        await  """

async def set_audio_level_async(level):
    await vts.request(vts.vts_request.requestSetParameterValue(parameter=VOICE_PARAMETER, value=2))

def set_audio_level(level):
    print("setting audio level")
    utils.multi_thread.run_in_new_thread(set_audio_level_async, "set_audio_level", level)
    print("audio level set")
    

def get_icon():
    with open('./repo/icon.png', 'rb') as file:
        encoded_string = base64.b64encode(file.read())
        return encoded_string.decode('utf-8')


async def start():
    global vts
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    icon_base64 = get_icon()
    vts.vts_request.icon = icon_base64

    # Attempt to connect to VTube Studio
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

    # Set up audio level loop
    # while True:
    #     print()
    #     mouse_movement_semaphore.acquire()
    #     set_audio_level(2)

    # I've read the source of pyvts and it's really really broken,
    # icon doesn't work until we set it explicitly here.
    print(f"{Style.BRIGHT}{Fore.MAGENTA}VTube Studio connected!{Fore.RESET} at port {Fore.BLUE}{vts.port}{Fore.RESET}")


from concurrent.futures import ThreadPoolExecutor

def run_async():    
    asyncio.get_event_loop().run_in_executor(None, asyncio.run(start()))
    # utils.multi_thread.run_in_new_thread(asyncio.run, start)
    # utils.multi_thread.run_in_new_thread(audio_level_loop)
    """ mouth_movement_thread = threading.Thread(target=audio_level_loop)
    mouth_movement_thread.start() """
    

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