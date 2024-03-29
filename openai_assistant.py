"""
Author: Jean-Francois Gosselin
Email: jfgosselin@gmail.com
Date: 2024-03-28

Description: This Python application utilizes the Streamlit library to create a web-based chat interface that interacts with OpenAI's GPT model. 
It initializes the Streamlit UI and sets up a chat environment where users can interact with the AI model. The configuration for the OpenAI API 
and UI elements such as page title, welcome message, and chat instructions are dynamically loaded from environment variables using a singleton
configuration class, ensuring a flexible and easily configurable application. The script handles user inputs, sends them to the OpenAI API, and 
displays the AI's responses, creating an interactive chat experience. Custom CSS is applied to tailor the UI, and markdown content is dynamically
rendered from a file, enhancing the application's presentation and usability.
"""


from dotenv import load_dotenv
import os
import streamlit as st
from openai import OpenAI

class Config:
    """Singleton configuration class for environment variables."""
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    ASSISTANT_KEY = os.getenv("ASSISTANT_KEY")
    PAGE_TITLE = os.getenv("PAGE_TITLE")
    WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE")
    INSTRUCTIONS = os.getenv("INSTRUCTIONS")
    USER_PROMPT = os.getenv("USER_PROMPT")
    BEGIN_MESSAGE = os.getenv("BEGIN_MESSAGE")
    EXIT_MESSAGE = os.getenv("EXIT_MESSAGE")
    START_CHAT_BUTTON = os.getenv("START_CHAT_BUTTON")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    DISCLAIMER=os.getenv("DISCLAIMER")
    LOGO=os.getenv("LOGO")


def initialize_openai_client():
    """Initializes and returns the OpenAI client along with the assistant object."""
    client = OpenAI(api_key=Config.API_KEY)
    assistant = client.beta.assistants.retrieve(Config.ASSISTANT_KEY)
    return client, assistant

def setup_streamlit_ui():
    """Configures Streamlit's page and displays initial UI components."""
    st.set_page_config(page_title=Config.PAGE_TITLE, page_icon=":speech_balloon:")
    apply_custom_css()
    display_markdown_content(Config.DISCLAIMER)
    if os.path.isfile(Config.LOGO):
     st.image(Config.LOGO, width=90)
    st.title(Config.PAGE_TITLE)
    st.write(Config.WELCOME_MESSAGE)

def apply_custom_css():
    """Applies custom CSS to hide default Streamlit elements and adjust the layout."""
    custom_css = """
        <style>
            .reportview-container {margin-top: -2em;}
            #MainMenu, .stDeployButton, footer, #stDecoration {visibility: hidden;}
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def display_markdown_content(file_path):
    """Reads and displays markdown content from a specified file."""
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        st.markdown(content, unsafe_allow_html=True)

def initialize_chat_variables():
    """Initializes necessary chat variables in Streamlit's session state."""
    defaults = {"start_chat": False, "thread_id": None, "messages": []}
    for key, default in defaults.items():
        st.session_state.setdefault(key, default)

def handle_chat_interaction(client, assistant):
    """Manages user interactions and chat logic."""
    if not st.session_state.get('start_chat', False):
        if st.button(Config.START_CHAT_BUTTON):
           start_new_chat_session(client)
           st.rerun()

    if 'start_chat' in st.session_state and st.session_state.start_chat:  
      if st.button(Config.EXIT_MESSAGE):
         reset_chat_session()
         st.rerun()
    if st.session_state.start_chat:
        display_chat_messages()
        user_input = st.chat_input(Config.USER_PROMPT)
        if user_input:
            process_and_display_chat_interaction(user_input, client, assistant)
    else:
      st.write(Config.BEGIN_MESSAGE)
      
def start_new_chat_session(client: OpenAI):
    """Begins a new chat session by creating a new thread."""
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

def reset_chat_session():
    """Resets the chat session to its initial state."""
    st.session_state["messages"] = []
    st.session_state["start_chat"] = False
    st.session_state["thread_id"] = None

def display_chat_messages():
    """Displays all chat messages stored in the session state."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def process_and_display_chat_interaction(user_input, client: OpenAI, assistant):
    """Processes the user input, fetches the assistant's response, and displays both in the chat."""
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id, role="user", content=user_input
    )

    with client.beta.threads.runs.create_and_stream(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant.id,
        model=Config.OPENAI_MODEL,
        instructions=Config.INSTRUCTIONS,
        # event_handler=EventHandler(streamlit),
    ) as stream:
        with st.chat_message("assistant"):
            response = st.write_stream(stream.text_deltas)
            stream.until_done()

    st.session_state.messages.append({"role": "assistant", "content": response})

# Main
if __name__ == "__main__":
    client, assistant = initialize_openai_client()
    # models = client.models.list()
    # for model in models:
    #     print(model)
    setup_streamlit_ui()
    initialize_chat_variables()
    handle_chat_interaction(client, assistant)