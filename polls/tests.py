import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question
# Create your tests here.

def create_question(question_text, days):
        '''
        question_text를 가지고 현제 시간에 days를 더한 question을 만든다.
        '''
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        '''
        was_published_recently()는 미래 시점일 때 False 반환
        '''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_questions(self):
        '''
        was_published_recently()은 하루보다 더 작으면 False
        '''
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        '''
        was_published_recently() 날짜가 같으면 True
        '''
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        '''
        question이 없으면 에러 메세지
        '''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        '''
        과거 질문을 index 페이지에 출력
        '''
        create_question(question_text="Past qeustion.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_future_question(self):
        '''
        미래 질문을 index 페이지에 출력
        '''        
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

        def test_future_question_and_past_question(self):
            '''
            과거와 미래 시점의 질문이 있을 때 과거 시점만 출력
            '''
            create_question(question_text="Past question.", days=-30)
            create_question(question_text="Futre question.", days=30)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

        def test_two_past_question(self):
            '''
            index 페이지는 여러 질문을 출력 
            '''
            create_question(question_text='Past question 1.', days=-30)
            create_question(question_text='Past question 2.', dyas=-5)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question 2.>', '<Question: Past question 1.>'])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        '''
        show 404 page if question is in future
        '''
        future_quesion = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_quesion.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        '''
        show question's text if question is in past
        '''
        past_question = create_question(question_text='Past question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
