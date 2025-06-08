from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='courses/', null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to='lessons/', null=True, blank=True)
    video_link = models.URLField()

    def __str__(self):
        return f"{self.title} ({self.course.title})"