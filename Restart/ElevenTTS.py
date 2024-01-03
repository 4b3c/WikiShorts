import requests


def save_audio(text, save_file):
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/tSqWUhQ9nAcICRpWve5y"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "76a9308c2f88e21ba1d010dfe02e902e"
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.6,
            "style": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open(save_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)