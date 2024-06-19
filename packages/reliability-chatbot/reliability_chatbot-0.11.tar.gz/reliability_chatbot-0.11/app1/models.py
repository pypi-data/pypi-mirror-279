
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)

from django.db import models

class ChatSession(models.Model):
    user_name = models.CharField(max_length=255)
    # session_id = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()


class SimilarQuestion(models.Model):
    user_name = models.CharField(max_length=255)
    # session_id = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()


from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)

from django.db import models

class ChatSession(models.Model):
    user_name = models.CharField(max_length=255)
    # session_id = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()


class SimilarQuestion(models.Model):
    user_name = models.CharField(max_length=255)
    # session_id = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()


class Feedback(models.Model):
    # user_name = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()
    feedback = models.BooleanField()  # This should be a BooleanField

    def __str__(self):
        return f"  {'Positive' if self.feedback else 'Negative'}"








