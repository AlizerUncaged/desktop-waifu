import keyboard
import time

def audio_input():
    return keyboard.is_pressed('RIGHT_SHIFT')

def audio_input_await():
    while not audio_input():
        time.sleep(0.1)