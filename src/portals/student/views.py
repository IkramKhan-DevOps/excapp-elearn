
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from src.accounts.decorators import student_required


User = get_user_model()

student_required = [login_required, student_required]
student_nocache_decorators = [login_required, student_required, never_cache]

"""  VIEWS ================================================================================= """


class DashboardView(TemplateView):
    template_name = 'student/dashboard.html'
