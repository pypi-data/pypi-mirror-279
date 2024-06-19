from django.contrib import admin
from .models import ChatSession,SimilarQuestion

admin.site.register(ChatSession),
admin.site.register(SimilarQuestion)

