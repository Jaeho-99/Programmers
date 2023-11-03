from polls.models import Question
from polls_api.serializers import *
# 로그아웃된 상태에서 post를 하지 못하도록 막기 위해 permissions 임포트
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly

# generics 클래스의 ListCreateAPIView 상속
# get, post 기능이 구현되어 있음
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # 로그인된 상태에서만 질문 등록이 가능하게 만듦.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # QuestionList 뷰에서 create할 때, owner는 현재 로그인된 user로
    # 지정되어서 create 됨.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# generics 클래스의 RetrieveUpdateDestroyAPIView 상속
# get, put, delete 기능이 구현되어 있음.
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # 로그인된 상태에서만 질문 수정이 가능하게 만듦.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 회원 등록 뷰 클래스 정의
class RegisterUser(generics.CreateAPIView):
    serializer_class = RegisterSerializer