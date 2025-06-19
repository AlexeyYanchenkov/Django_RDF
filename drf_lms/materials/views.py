from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .permissions import IsModerator, IsOwner
from rest_framework import generics, permissions, status
from .paginators import StandardResultsSetPagination
from rest_framework.response import Response
from rest_framework.decorators import action


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



