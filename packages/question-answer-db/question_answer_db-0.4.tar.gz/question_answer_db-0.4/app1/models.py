from django.db import models

class ChatSession(models.Model):
    user_name = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()
