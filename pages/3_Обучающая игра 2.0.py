import streamlit as st
import requests
import json
import re
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

with GigaChat(credentials=..., verify_ssl_certs=False) as giga:
    response = giga.chat("Какие факторы влияют на стоимость страховки на дом?")
    print(response.choices[0].message.content)

def generate_test():
    access_token = get_access_token()
    if not access_token:
        st.error("Не удалось получить токен доступа. Проверьте учетные данные.")
        return None
    with GigaChat(verify_ssl_certs=False) as giga:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        temperature: 0.7
        max_tokens: 500 
        prompt =  f"""
                    Сгенерируй 10 тестовых вопросов по теме 'Программирование на Python'.
                    Для каждого вопроса предоставь три варианта ответа, один из которых должен быть правильным.
                    Формат вывода:
                    Вопрос 1: [текст вопроса]
                    Варианты ответа:
                    1. [вариант 1]
                    2. [вариант 2]
                    3. [вариант 3]
                    Правильный ответ: [номер правильного ответа]
                    """
        response = giga.chat(prompt)
        return response

st.title("Сражение с вопросами по Python")

if "health" not in st.session_state:
    st.session_state.health = 100
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "questions" not in st.session_state:
    st.session_state.questions = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Кнопка для начала сражения
if st.button("Начать сражение"):
    questions = generate_test()
    if questions:
        st.session_state.questions = questions
        st.session_state.current_question = 0
        st.session_state.health = 100
        st.session_state.game_over = False

# Если вопросы сгенерированы и игра не завершена
if st.session_state.questions and not st.session_state.game_over:
    # Отображение полоски здоровья
    st.write(f"Здоровье: {st.session_state.health}")
    st.progress(st.session_state.health / 100)

    # Текущий вопрос
question = st.session_state.questions[st.session_state.current_question]
st.write(f"**Вопрос {st.session_state.current_question + 1}:** {question['question']}")

    # Варианты ответов
selected_option = st.radio(
    "Выберите ответ:",
    question["options"],
    key=f"question_{st.session_state.current_question}"
)

# Кнопка для подтверждения ответа
if st.button("Ответить"):
    if question["correct"] is not None:
        correct_answer = question["options"][question["correct"] - 1]
        if selected_option == correct_answer:
            st.session_state.health -= 10
            if st.session_state.health <= 0:
                st.session_state.health = 0
                st.session_state.game_over = True
                st.success("Вы победили! 🎉")
             else:
                st.success("Правильный ответ! Здоровье уменьшено на 10.")
                st.session_state.current_question += 1
                if st.session_state.current_question >= len(st.session_state.questions):
                    st.session_state.game_over = True
                    st.success("Вы ответили на все вопросы! Вы победили! 🎉")
         else:
            st.session_state.game_over = True
            st.error("Вы проиграли! 😢")
      else:
          st.error("Ошибка: вопрос не содержит правильного ответа.")
