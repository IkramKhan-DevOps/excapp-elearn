from django.db import models
from django.urls import reverse

from src.accounts.models import User


class Course(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    section = models.CharField(max_length=255, null=False, blank=False)
    subject = models.CharField(max_length=255, null=False, blank=False)
    room = models.CharField(max_length=255, null=False, blank=False, help_text="batch name/number or room")
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor', blank=True)
    description = models.TextField()
    students = models.ManyToManyField(User, through='Enroll', related_name='students')

    is_paid = models.BooleanField(default=False, help_text="If instructor paid for the course please check this.")
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['instructor', '-id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('admins:course-detail', args=[self.pk])


class Enroll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses')
    allowed_in_course = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enrollment"
        ordering = ['-course', '-user']

    def __str__(self):
        return f"{self.user.username} in {self.course.name}"
