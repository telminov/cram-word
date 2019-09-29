"""
Интеграция с Яндекс.Словарь
https://yandex.ru/dev/dictionary/doc/dg/concepts/api-overview-docpage/
"""
from typing import Optional

import requests
from django.conf import settings


def from_rus(rus_word: str, lang_code: str) -> Optional[str]:
    url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
    params = {
        'key': settings.YA_API_KEY,
        'lang': f'ru-{lang_code}',
        'text': rus_word,
    }
    response = requests.get(url, params)
    response.raise_for_status()

    response_result = response.json()
    if response_result['def']:
        return response_result['def'][0]['tr'][0]['text']


def to_rus(word: str, lang_code: str) -> Optional[dict]:
    url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
    params = {
        'key': settings.YA_API_KEY,
        'lang': f'{lang_code}-ru',
        'text': word,
    }
    response = requests.get(url, params)
    response.raise_for_status()

    response_result = response.json()
    if response_result['def']:
        result = {
            'translation': response_result['def'][0]['tr'][0]['text'],
            'transcription': response_result['def'][0]['ts'],
        }
        return result

