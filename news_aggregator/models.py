from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    class Meta:
        app_label = 'news_aggregator'

    def __str__(self):
        return self.username

class Story(models.Model):
    CATEGORY_CHOICES = [
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivia')
    ]
    
    REGION_CHOICES = [
        ('uk', 'UK'),
        ('eu', 'EU'),
        ('w', 'World')
    ]
    
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=2, choices=REGION_CHOICES)
    author = models.CharField(max_length=64)
    date = models.DateTimeField()
    details = models.CharField(max_length=128)
    unique_key = models.CharField(max_length=64, unique=True)
    
    def __str__(self):
        return self.headline
