import keyboard

KEYS = ["RIGHT_CTRL"]

def audio_input():
    return all(keyboard.is_pressed(key) for key in KEYS)

def audio_input_await():
    keyboard.wait(KEYS[0])