FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt *.png *.md .env openai_assistant.py  /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "openai_assistant.py"]