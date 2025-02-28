import streamlit as st
from ooooo import get_access_token, send_prompt

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
