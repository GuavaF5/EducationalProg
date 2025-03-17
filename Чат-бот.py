import streamlit as st
import requests
import json

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


st.set_page_config(page_title = "Сайт с обучающей программой") 
st.title("Чат-бот")
st.sidebar.success("Меню") 


if "access_token" not in st.session_state:
    try:
        st.session_state.access_token = get_access_token()
        st.toast("Получил токен")
    except Exception as e:
        st.toast(f"Не получилось получить токен: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "ai", "content": "Что вы хотите узнать?"}]

for msg in st.session_state.messages:
    
    st.chat_message(msg["role"]).write(msg["content"])


if user_prompt := st.chat_input():
    st.chat_message("user").write(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    response = send_prompt(user_prompt, st.session_state.access_token)

    st.chat_message("ai").write(response)
    st.session_state.messages.append({"role": "ai", "content": response})
