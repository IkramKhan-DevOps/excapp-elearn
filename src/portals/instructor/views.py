
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, ListView, DetailView,UpdateView, CreateView, DeleteView

from src.portals.admins.models import Course, Enroll

User = get_user_model()

customer_decorators = [login_required]
customer_nocache_decorators = [login_required, never_cache]

"""  VIEWS ================================================================================= """


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
    fields = ['name', 'section', 'subject', 'room', 'description']
    template_name = 'instructor/course_form.html'

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super(CourseCreateView, self).form_valid(form)


class CourseUpdateView(UpdateView):
    model = Course
    fields = ['name', 'section', 'subject', 'room', 'description']
    template_name = 'instructor/course_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Course.objects.filter(instructor=self.request.user), pk=self.kwargs['pk'])


class EnrollListView(ListView):
    model = Enroll
    fields = '__all__'
    template_name = 'instructor/enroll_list.html'

    def get_queryset(self):
        return Enroll.objects.filter(course__instructor=self.request.user, course=self.kwargs['course'], is_active=True, is_banned=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EnrollListView, self).get_context_data(**kwargs)
        context['enroll_ban'] = Enroll.objects.filter(course__instructor=self.request.user, course=self.kwargs['course'], is_active=True, is_banned=True)
        context['enroll_inactive'] = Enroll.objects.filter(course__instructor=self.request.user, course=self.kwargs['course'], is_active=False)
        return context


