import json
import os
import time
import webbrowser
from copy import deepcopy
from functools import partial

import requests
import streamlit as st

st.set_page_config(page_title="RAG chat")


history_containers: dict[int, st.container] = {}


def get_response(message: str, token) -> str:
    directory: str = "/chatbot/message/new"

    response = requests.post(
        os.environ["API_URL"] + directory,
        data=str(json.dumps({"text": message})),
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        },
    )

    return response.json()["text"]


@st.cache_resource
def _get_user_history(token):

    directory = "/chatbot/message/fetchAll"
    response = requests.get(
        os.environ["API_URL"] + directory,
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        },
    )

    return json.loads(response.content)


def _setup_initial_state():
    first_message = (
        "How can I help you?"
        if st.session_state.is_logged
        else "You have no token! Please obtain one by logging via Google "
        "(button on the left)."
    )
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": first_message}
        ]


def _setup_layout():

    with st.sidebar:
        st.markdown(
            """
        <style>
        .really-big-font {
            font-size:60px !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p class="really-big-font">RAG chat</p>', unsafe_allow_html=True
        )

        if "TOKEN" not in st.session_state:
            _get_google_redirect_button()

        if "TOKEN" in st.session_state:
            st.button(
                "Delete all history",
                key="delete-history",
                on_click=_delete_all_history,
            )


def _delete_all_history():

    keys = list(history_containers.keys())
    for idx in keys:
        _delete_history_element(idx, st.session_state.TOKEN)


def _sign_out():
    raise NotImplementedError


def _get_google_redirect_button():

    directory = "/login"

    response = requests.get(
        os.environ["API_URL"] + directory,
        headers={"accept": "application/json"},
    )

    authorization_url = response.json()["url"]
    button_html = (
        """
    <style>
        .button {
        border-radius: 5px;
        border: 4px solid #26261c;
        font: bold 16px;
        text-decoration: none;
        background-color: #ecbc54;
        color: #26261c;
        padding: 6px 12px 6px 12px;
        border-top: 1px solid #CCCCCC;
        border-right: 1px solid #333333;
        border-bottom: 1px solid #333333;
        border-left: 1px solid #CCCCCC;
        }
       
        a:link {
            color: #26261c;
        }

        a:visited {
            color: #26261c;
        }

        a:hover {
            color: #26261c;
        }

        a:active {
            color: yellow;
            background-color: transparent;
            text-decoration: underline;
        }
    </style>"""
        + f"""
    <a href="{authorization_url}" class="button">Login with Google<a/>
    """
    )

    return st.markdown(button_html, unsafe_allow_html=True)


@st.cache_resource
def _get_token(code):

    directory = "/auth"

    response = requests.get(
        os.environ["API_URL"] + directory + f"?code={code}",
        headers={
            "accept": "application/json",
        },
    )

    token = response.json()["token_json"]["id_token"]
    st.session_state.is_logged = True

    return token


def _delete_history_element(id_: int, token):

    del history_containers[id_]

    if isinstance(st.session_state.history, list):
        ids = list(map(lambda item: item["id"], st.session_state.history))
        history_item = ids.index(id_)

        del st.session_state.history[history_item]

    if token is not None:
        _post_delete_history(id_, token)


def _post_delete_history(id_: int, token):

    if token is None:
        return

    directory = f"/chatbot/message/{id_}/delete"
    _ = requests.delete(
        os.environ["API_URL"] + directory,
        headers={
            "accept": "application/json",
            "Authorization": "Bearer " + token,
        },
    )


def _add_to_history(prompt: str, response: str, username: str):

    if len(history_containers) == 0:
        id_ = -1
    else:
        id_ = min(list(history_containers.keys())) - 1

    with st.sidebar:
        new_container = st.container(border=True)
        with new_container:
            st.markdown(f"**{username}**: {prompt}")
            st.markdown(f"**Response**: {response}")
            st.button(
                "🗑️",
                key=id_,
                on_click=partial(_delete_history_element, id_, None),
            )

    history_containers[id_] = new_container

    if isinstance(st.session_state.history, dict):
        st.session_state.history = []

    st.session_state.history.append(
        {"prompt": prompt, "response": response, "id": id_}
    )


def _load_history(token):

    with st.sidebar:
        st.markdown(
            """
        <style>
        .big-font {
            font-size:30px !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p class="big-font">Chat History</p>', unsafe_allow_html=True
        )

    if token is None:
        return

    history = st.session_state.history

    if isinstance(history, dict) and len(history_containers) == 0:
        return

    with st.sidebar:
        for history_item in history:
            id_ = history_item["id"]

            new_container = st.container(border=True)
            with new_container:
                st.markdown(f"**You**: {history_item['prompt']}")
                st.markdown(f"**Response**: {history_item['response']}")
                st.button(
                    "🗑️",
                    key=id_,
                    on_click=partial(_delete_history_element, id_, token),
                )

            history_containers[id_] = new_container


def _try_get_token():

    if "TOKEN" in st.session_state:
        return st.session_state.TOKEN

    with st.spinner("Processing..."):
        time.sleep(0.5)

        if "code" not in st.session_state:
            if "code" in list(st.query_params.keys()):
                st.session_state.code = deepcopy(st.query_params["code"])

        if "code" in st.session_state:
            token = _get_token(st.session_state.code)
        else:
            token = None
        return token


def main():

    # st.session_state.is_logged = (
    #     True if st.query_params.logged == "yes" else False
    # )

    if "TOKEN" not in st.session_state:
        token = _try_get_token()
        if token is not None:
            st.session_state.is_logged = True
            st.session_state.TOKEN = token
        else:
            st.session_state.is_logged = False
        st.query_params.clear()

    if "TOKEN" in st.session_state:
        history = _get_user_history(st.session_state.TOKEN)
        if isinstance(history, dict):
            st.session_state.history = []
        st.session_state.history = history
    else:
        st.session_state.history = []

    _setup_initial_state()
    _setup_layout()
    if "TOKEN" in st.session_state:
        _load_history(st.session_state.TOKEN)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input(disabled=not st.session_state.is_logged):
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
                        response = get_response(prompt, st.session_state.TOKEN)
                        st.write(response)
                chatbot_message = {"role": "assistant", "content": response}
                st.session_state.messages.append(chatbot_message)

                _add_to_history(prompt, chatbot_message["content"], "You")


if __name__ == "__main__":
    main()
