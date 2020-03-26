from django.db import models

# Create your models here.

class Quesetion(models.Model):
    question_text = models.CharField(manx_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)