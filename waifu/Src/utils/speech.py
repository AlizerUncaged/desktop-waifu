import torch, os

DEVICE = torch.device(os.environ.get("TORCH_DEVICE", "cpu"))

LOCAL_FILE = 'model.pt'

def prepare():
    global DEVICE, LOCAL_FILE
    torch.set_num_threads(4)
    if not os.path.isfile(LOCAL_FILE):
        torch.hub.download_url_to_file(f'https://models.silero.ai/models/tts/{"en"}/{"v3_en"}.pt',
                                    LOCAL_FILE)  

def silero_tts(message, language = "en", model = "v3_en", speaker = "en_21"):
    global DEVICE, LOCAL_FILE

    model = torch.package.PackageImporter(LOCAL_FILE).load_pickle("tts_models", "model")
    model.to(DEVICE)

    sample_rate = 48000

    audio_paths = model.save_wav(text=message,
                                speaker=speaker,
                                put_accent=True,
                                put_yo=True,
                                sample_rate=sample_rate)
    return audio_paths