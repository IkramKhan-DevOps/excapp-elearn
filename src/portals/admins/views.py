from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DetailView
)

from src.portals.admins.models import Course

admin_decorators = [login_required, user_passes_test(lambda u: u.is_superuser)]
admin_nocache_decorators = [login_required, user_passes_test(lambda u: u.is_superuser), never_cache]


"""  INIT ------------------------------------------------------------------------- """


class DashboardView(TemplateView):
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


class CourseListView(ListView):
    queryset = Course.objects.all()


class CourseDetailView(DetailView):
    model = Course


class CourseCreateView(CreateView):
    model = Course
    fields = ['name', 'section', 'subject', 'instructor', 'room', 'description']


class CourseUpdateView(UpdateView):
    model = Course
    fields = ['name', 'section', 'subject', 'instructor', 'room', 'description']
