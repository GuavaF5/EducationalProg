import streamlit as st
import requests
import json
import re

# Функция для получения access token

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


# Улучшенная функция для парсинга вопросов и ответов
def generate_backup_questions():
    questions = [
        {
            "question": "Какой оператор используется для создания словаря в Python?",
            "options": ["dict()", "[]", "set()"],
            "correct": 1
        },
        {
            "question": "Что такое декораторы в Python?",
            "options": [
                "Специальные функции, которые изменяют поведение других функций",
                "Встроенная функция для работы с файлами",
                "Инструкция для импорта модулей"
            ],
            "correct": 1
        },
        {
            "question": "Как вывести значение переменной в Python?",
            "options": ["print(var)", "echo var", "puts var"],
            "correct": 1
        },
        {
            "question": "Какая структура данных в Python позволяет хранить элементы в определённом порядке и имеет индексы?",
            "options": ["Словарь", "Список", "Множество"],
            "correct": 2
        },
        {
            "question": "Как создать функцию в Python?",
            "options": [
                "def function_name(): ...",
                "function_name = lambda x: x + 1",
                "function_name = def x: x + 1"
            ],
            "correct": 1
        }
    ]
    return questions

# Улучшенная функция для парсинга сгенерированных вопросов и ответов
def parse_questions(text):
    if not text:
        return []

    questions = []
    lines = text.split("\n")
    current_question = None

    for line in lines:
        line = line.strip()  # Убираем лишние пробелы

        # Обработка вопроса
        if "Вопрос" in line or line.startswith(("1.", "2.", "3.", "4.", "5.")):
            if current_question:
                questions.append(current_question)
            question_text = line.split(":")[-1].strip()  # Убираем "Вопрос X:"
            current_question = {"question": question_text, "options": [], "correct": None}

        # Обработка вариантов ответа
        elif line.startswith(("1.", "2.", "3.")):
            if current_question:
                option = line.split(".", 1)[-1].strip()  # Убираем "1.", "2.", "3."
                current_question["options"].append(option)

        # Обработка правильного ответа
        elif "Правильный ответ" in line:
            if current_question:
                # Извлекаем номер правильного ответа
                match = [s for s in line.split() if s.isdigit()]
                if match:
                    correct_answer = int(match[0])
                    current_question["correct"] = correct_answer

    if current_question:
        questions.append(current_question)
    return questions

# Функция для генерации вопросов
def generate_questions():
    try:
        # Получаем access token
        access_token = get_access_token()
        if not access_token:
            st.error("Не удалось получить токен доступа. Проверьте учетные данные.")
            return None

        # URL API Gigachat
        API_URL = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'

        # Заголовки для авторизации
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Данные для запроса
        data = {
            "model": "GigaChat",  # Указываем модель
            "messages": [
                {
                    "role": "user",
                    "content": f"""
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
                }
            ],
            "temperature": 0.7,
            "max_tokens": 500  # Увеличиваем количество токенов для более длинного ответа
        }

        # Отправка POST запроса к API
        response = requests.post(API_URL, headers=headers, json=data, verify=False)

        # Проверка статуса ответа
        if response.status_code == 200:
            # Парсинг JSON ответа
            result = response.json()
            if "choices" not in result or not result["choices"]:
                st.error("Ответ от API не содержит данных. Проверьте запрос.")
                return None

            generated_text = result["choices"][0].get("message", {}).get("content")
            if not generated_text:
                st.error("Не удалось извлечь текст из ответа API.")
                return None

            # Парсинг вопросов и ответов
            questions = parse_questions(generated_text)
            if not questions:
                st.error("Не удалось распарсить вопросы. Используем резервные вопросы.")
                questions = generate_backup_questions()

            # Проверка, что все вопросы имеют правильные ответы
            for i, question in enumerate(questions):
                if question["correct"] is None:
                    st.error(f"Вопрос {i + 1} не содержит правильного ответа. Используем резервные вопросы.")
                    questions = generate_backup_questions()
                    break

            return questions
        else:
            st.error(f"Ошибка: {response.status_code}")
            st.write(response.text)
            return None
    except Exception as e:
        st.error(f"Произошла ошибка: {e}")
        return None

# Заголовок приложения
st.title("Сражение с вопросами по Python")

# Инициализация состояния игры
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
    questions = generate_questions()
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

# Если игра завершена
if st.session_state.game_over:
    if st.session_state.health <= 0:
        st.success("Вы победили! 🎉")
    else:
        st.error("Вы проиграли! 😢")
