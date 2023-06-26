from django.contrib import admin
from .models import Chat
from .models import Message
from .models import Answer
from .models import Vote

# Register your models here.

admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Answer)
admin.site.register(Vote)