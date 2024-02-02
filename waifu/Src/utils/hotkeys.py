import keyboard
import time

KEYS = ["CTRL"]

def audio_input():
    return all(keyboard.is_pressed(key) for key in KEYS)

def audio_input_await():
    while not audio_input():
        time.sleep(0.1)
