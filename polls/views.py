from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Question

# Create your views here.

'''
index(request)
polls/index.html 템플릿을 불러온 후 , context에 전달

render(request, template_name, context_dict)
template에 context를 채워넣어 표현한 결과를 HttpResponse 객체와 함께 돌려주는 구문
input: 
    request: request 객체
    template_name: 템플릿 이름
    context_dict: context 사전형 객체를 선책적으로 받는다.

output:
    context로 표현된 HttpResponse 객체
'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list,} # dictionary

    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    '''
    get_object_or_404(): Django 모델을 첫번째 인자로 받고, 몇개의 키워드 인수를 모델 관리자의 get() 함수에 넘긴다.
    객체가 존재하지 않을경우 Http404 에러
    '''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s"
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s" % question_id)