from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Word(models.Model):
    CATEGORY_CHOICES = [
        ('Greetings', 'Greetings'),
        ('Daily Activities', 'Daily Activities'),
        ('Emotions', 'Emotions'),
        ('Feelings', 'Feelings'),
    ]
    LEVEL_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    language = models.CharField(max_length=100, choices=[('Twi', 'Twi'), ('Yoruba', 'Yoruba')])
    english_word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    level = models.CharField(max_length=100, choices=LEVEL_CHOICES)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f'{self.english_word} ({self.language})'

class UserAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Attempt by {self.user} on {self.word}'
