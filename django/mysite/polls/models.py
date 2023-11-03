from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="질문") # 텍스트를 저장하는 필드
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="생성일") # 날짜를 저장하는 필드
    owner = models.ForeignKey('auth.User', related_name='questions', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE) # 외래키 Question을 CASCADE로 참조한다.
    choice_text = models.CharField(max_length=200) 
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
# Vote 기능의 모델 클래스 정의
class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # 한 질문 당 한 번의 투표만 가능하도록 제약 조건을 걺.
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'voter'], name='unique_voter_for_questions')
        ]