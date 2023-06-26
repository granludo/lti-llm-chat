from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from chatgpt.models import Message, Answer
from .chatgpt import answer_chatgpt
import time

voted_questions = []

def verify_message(message_id):
    time.sleep(10)
    message = Message.objects.get(id = message_id)
    if message.likes > message.dislikes:
        new_context = {
            "role": "user",
            "content": message.content
        }
        chat = message.chat
        chat.context.append(new_context)
        chat.save()

        if len(voted_questions) == 0:
            voted_questions.append(message)
            process_question()
        else:
            voted_questions.append(message)
    else:
        message.deleted = True
        message.save()


def process_question():
    while len(voted_questions) > 0:
        message = voted_questions.pop(0)
        answer = answer_chatgpt(message)
        new_answer = Answer.objects.create(message = message, content = answer)
        message.processed = True
        message.save()

        new_context = {
            "role": "assistant",
            "content": answer
        }
        chat = message.chat
        chat.context.append(new_context)
        chat.save()
        
        