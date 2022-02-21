from django.contrib import admin
from .models import (
   Enroll, Course, Assignment, AssignmentContent
)


admin.site.register(Enroll)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(AssignmentContent)


