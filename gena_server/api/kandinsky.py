import json
import time
import base64
import uuid as uid
import os
from pathlib import Path


import requests


class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get('https://api-key.fusionbrain.ai/' + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        print('pipeline')
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": "{prompt}"
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post('https://api-key.fusionbrain.ai/' + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        print('generate')
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get('https://api-key.fusionbrain.ai/' + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            print('check_generation')
            print(data)
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)

def save_image(str_image):
    # Сохранение строки base64 в файл
    binary_img = base64.b64decode(str_image)
    folder = './images'
    os.makedirs(folder, exist_ok=True)

    # Генерируем уникальное имя файла
    filename = f"{uid.uuid4().hex}.jpg"  # Уникальный идентификатор
    filepath = os.path.join(folder, filename)
    
    # Сохраняем файл
    with open(filepath, 'wb') as new_img:
        new_img.write(binary_img)
    
    print(filepath)

if __name__ == '__main__':
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', '06A3A1C1C6B7E26C84233547A56AA0A3', 'D3817014623AE5637C5BA5C0300E08DB')
    pipeline_id = api.get_pipeline()
    uuid = api.generate("Сюрреалистичная картина с плавящимися часами и абстрактными фигурами на фоне заката", pipeline_id)
    files = api.check_generation(uuid)
    save_image(files[0])