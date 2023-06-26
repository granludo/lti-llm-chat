from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('form_new_chat', views.form_chat, name = 'form_chat'),
    path('create_chat', views.create_chat, name = 'create_chat'),
    path('chat/<int:chat_id>', views.chat_detail, name = 'chat_detail'),
    path('create_message', views.create_message, name = 'create_message'),
    path('like_message/<int:message_id>', views.like_message, name = 'like_message'),
    path('dislike_message/<int:message_id>', views.dislike_message, name = 'dislike_message'),

    path('launch', views.launch, name = 'launch')
]