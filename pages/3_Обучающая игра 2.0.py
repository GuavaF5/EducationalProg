import streamlit as st
import requests
import json
import random

def get_access_token() -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload = 'scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': '254ee246-4b6b-49e3-b72e-29c60d84e69d',
        'Authorization': 'Basic YjA2NmI2NDAtZTU3ZC00ZDJkLTk3OWMtODRmYzkyNjAyZjI2OjczYzc1NjdkLWNjNWEtNDJmMS04ZGI3LWFhZTQxZjBlM2UxOA=='
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    access_token = response.json()["access_token"]
    return access_token

def send_prompt(user_question: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat-Pro",
        "messages": [
            {
                "role": "user",
                "content": user_question,
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

def get_random_city(access_token: str):
    # Запрос к GigaChat для получения случайного города
    prompt = "Назови случайный город в мире. НИ ЗА ЧТО НЕ УПОМИНАЙ СТРАНУ В КОТОРОЙ ОН НАХОДИТСЯ. В тексте ни в коем случае нельзя называть страну, в которой находится город. Только название города и его краткое описание, без страны. Можешь брать город из любой части мира"
    city = send_prompt(prompt, access_token)
    return city.strip()

def get_country_by_city(city: str, access_token: str):
    # Запрос к GigaChat для получения страны по городу
    prompt = f"В какой стране находится город {city}? В выводе должно содержаться только одно слово - название страны. Формат вывода: [Название страны]"
    country = send_prompt(prompt, access_token)
    return country.strip()

if "access_token" not in st.session_state:
    try:
        st.session_state.access_token = get_access_token()
        st.toast("Токен успешно получен")
    except Exception as e:
        st.toast(f"Не удалось получить токен: {e}")

st.title("Угадай страну")

if "city" not in st.session_state:
    st.session_state.city = None
if "country" not in st.session_state:
    st.session_state.country = None
if "user_answer" not in st.session_state:
    st.session_state.user_answer = None

if st.button("Сыграть в угадай страну"):
    st.session_state.city = get_random_city(st.session_state.access_token)
    st.session_state.country = get_country_by_city(st.session_state.city, st.session_state.access_token)
    st.session_state.user_answer = None  # Сброс предыдущего ответа пользователя

if st.session_state.city:
    st.write(f"Город: {st.session_state.city}")
    st.session_state.user_answer = st.text_input("В какой стране находится этот город?")

    if st.session_state.user_answer:
        if st.session_state.user_answer.lower() == st.session_state.country.lower():
            st.success("Правильно! Вы угадали!")
        else:
            st.error(f"Неправильно. Правильный ответ: {st.session_state.country}")
