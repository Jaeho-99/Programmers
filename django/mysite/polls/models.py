from django.db import models

from django.utils import timezone
import datetime
from django.contrib import admin

class Question(models.Model):
    # verbose_name 옵션에 필드의 칼럼명 입력
    question_text = models.CharField(max_length=200, verbose_name="질문") # 텍스트를 저장하는 필드
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="생성일") # 날짜를 저장하는 필드
    # 해당 질문의 owner를 정의.
    # owner가 삭제되면 Qeustion은 모두 delete(CASCADE)되며,
    # 필드가 비어 있어도(null) 괜찮다는 의미.
    # 유저의 Question을 불러올 때, realated_name인 'questions'로 가져옴.
    owner = models.ForeignKey('auth.User', related_name='questions', on_delete=models.CASCADE, null=True)

    # @admin.display 어노테이션으로 함수의 칼럼명 입력 
    @admin.display(boolean=True, description='최근생성(하루기준)')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # 외래키 Question을 CASCADE로 참조한다.
    choice_text = models.CharField(max_length=200) # 텍스트를 저장하는 필드
    votes = models.IntegerField(default=0) # 숫자를 저장하는 필드
    def __str__(self):
        return self.choice_text