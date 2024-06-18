# from django.db import models

# class User(models.Model):
#     username = models.CharField(max_length=100, unique=True)

# from django.db import models

# class ChatSession(models.Model):
#     user_name = models.CharField(max_length=255)
#     session_id = models.CharField(max_length=255)
#     question = models.TextField()
#     answer = models.TextField()


# class SimilarQuestion(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     data = models.JSONField()  # Updated to use the new JSONField






from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)

from django.db import models

class ChatSession(models.Model):
    user_name = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()


class SimilarQuestion(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    
    session_id = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()











