# Django의 REST 프레임워크에서 시리얼라이저 임포트.
from rest_framework import serializers
from polls.models import Question
# User 모델 임포트
from django.contrib.auth.models import User
# 간단한 패스워드 가입에 대한 처리를 위해 임포트
from django.contrib.auth.password_validation import validate_password

# ModelSerializer를 상속받는 경우, 필드 및 메서드가 자동으로 지정됨.
class QuestionSerializer(serializers.ModelSerializer):
    # 사용자의 이름으로 읽어서 해당 owner를 read only로 갖고 옴.
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'owner']

class UserSerializer(serializers.ModelSerializer):
    # User 모델의 Primary Key 값으로 연결된 모든 Question 모델의 오브젝트들을 가져옴
    questions = serializers.StringRelatedField(many=True, read_only=True)

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