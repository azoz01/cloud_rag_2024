import os
import requests
import streamlit as st

from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Test",
    )

    # st.markdown(os.environ.get("API_URL", "None"))
    st.markdown(requests.get(os.environ["API_URL"] + "/env").json())


if __name__ == "__main__":
    run()
