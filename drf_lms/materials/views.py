from rest_framework.viewsets import ModelViewSet
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework import generics


# ViewSet для курсов
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# Generic-представление для списка и создания уроков
class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

# Generic-представление для получения, редактирования и удаления урока
class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer