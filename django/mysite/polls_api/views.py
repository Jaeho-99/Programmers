from polls.models import *
from polls_api.serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .permissions import *

# Vote 뷰 정의

class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 특정 유저에 대해서만 쿼리셋을 할 수 있도록 지정.
    def get_queryset(self, *args, **kwargs):
        return Vote.objects.filter(voter=self.request.user)

    # 조상 클래스를 보면 perform_create 이전에 is_valid 메서드가 호출됨.
    # 따라서, create 메서드를 오버라이딩 함.
    def create(self, request, *args, **kwargs):
        new_data = request.data.copy()
        new_data['voter'] = request.user.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsVoter]

    # Update 시 해당 유저의 계정에 대해서만 가능하도록 정의.
    def perform_update(self, serializer):
        serializer.save(voter=self.request.user)

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