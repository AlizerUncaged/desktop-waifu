import asyncio, threading


EVENT_LOOPS = {}

def run_in_new_thread(function, *args, **kwargs):
    t = threading.Thread(target=function, args=args, kwargs=kwargs)
    t.start()

    