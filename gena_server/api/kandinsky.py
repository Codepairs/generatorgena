import json
import time
import base64
import uuid as uid
import os
from pathlib import Path

from django.conf import settings

import requests


class FusionBrainAPI:

    def __init__(self):
        self.url = 'https://api-key.fusionbrain.ai/'
        self.AUTH_HEADERS = {
            'X-Key': f'Key {settings.KANDINSKY_API_KEY}',
            'X-Secret': f'Secret {settings.KANDINSKY_SECRET_KEY}',
        }

    def get_pipeline(self):
        response = requests.get(self.url + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
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
        response = requests.post(self.url + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.url + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            print(data)
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)

#if __name__ == '__main__':
#    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', '06A3A1C1C6B7E26C84233547A56AA0A3', 'D3817014623AE5637C5BA5C0300E08DB')
#    pipeline_id = api.get_pipeline()
#    uuid = api.generate("Сюрреалистичная картина с плавящимися часами и абстрактными фигурами на фоне заката", pipeline_id)
#    files = api.check_generation(uuid)