from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Chat, Message, Vote, Answer
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages

from lti import ToolConfig, ToolConsumer
from lti.contrib.django import DjangoToolProvider
from oauthlib.oauth1 import RequestValidator

from chatgpt.utils.chatgpt import answer_chatgpt
from chatgpt.utils.tasks import verify_message

import threading

# Create your views here.

def index(request):
    chats = Chat.objects.all()
    if not request.user.is_authenticated:
        return redirect('/admin')

    else:
        return render(request, 'chatgpt/index.html', {'chats': chats})


def form_chat(request):
    context = {}
    return render(request, 'chatgpt/create_chat.html', context)


def create_chat(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        user = request.user
        new_chat = Chat.objects.create(user=user, title=title)
        messages.success(request, f"Chat {title} created")
        return redirect('index')

    return render(request, 'chatgpt/create_chat.html')


def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id = chat_id)
    messages = Message.objects.filter(chat = chat)
    votes = Vote.objects.filter(user = request.user)
    answers = Answer.objects.all()
    context = {
        'chat': chat,
        'messages': messages,
        'votes': votes,
        'answers': answers
    }

    return render(request, 'chatgpt/chat.html', context)


def create_message(request):
    chat_id = request.POST.get('chat_id')
    if request.method == 'POST':
        content = request.POST.get('content')
        question = request.POST.get('checkbox')
        if question == '1':
            question = True
        else:
            question = False

        if content:
            chat = get_object_or_404(Chat, id = chat_id)
            new_message = Message.objects.create(chat = chat,
                                                sender = request.user,
                                                content = content,
                                                is_question = question,
                                                processed = False,
                                                deleted = False,
                                                likes = 0,
                                                dislikes = 0)
            messages.success(request, f"Message created")

        if question:
            thread = threading.Thread(target=verify_message, args=(new_message.id,))
            thread.start()

    return redirect('chat_detail', chat_id=chat_id)


def create_answer(message):
    answer = answer_chatgpt(content)
    new_answer = Answer.objects.create(message = message, content = answer)
    messages.success(request, f"Answer created")

    return redirect('chat_detail', chat_id=message.chat.id)


def like_message(request, message_id):
    message = get_object_or_404(Message, id = message_id)
    user = request.user
    vote_exists = Vote.objects.filter(user = user, message = message).exists()
    if vote_exists:
        vote = Vote.objects.get(user = user, message = message)
        if vote.vote == False:
            vote.vote = True
            vote.save()
            message.dislikes -= 1
            message.likes += 1
            message.save()
    else:
        new_vote = Vote.objects.create(user = user, message = message, vote = True)
        message.likes += 1
        message.save()

    return redirect('chat_detail', chat_id=message.chat.id)


def dislike_message(request, message_id):
    message = get_object_or_404(Message, id = message_id)
    user = request.user
    vote_exists = Vote.objects.filter(user = user, message = message).exists()
    if vote_exists:
        vote = Vote.objects.get(user = user, message = message)
        if vote.vote == True:
            vote.vote = False
            vote.save()
            message.likes -= 1
            message.dislikes += 1
            message.save()
    else:
        new_vote = Vote.objects.create(user = user, message = message, vote = False)
        message.dislikes += 1
        message.save()

    return redirect('chat_detail', chat_id=message.chat.id)


class MyRequestValidator(RequestValidator):
    def validate_client_key(self, request):
        return True


@csrf_exempt
def launch(request):
    if request.method == 'POST':
        lti_params = request.POST.dict()

        tool_config = ToolConfig(
            title='ChatGPT a Moodle',
            launch_url='http://127.0.0.1:8000/launch',
            secure_launch_url='http://127.0.0.1:8000/launch'
        )

        tool_provider = DjangoToolProvider.from_django_request(tool_config, request)
        validator = MyRequestValidator()
        #if not tool_provider.is_valid_request(validator):
            #return HttpResponse('Invalid LTI request', status=400)
        
        username = lti_params.get('user_id')
        user, created = User.objects.get_or_create(username=username)

        if created:
            email = lti_params.get('lis_person_contact_email_primary')
            first_name = lti_params.get('lis_person_name_given')
            last_name = lti_params.get('lis_person_name_family')
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        
        login(request, user)

        return redirect('index')