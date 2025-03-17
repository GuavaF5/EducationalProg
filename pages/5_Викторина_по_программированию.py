import streamlit as st
import requests
import json
import random

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

def generate_questions(access_token: str):
    prompt = (
        "Сгенерируй 10 тестовых вопросов по теме Программирование на Python в формате строки из 10 элементов, разделённых символом '|'. Сразу выводи эту строку, без лишних слов "
        "Формат вывода: [Вопрос 1: ...  | Вопрос 2: ... |  Вопрос 3: ... | Вопрос 4: ...  | Вопрос 5: ... |  Вопрос 6: ... |  Вопрос 7: ...  | Вопрос 8: ... |  Вопрос 9: ... | Вопрос 10: ... ]"
    )
    response = send_prompt(prompt, access_token)
    return response.strip()
 
a = generate_questions(get_access_token())

def parse_question_response(a: str):
    a = a.replace("]", "")
    a = a.replace("[", "")
    parts = a.split("|")    
    questions = [part.strip() for part in parts[:10]]
    return questions

b = parse_question_response(a)

def generate_answers(access_token: str, b: str):
    prompt = (f"Сгенерируй по два варианта ответа к каждому вопросу из {b}. Один из ответов должен быть правильным, а другой - неверным."
            "Представь полученный текст в формате строки. Ответы к вопросу раздели между собой точкой с запятой (;). После неправильного варианта ответа ставь знак '|' "
            '''Формат вывода: [Вопрос 1: Правильный ответ - ... ; Неправильный ответ - ... |
            Вопрос 2: Правильный ответ - ... ; Неправильный ответ - ... |
            Вопрос 3: Правильный ответ - ... ; Неправильный ответ - ... |
            Вопрос 4: Правильный ответ - ... ; Неправильный ответ - ... |
            Вопрос 5: Правильный ответ - ... ; Неправильный ответ - ... |
            Вопрос 6: Правильный ответ - ... ; Неправильный ответ - ... |
            Вопрос 7: Правильный ответ - ... ; Неправильный ответ - ... |
            Вопрос 8: Правильный ответ - ... ; Неправильный ответ - ... |
            Вопрос 9: Правильный ответ - ... ; Неправильный ответ - ... |
            Вопрос 10: Правильный ответ - ... ; Неправильный ответ - ... ]
            Пример вывода: Вопрос 1: Что такое list comprehension в Python?
Правильный ответ - List comprehension — это удобный способ создания списка, при котором можно задать условия фильтрации и преобразования элементов внутри создаваемого списка. Пример: `[x**2 for x in ran
ge(10) if x % 2 == 0]`.
Неправильный ответ - List comprehension — это устаревший способ работы со списками в Python, который был заменен генераторами.
|
Вопрос 2: Как создать и использовать словарь в Python?
Правильный ответ - Словарь в Python создается с использованием фигурных скобок `{}` или функции `dict()`. Например: `my_dict = {"key1": "value1", "key2": "value2"}`. Для добавления элемента используется
 синтаксис `my_dict["new_key"] = "new_value"`.
Неправильный ответ - Словарь в Python создается с использованием квадратных скобок `[ ]`, а для добавления элементов нужно использовать метод `.append()`.
|
Вопрос 3: Какие основные отличия между функциями и методами в Python?
Правильный ответ - Функция — это самостоятельный блок кода, который может существовать вне класса. Метод же всегда принадлежит классу и оперирует его экземплярами. Кроме того, методы получают первый нея
вный аргумент — `self`, который указывает на текущий объект.
Неправильный ответ - Основное отличие заключается в том, что функции могут принимать любые аргументы, тогда как методы ограничены только теми параметрами, которые определены в классе.
|
Вопрос 4: Как работает механизм наследования в Python?
Правильный ответ - Наследование в Python позволяет создавать новый класс на основе существующего. Дочерний класс автоматически получает все атрибуты и методы родительского класса. При необходимости доче
рний класс может переопределять методы родителя и добавлять свои собственные.
Неправильный ответ - Механизм наследования в Python полностью отличается от других языков программирования тем, что здесь нет возможности множественного наследования.
|
Вопрос 5: В чем разница между == и is операторами в Python?
Правильный ответ - Оператор `==` проверяет равенство значений двух объектов, а оператор `is` проверяет тождественность, т.е. являются ли оба объекта одним и тем же объектом в памяти.
Неправильный ответ - Оператор `is` проверяет равенство значений, а `==` проверяет идентичность объектов.
|
Вопрос 6: Как реализовать простой веб-сервер с помощью модуля Flask?
Правильный ответ - Для реализации простого веб-сервера с использованием Flask достаточно создать файл, например, `app.py`, и прописать следующий код:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
```
Неправильный ответ - Чтобы создать веб-сервер с Flask, необходимо установить дополнительный пакет `pip install flask` и затем запускать сервер командой `python -m http.server`.
|
Вопрос 7: Как работать с файлами в Python?
Правильный ответ - Работа с файлами в Python осуществляется с помощью встроенной функции `open()`, которая открывает файл и возвращает файловый объект. После работы с содержимым файл следует закрыть с п
омощью метода `close()`.
Неправильный ответ - Файлы в Python открываются с помощью команды `file_object = File("filename")`, после чего их можно читать или записывать с помощью методов `.read()` и `.write()`.
|
Вопрос 8: Как использовать генераторы (yield) в Python?
Правильный ответ - Генераторы в Python позволяют создавать итераторы, которые могут производить значения по требованию. Ключевое слово `yield` превращает функцию в генератор, возвращая последовательно к
аждое значение вместо одного списка.
Неправильный ответ - Генераторы используются исключительно для обработки больших объемов данных, чтобы экономить память.
|
Вопрос 9: Как обрабатывать исключения в Python?
Правильный ответ - Обработка исключений в Python выполняется с помощью конструкции `try...except...else...finally`. В блоке `try` размещается код, который может вызывать ошибки, а в блоках `except` указ
ываются обработчики для конкретных типов ошибок.
Неправильный ответ - Исключения в Python обрабатываются через конструкцию `raise`, которая принудительно вызывает ошибку, если условие не выполнено.
|
Вопрос 10: Как работают декораторы в Python?
Правильный ответ - Декоратор в Python — это функция, которая принимает другую функцию и возвращает новую функцию с изменённым поведением. Это позволяет расширять функциональность функций или классов без
 изменения их исходного кода.
Неправильный ответ - Декораторы в Python изменяют порядок выполнения программы, позволяя выполнять дополнительные действия перед вызовом основной функции.
            '''
        
        )
    response = send_prompt(prompt, access_token)
    return response

