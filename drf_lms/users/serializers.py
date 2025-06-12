from rest_framework import serializers
from .models import CustomUser, Payment
from materials.serializers import CourseSerializer, LessonSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'phone', 'city', 'avatar')


class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'payment_date',
            'course', 'lesson',
            'amount', 'payment_method'
        ]