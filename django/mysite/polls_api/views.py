from polls.models import Question
from polls_api.serializers import QuestionSerializer
from rest_framework import generics

# generics 클래스의 ListCreateAPIView 상속
# get, post 기능이 구현되어 있음
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

# generics 클래스의 RetrieveUpdateDestroyAPIView 상속
# get, put, delete 기능이 구현되어 있음.
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer