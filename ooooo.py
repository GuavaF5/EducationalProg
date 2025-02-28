import requests
import json
import streamlit as st
from gigachat import GigaChat

def get_access_token() -> str:
  url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

  payload='scope=GIGACHAT_API_PERS'
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': '254ee246-4b6b-49e3-b72e-29c60d84e69d',
    'Authorization': 'Basic YjA2NmI2NDAtZTU3ZC00ZDJkLTk3OWMtODRmYzkyNjAyZjI2OjczYzc1NjdkLWNjNWEtNDJmMS04ZGI3LWFhZTQxZjBlM2UxOA=='
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  access_token = response.json()["access_token"]
  return access_token

def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat-Pro",
        "messages": [
            {
                "role": "user",
                "content": msg,
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response.json()["choices"][0]["message"]["content"]


def questions(access_token: str):
    url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions' 

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    payload = json.dumps({
        "model": "GigaChat-Pro",
        "messages": [
        {
            "role": "system",
            "content": "Ты должен задать любой вопрос по теме БИОЛОГИЯ или ФИЗИКА или ИСТОРИЯ.\nВопрос должен соответствовать уровню 10 класса школы. \nИспользуй научный лексикон для этого.]"
        },
        {
            "role": "user",
            "content": "<Текст вопроса>"
        }
    ]
})
    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response.json()["choices"][0]["message"]["content"]


def q2(access_token: str, msg: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "prompt": "Сгенерируй 5 тестовых вопросов по теме 'Программирование на Python'.",
        "max_tokens": 100,
        "temperature": 0.7,
        "n": 1
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    generated_text = result['choices'][0]['text']
    return generated_text
print(q2)