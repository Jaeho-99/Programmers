from rest_framework import serializers
from polls.models import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
# validator 임포트
from rest_framework.validators import UniqueTogetherValidator

# Vote 모델 시리얼라이저 정의
class VoteSerializer(serializers.ModelSerializer):
    # 특정 질문에만 가능한 Choice인지 판단하는 메서드
    def validate(self, attrs):
        if attrs['choice'].question.id != attrs['question'].id:
            raise serializers.ValidationError("적절하지 않는 Question과 Choice의 조합입니다.")

        return attrs
    
    class Meta:
        model = Vote
        fields = ['id', 'question', 'choice', 'voter']
        # valid한지 체크하는 validator 정의. is_valid를 정의하는 것과 유사(?)
        # 고유한 question과 voter인지 확인. (중복 투표 방어)
        validotrs = [
            UniqueTogetherValidator(
                queryset=Vote.objects.all(),
                fields = ['question', 'voter']
            )
        ]

# Choice에 대한 시리얼라이저 추가
class ChoiceSerializer(serializers.ModelSerializer):
    # method에 의해서 값이 결정되는 votes_count
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ['choice_text', 'votes_count']

    # method 정의
    def get_votes_count(self, obj):
        return obj.vote_set.count()


class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # choices 이라는 Choice시리얼라이저.
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        # fields에 choices 추가
        fields = ['id', 'question_text', 'pub_date', 'owner', 'choices']

class UserSerializer(serializers.ModelSerializer):
    questions = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='question-detail')
    
    class Meta:
        model = User
        fields = ['id', 'username', 'questions']

# 사용자등록 시리얼라이저 정의
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # 패스워드 재확인용
    password2 = serializers.CharField(write_only=True, required=True)
    
    # 패스워드 재확인 메서드
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password' : '두 패스워드가 일치하지 않습니다.'})
        return attrs

    # User에는 password2가 정의되어 있지 않기 때문에 직접 create를 정의해야 함.
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']