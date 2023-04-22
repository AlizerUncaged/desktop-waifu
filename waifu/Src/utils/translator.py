from googletrans import Translator

TRANSLATOR = Translator()

def translate_to_jp(text):
    global TRANSLATOR
    result = TRANSLATOR.translate(text=text, dest='ja')
    return result.text
