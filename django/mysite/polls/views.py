from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F
# generic 뷰 모델 임포트
from django.views import generic
# url을 생성하는 revese_lazy 메서드 임포트
from django.urls import reverse_lazy
# 유저생성폼 임포트
from django.contrib.auth.forms import UserCreationForm

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'questions' : latest_question_list}
	return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': f"선택이 없습니다. id={request.POST['choice']}"})
    else:
        # F : DB에서 읽는다는 의미.
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))
    
def result(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/result.html', {'question' : question})

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    # 해당 경로의 이름으로 url을 가져옴.
    success_url = reverse_lazy('user-list')
    template_name = 'registration/signup.html'