from dj_rest_auth.serializers import LoginSerializer as BaseLoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()        # → settings.AUTH_USER_MODEL = "accounts.CustomUser"

class UserSerializer(serializers.ModelSerializer):
    password2   = serializers.CharField(write_only=True)  #비밀번호 확인
    full_name   = serializers.CharField(write_only=True)  #이름 한 칸
    phone_number = serializers.CharField()                #모델 필드 그대로

    class Meta:
        model  = User
        fields = [
            "username",
            "password",
            "password2",
            "full_name",
            "phone_number",
            "email",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    #비밀번호 일치 검사
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "비밀번호가 서로 다릅니다."})
        return attrs

    #실제 사용자 생성
    def create(self, validated_data):
        validated_data.pop("password2")                 #더 이상 필요 없음
        full_name    = validated_data.pop("full_name")  #모델에 직접 저장
        phone_number = validated_data.pop("phone_number")

        user = User.objects.create_user(
            username = validated_data["username"],
            password = validated_data["password"],
            email    = validated_data.get("email", ""),
        )

        #커스텀 필드 채우기
        user.full_name   = full_name
        user.phone_number = phone_number
        user.save()

        return user

#마이페이지 정보수정
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image', 'nickname']

    def update(self, instance, validated_data):
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()
        return instance