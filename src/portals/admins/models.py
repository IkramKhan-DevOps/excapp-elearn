import datetime
import uuid

from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField

from src.accounts.models import User


class Course(models.Model):
    thumbnail = ResizedImageField(
        upload_to='instructor/images/courses/', null=True, blank=True, size=[600, 300], quality=75, force_format='PNG',
        help_text='size of logo must be 100*100 and format must be png image file', crop=['middle', 'center']
    )
    name = models.CharField(max_length=255, null=False, blank=False)
    section = models.CharField(max_length=255, null=False, blank=False)
    subject = models.CharField(max_length=255, null=False, blank=False)
    room = models.CharField(max_length=255, null=False, blank=False, help_text="batch name/number or room")
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student', blank=True)
    code = models.UUIDField(
        default=uuid.uuid4, editable=False,
    )
    description = models.TextField(null=True, blank=True)
    students = models.ManyToManyField(User, through='Enroll', related_name='students')

    is_paid = models.BooleanField(default=False, help_text="If student paid for the course please check this.")
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('admins:course-detail', args=[self.pk])


class Enroll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enrollment"
        ordering = ['-course', '-user']

    def __str__(self):
        return f"{self.user.username} in {self.course.name}"


class Assignment(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_assignment')

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Assignments'
        ordering = ['-expires_on']

    def __str__(self):
        return self.name


class AssignmentContent(models.Model):
    url = models.URLField()
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Assignment Contents'
        ordering = ['created_on', '-assignment']

    def __str__(self):
        return self.url
