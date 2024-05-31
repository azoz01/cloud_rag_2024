import json
from functools import partial

import requests
import streamlit as st

site = "https://ragapi-hw2k5v4d7q-uc.a.run.app"

st.session_state.TOKEN = "<TMP_TOKEN>"

history_containers: dict[int, st.container] = {}


def get_response(message: str) -> str:
    directory: str = "/chatbot/message/new"

    response = requests.post(
        site + directory,
        data=str(json.dumps({"text": message})),
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + st.session_state.TOKEN,
        },
    )

    return response.json()["text"]


def _get_user_history():
    directory = "/chatbot/message/fetchAll"
    response = requests.get(
        site + directory,
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + st.session_state.TOKEN,
        },
    )

    return json.loads(response.content)


def _setup_initial_state():
    st.session_state.is_logged = False
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I help you?"}
        ]


def _setup_layout():

    st.set_page_config(page_title="RAG chat")

    with st.sidebar:
        st.title("RAG chat history")
        st.button("Login with Google", key="google-log", on_click=_login)


def _login():
    raise NotImplementedError
    st.session_state.is_logged = True
    st.session_state.TOKEN = "..."


def _delete_history_element(id_: int):

    del history_containers[id_]

    _post_delete_history(id_)


def _post_delete_history(id_: int):

    directory = f"/chatbot/message/{id_}/delete"
    _ = requests.delete(
        site + directory,
        headers={
            "accept": "application/json",
            "Authorization": "Bearer " + st.session_state.TOKEN,
        },
    )


def _load_history():

    history = _get_user_history()

    if len(history) == 0:
        with st.sidebar:
            with st.container(border=True):
                st.markdown("The history of the chat is empty! 😥.")
        return

    with st.sidebar:
        for history_item in history:
            full_username = history_item["username"]
            id_ = history_item["id"]
            try:
                at_index = full_username.index("@")
            except ValueError:
                at_index = len(full_username)
            username = full_username[:at_index]
            new_container = st.container(border=True)
            with new_container:
                st.markdown(f"**{username}**: {history_item['prompt']}")
                st.markdown(f"**Response**: {history_item['response']}")
                st.button(
                    "🗑️",
                    key=id_,
                    on_click=partial(_delete_history_element, id_),
                )

            history_containers[id_] = new_container


def main():
    _setup_initial_state()
    _setup_layout()
    _load_history()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input():
        if prompt is not None:

            # User-provided prompt
            user_message = {"role": "user", "content": prompt}
            st.session_state.messages.append(user_message)

            with st.chat_message("user"):
                st.write(prompt)

            # Generate a new response if last message is not from assistant
            if st.session_state.messages[-1]["role"] != "assistant":
                with st.chat_message("assistant"):

                    with st.spinner("Thinking..."):
                        response = get_response(prompt)
                        st.write(response)
                chatbot_message = {"role": "assistant", "content": response}
                st.session_state.messages.append(chatbot_message)


if __name__ == "__main__":
    main()
