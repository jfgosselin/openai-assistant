# Private OpenAI Assistant GTP 

Quickly build a chat web app using the [OpenAI Assistant](https://platform.openai.com/docs/assistants/overview?context=with-streaming) API and Streamlit.

## Usage

- Head to https://platform.openai.com/assistants and create your Assistant.
- Edit the [.env](.env) file with your OpenAI API key, OpenAI Assistant key, prompts, logo, disclaimer, etc.

```plaintext
## OpenAI Configuration ##

# Your OpenAI API key https://platform.openai.com/api-keys 
API_KEY=sk-...
# Your OpenAI Assistant key (You need to create a GPT Assistant first)
ASSISTANT_KEY=asst_...
# Model name https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo
OPENAI_MODEL="gpt-4-turbo-preview"
# Use the instructions parameter to guide the personality of the Assistant and define its goals.
# https://platform.openai.com/docs/assistants/how-it-works/objects
INSTRUCTIONS=""

## Streamlit Configuration ##
PAGE_TITLE="My Page Title"
WELCOME_MESSAGE="Hello, I'm your Assistant. How can I help you?"
USER_PROMPT="What's your question?"
BEGIN_MESSAGE="Click 'Start Chat' to begin."
EXIT_MESSAGE="Exit Assistant"
START_CHAT_BUTTON="Start Chat"
DISCLAIMER="disclaimer.md"
LOGO="logo.png"
```

- Build the docker image:

```bash
./build_image.sh
```

- Run it:

```bash
docker-compose up -d 
```

- You should be able to access your application at http://localhost:8555.

If you want to quickly expose it to your family, friends, or colleagues, you can use [ngrok](https://ngrok.com/).



