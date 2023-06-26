import os
import requests
import json
from dotenv import load_dotenv

import openai

def answer_chatgpt(message):
    load_dotenv()
    openai.api_key = os.environ.get('api_key')

    chat = message.chat
    context = chat.context

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = context,
        temperature = .7,
        max_tokens = 300,
    )

    return response['choices'][0]['message']['content']