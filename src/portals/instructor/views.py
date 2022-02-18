
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, ListView, DetailView,UpdateView, CreateView, DeleteView

from src.accounts.decorators import customer_required
from src.portals.admins.models import Course

User = get_user_model()

customer_decorators = [login_required, customer_required]
customer_nocache_decorators = [login_required, customer_required, never_cache]

"""  VIEWS ================================================================================= """


@method_decorator(customer_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'instructor/dashboard.html'


class CourseListView(ListView):
    queryset = Course.objects.all()
    template_name = 'instructor/course_list.html'

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)


class CourseDetailView(DetailView):
    model = Course
    template_name = 'instructor/course_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Course.objects.filter(instructor=self.request.user), pk=self.kwargs['pk'])


class CourseCreateView(CreateView):
    model = Course
    fields = ['name', 'section', 'subject', 'instructor', 'room', 'description']
    template_name = 'instructor/course_form.html'

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super(CourseCreateView, self).form_valid(form)


class CourseUpdateView(UpdateView):
    model = Course
    fields = ['name', 'section', 'subject', 'instructor', 'room', 'description']
    template_name = 'instructor/course_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Course.objects.filter(instructor=self.request.user), pk=self.kwargs['pk'])

