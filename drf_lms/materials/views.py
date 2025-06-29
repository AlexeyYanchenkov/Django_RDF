from datetime import timedelta
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from users.models import Payment
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .permissions import IsModerator, IsOwner
from rest_framework import generics, permissions, status
from .paginators import StandardResultsSetPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from services.stripe import create_stripe_product, create_stripe_price, create_stripe_session
from .tasks import send_course_update_email


class CreateStripePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Курс не найден"}, status=404)

        # Создаём продукт
        product_id = create_stripe_product(course.name)

        # Создаём цену
        price_id = create_stripe_price(product_id, float(course.price))

        # Создаём платёжную сессию
        success_url = "http://localhost:8000/success/"
        cancel_url = "http://localhost:8000/cancel/"
        session_url = create_stripe_session(price_id, success_url, cancel_url)

        # Сохраняем платёж
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            payment_method='card',
            stripe_session_url=session_url
        )

        return Response({
            "payment_id": payment.id,
            "stripe_url": session_url
        })


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsModerator() | IsOwner()]
        elif self.request.method in ['POST', 'DELETE']:
            return [IsOwner()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        course = self.get_object()
        Subscription.objects.get_or_create(user=request.user, course=course)
        return Response({'status': 'subscribed'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])

    def unsubscribe(self, request, pk=None):
        course = self.get_object()
        Subscription.objects.filter(user=request.user, course=course).delete()
        return Response({'status': 'unsubscribed'}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, send_course_update_email=None, *args, **kwargs):
        course = self.get_object()
        last_updated = course.updated_at

        response = super().update(request, *args, **kwargs)

        if now() - last_updated > timedelta(hours=4):
            subscriptions = Subscription.objects.filter(course=course)
            for sub in subscriptions:
                user_email = sub.user.email
                send_course_update_email.delay(user_email, course.title)

class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsModerator() | IsOwner()]
        elif self.request.method in ['POST', 'DELETE']:
            return [IsOwner()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
