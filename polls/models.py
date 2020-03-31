from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
"""
    CharField: 문자 필드
    DateTimeField: 날짜와 시간(datetime)
"""
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
    
"""
    makemigrations를 실행해서, 도델을 변경시킨 사실과 이 변경사항을 
    migration으로 저장시키고 싶다는 것을 Django에게 알려준다.

    모델의 바꾸는 법
    1. models.py에서 모델을 변경
    2. python3 manage.py makemigrations를 통해 변경사항에 대한 migration생성
    3. python3 manage.py migrate 명령을 통해 변경사항을 데이터베이스에 적용
"""