c = generate_answers(get_access_token(), b)


print(c)
def parse_answers_response(c: str):
    parts = c.split("|")    
    ww = [part.strip() for part in parts[:10]]
    questions = ""
    bn = "$"
    for i in range(len(ww)):
        h = ww[i].split("?")
        questions += h[-1]
        questions += bn
    pp = questions.split("$")
    nn = " ".join(pp)
    nn = nn.replace("ответ", "")
    nn = nn.replace("Неправильный", "$")
    nn = nn.replace("Правильный", "|")
    nn = nn.replace("-", "")
    nn = nn.replace("|", "", 1)
    mm = nn.split("|")
    return mm
    

d = parse_answers_response(c)
print(d)
# Инициализация состояния игры
if "health" not in st.session_state:
    st.session_state.health = 100
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False


st.title("Викторина (битва) по программированию на Python")

# Отображение полоски здоровья
st.write(f"Здоровье врага: {st.session_state.health}")
st.progress(st.session_state.health / 100)

# Если игра не завершена
if not st.session_state.game_over:
    # Отображение текущего вопроса
    st.write(f"{b[st.session_state.current_question]}")

    # Отображение вариантов ответов
    options = d[st.session_state.current_question].split("$")
    rightoption = options[0]
    selected_option = st.radio("Выберите ответ:", options)

    # Кнопка для подтверждения ответа
    if st.button("Ответить"):
        if selected_option == rightoption or selected_option == rightoption + (" "):
            st.session_state.health -= 10
            if st.session_state.health <= 0:
                st.session_state.health = 0
                st.session_state.game_over = True
                st.success("Вы победили! 🎉")
            else:
                st.success("Правильный ответ! Здоровье врага уменьшено на 10. Продолжайте в том же духе!")
                st.session_state.current_question += 1
                if st.session_state.current_question >= 10:
                    st.session_state.game_over = True
                    st.success("Вы ответили на все вопросы! Вы победили! 🎉")
                    
                
                    
        
        else:
            st.session_state.game_over = True
            st.error("Неправильный ответ! Игра окончена. 😢")

# Если игра завершена
if st.session_state.game_over:
    if st.session_state.health <= 0:
        st.success("Вы победили! 🎉")
    else:
        st.error("Вы проиграли! 😢")


