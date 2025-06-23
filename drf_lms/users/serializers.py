from rest_framework import serializers
from .models import CustomUser, Payment
from materials.serializers import CourseSerializer, LessonSerializer
from django.contrib.auth.password_validation import validate_password

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'phone', 'city', 'avatar')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'payment_date',
            'course', 'lesson',
            'amount', 'payment_method'
        ]
        read_only_fields = ['id', 'user', 'payment_date']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone', 'city', 'avatar']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'phone', 'city', 'avatar']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
