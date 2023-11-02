# Django의 REST 프레임워크에서 시리얼라이저 임포트.
from rest_framework import serializers
from polls.models import Question

# ModelSerializer를 상속받는 경우, 필드 및 메서드가 자동으로 지정됨.
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date']