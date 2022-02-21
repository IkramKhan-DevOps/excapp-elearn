import datetime
import uuid
from itertools import product

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, ListView, DetailView,UpdateView, CreateView, DeleteView

from src.accounts.decorators import instructor_required
from src.portals.admins.models import Course, Enroll, Assignment

User = get_user_model()

instructor_decorators = [login_required, instructor_required]
instructor_nocache_decorators = [login_required, instructor_required, never_cache]

"""  BASE --------------------------------------------------------------------------------------------------------  """


@method_decorator(instructor_decorators, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'instructor/dashboard.html'


"""  COURSE ------------------------------------------------------------------------------------------------------  """


@method_decorator(instructor_decorators, name='dispatch')
class CourseListView(ListView):
    queryset = Course.objects.all()
    template_name = 'instructor/course_list.html'

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)


@method_decorator(instructor_decorators, name='dispatch')
class CourseDetailView(DetailView):
    model = Course
    template_name = 'instructor/course_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Course.objects.filter(instructor=self.request.user), pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['assignments_count'] = 10
        context['course_count'] = 10
        context['quizzes_count'] = 10
        context['polls_count'] = 10
        context['students'] = self.object.students.all()[:20]
        context['upcoming_events'] = 10

        return context


@method_decorator(instructor_decorators, name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    fields = ['thumbnail', 'name', 'section', 'subject', 'room', 'description']
    template_name = 'instructor/course_form.html'

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super(CourseCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('instructor:course-detail', args=(self.object.id,))


@method_decorator(instructor_decorators, name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    fields = ['thumbnail', 'name', 'section', 'subject', 'room', 'description']
    template_name = 'instructor/course_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Course.objects.filter(instructor=self.request.user), pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('instructor:course-detail', args=(self.object.id,))


@method_decorator(instructor_decorators, name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'instructor/course_delete.html'
    success_url = reverse_lazy('instructor:course')

    def get_object(self, queryset=None):
        return get_object_or_404(Course.objects.filter(instructor=self.request.user), pk=self.kwargs['pk'])


@method_decorator(instructor_decorators, name='dispatch')
class CourseCodeChange(View):

    def get(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course.objects.filter(instructor=self.request.user), pk=pk)
        course.code = uuid.uuid4()
        course.save()
        messages.success(request, "Course Join Code changed successfully")
        return redirect('instructor:course-detail', course.pk)


@method_decorator(instructor_decorators, name='dispatch')
class EnrollListView(ListView):
    model = Enroll
    fields = '__all__'
    template_name = 'instructor/enroll_list.html'

    def get_queryset(self):
        return Enroll.objects.filter(course__instructor=self.request.user, course=self.kwargs['course'], is_active=True, is_banned=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EnrollListView, self).get_context_data(**kwargs)
        context['enroll_ban'] = Enroll.objects.filter(
            course__instructor=self.request.user, course=self.kwargs['course'], is_active=True, is_banned=True
        )
        context['enroll_inactive'] = Enroll.objects.filter(
            course__instructor=self.request.user, course=self.kwargs['course'], is_active=False
        )
        return context


"""  ASSIGNMENT --------------------------------------------------------------------------------------------------  """


@method_decorator(instructor_decorators, name='dispatch')
class AssignmentListView(ListView):
    template_name = 'instructor/assignment_list.html'

    def get_queryset(self):
        return Assignment.objects.filter(course__instructor=self.request.user, expires_on__gte=datetime.datetime.now())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssignmentListView, self).get_context_data(**kwargs)
        context['assignments_expired'] = Assignment.objects.filter(
            course__instructor=self.request.user, expires_on__lt=datetime.datetime.now()
        )
        context['course_id'] = self.kwargs['course']
        return context


@method_decorator(instructor_decorators, name='dispatch')
class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'instructor/assignment_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Assignment.objects.filter(course__instructor=self.request.user), pk=self.kwargs['pk'])


@method_decorator(instructor_decorators, name='dispatch')
class AssignmentUpdateView(UpdateView):
    model = Assignment
    fields = ['name', 'description', 'expires_on']
    template_name = 'instructor/assignment_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Assignment.objects.filter(course__instructor=self.request.user), pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy(
            'instructor:assigment-detail', args=(self.kwargs['course'], self.object.pk)
        )


@method_decorator(instructor_decorators, name='dispatch')
class AssignmentCreateView(CreateView):
    model = Assignment
    fields = ['name', 'description', 'expires_on']
    template_name = 'instructor/assignment_form.html'

    def form_valid(self, form):
        form.instance.course = Course.objects.get(pk=self.kwargs['course'])
        return super(AssignmentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'instructor:assigment-detail', args=(self.kwargs['course'], self.object.pk)
        )


@method_decorator(instructor_decorators, name='dispatch')
class AssignmentDeleteView(DeleteView):
    model = Assignment
    template_name = 'instructor/assignment_delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Assignment.objects.filter(course__instructor=self.request.user), pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('instructor:assigment-list', args=(self.kwargs['course'],))
