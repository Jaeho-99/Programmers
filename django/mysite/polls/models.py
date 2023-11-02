from django.db import models

from django.utils import timezone
import datetime
from django.contrib import admin

class Question(models.Model):
    # verbose_name 옵션에 필드의 칼럼명 입력
    question_text = models.CharField(max_length=200, verbose_name="질문") # 텍스트를 저장하는 필드
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="생성일") # 날짜를 저장하는 필드

    # @admin.display 어노테이션으로 함수의 칼럼명 입력 
    @admin.display(boolean=True, description='최근생성(하루기준)')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        if self.was_published_recently():
            new_badge = "New!!!"
        else:
            new_badge = ''
        return f'{new_badge} 제목: {self.question_text}, 날짜: {self.pub_date}'
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # 외래키 Question을 CASCADE로 참조한다.
    choice_text = models.CharField(max_length=200) # 텍스트를 저장하는 필드
    votes = models.IntegerField(default=0) # 숫자를 저장하는 필드
    def __str__(self):
        return f'[{self.question.question_text}]{self.choice_text}'