# Control mouth movements.
import pyvts
import asyncio, threading, os, time, base64, random
from colorama import *
import utils.multi_thread

VTS = pyvts.vts(
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


async def my_async_function():
    # This is just an example, replace this with your own async function
    print("Hello from async function!")


""" def thread_function():
    while True:
        EVENT_LOOP.create_task(vts.request(
            vts.vts_request.requestSetParameterValue(parameter=VOICE_PARAMETER, value=random.uniform(-2, 2))
        ))
        print("sent")
        time.sleep(1)
        
async def create_new_tracking_parameter():
    global VOICE_PARAMETER
    # We can finally move the mouth lesgo
    # This is assuming the user didn't change the default tracking
    # parameter for the mouth, which is MouthOpen.
    

    thread_function() """


mouse_movement_semaphore = threading.Semaphore(0)

""" AUDIO_LEVEL = 0

async def audio_level_loop():
    global AUDIO_LEVEL
    while True:
        print()
        mouse_movement_semaphore.acquire()
        await  """

""" async def set_audio_level_async(level):
    global VOICE_PARAMETER
    result = await 
    print("Result")
    print(result) """

EVENT_LOOP = None
VOICE_LEVEL = 0

def set_audio_level(level):
    global VOICE_PARAMETER, EVENT_LOOP, VOICE_LEVEL

    """ if EVENT_LOOP is None:
        print("new event loop")
        EVENT_LOOP = asyncio.new_event_loop()
       
    parameters = VTS.vts_request.requestSetParameterValue(parameter=VOICE_PARAMETER, value=level) """
    VOICE_LEVEL = level
    
    # holy hell this is very slow, im not sure what is causing it
    # but this lags vtube studio
    """ print("sending" + str(level))

    # EVENT_LOOP.run_until_complete(vts.request(parameters))

    EVENT_LOOP.create_task(vts.request(parameters))

    print("sent" + str(level)) """
    # utils.multi_thread.run_in_new_thread(set_audio_level_async, level)
    

def get_icon():
    with open('./repo/icon.png', 'rb') as file:
        encoded_string = base64.b64encode(file.read())
        return encoded_string.decode('utf-8')


async def start():
    global VTS, VOICE_LEVEL
    icon_base64 = get_icon()
    VTS.vts_request.icon = icon_base64

    # Attempt to connect to VTube Studio
    tries = 0
    is_connected = False

    print(f"Connecting to VTube Studio!")
    
    while True:
        try:
            if not is_connected:
                await VTS.connect()
                is_connected = True
            print(f"Authentication request sent to VTube Studio, please{Fore.GREEN}{Style.BRIGHT} click allow{Fore.RESET}{Style.RESET_ALL}.")
            await VTS.request_authenticate_token()
            await VTS.request_authenticate()
            break
        except KeyboardInterrupt: # User quit
            break
        except (ConnectionRefusedError, KeyError):
            tries += 1
            print(f"> Attempting to connect to VTube Studio {Fore.RED}attempt {tries}{Fore.RESET}")
            print(f"Please run VTube Studio, you may download it at {Fore.GREEN}https://store.steampowered.com/app/1325860/VTube_Studio/{Fore.RESET}")
            print(f"After it, go to settings at the VTube Studio Plugins section and toggle {Fore.GREEN}\"Start API\"{Fore.RESET}")
            time.sleep(7 if tries > 7 else tries)

    print(f"{Style.BRIGHT}{Fore.MAGENTA}VTube Studio connected!{Fore.RESET} at port {Fore.BLUE}{VTS.port}{Fore.RESET}")
    # Set up audio level loop
    current_voice_level = 0
    while True:
        try:
            if VOICE_LEVEL != current_voice_level:
                await VTS.request(
                        VTS.vts_request.requestSetParameterValue(parameter=VOICE_PARAMETER, value=VOICE_LEVEL)
                    )
                current_voice_level = VOICE_LEVEL
        except KeyboardInterrupt:
            break
        
        await asyncio.sleep(1/30) # 30fps

    # I've read the source of pyvts and it's really really broken,
    # icon doesn't work until we set it explicitly here.


from concurrent.futures import ThreadPoolExecutor

def start_real():
    global EVENT_LOOP  
    EVENT_LOOP = asyncio.new_event_loop()
    EVENT_LOOP.run_until_complete(start())

def run_async():  
    t = threading.Thread(target=start_real)
    t.daemon = True
    t.start()
    """ loop = asyncio.new_event_loop()
    loop.run_until_complete() """
    
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