import streamlit as st
import requests
import json

# Функция для получения токена
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

# Функция для отправки запроса к GigaChat
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


# Функция для получения случайного города
def get_random_city(access_token: str):
    prompt = (
        "Назови один случайный город в мире, и три слова, которые с ним ассоциируются, "
        "но это не должно быть название страны, и в тексте ни в коем случае нельзя называть страну, "
        "в которой находится город. Формат вывода: [Название одного города (в одно слово) - три слова, ассоциируемые с этим городом.]. "
        "Постарайся назвать не очень популярный город, и не очень большой по численности населения."
    )
    city = send_prompt(prompt, access_token)
    city = city.replace("[", "")
    city = city.replace("]", "")
    city = city.replace("(", "")
    city = city.replace(")", "")
    return city.strip()

# Функция для получения страны по городу
def get_country_by_city(city: str, access_token: str):
    prompt = f"В какой стране находится город {city}? В выводе должно содержаться только одно слово - название страны. Формат вывода: [Название страны]"
    country = send_prompt(prompt, access_token)
    return country.strip()

# Заголовок приложения
st.title("Угадай страну")

# Инициализация состояния сессии для токена
if "access_token" not in st.session_state:
    try:
        st.session_state.access_token = get_access_token()
        st.toast("Токен успешно получен")
    except Exception as e:
        st.toast(f"Не удалось получить токен: {e}")

# Инициализация состояний
if "city" not in st.session_state:
    st.session_state.city = None
if "country" not in st.session_state:
    st.session_state.country = None
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""
if "show_question" not in st.session_state:
    st.session_state.show_question = False

# Кнопка для начала игры
if st.button("Сыграть в угадай страну"):
    st.session_state.city = get_random_city(st.session_state.access_token)
    st.session_state.country = get_country_by_city(st.session_state.city, st.session_state.access_token)
    st.session_state.user_answer = ""  # Сброс ответа пользователя
    st.session_state.show_question = True  # Показываем вопрос    


# Если игра начата, отображаем город и поле для ввода
if st.session_state.show_question:
    st.write(f"{st.session_state.city}")
    user_answer = st.text_input("В какой стране находится этот город?", value=st.session_state.user_answer)

    # Если пользователь ввёл ответ, проверяем его
    if user_answer:
        st.session_state.user_answer = user_answer  # Сохраняем ответ пользователя
        if user_answer.lower() == st.session_state.country.lower():
            st.success("Правильно! Вы угадали!")
        else:
            st.error(f"Неправильно. Правильный ответ: {st.session_state.country}")
        st.session_state.show_question = False  # Скрываем вопрос после ответа

if st.button("Перезапустить игру 1"):
        st.session_state.city = None
        st.session_state.country = None
        st.session_state.user_answer = ""
        st.session_state.show_question = False
        st.rerun()

