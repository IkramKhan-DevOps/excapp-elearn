from django.urls import path
from .views import (
    DashboardView, CourseUpdateView, CourseDetailView, CourseCreateView, CourseListView,
    EnrollListView, CourseDeleteView, CourseCodeChange
)

app_name = "instructor"
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('course/', CourseListView.as_view(), name='course'),
    path('course/add/', CourseCreateView.as_view(), name='course-add'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
    path('course/<int:pk>/code/change/', CourseCodeChange.as_view(), name='course-code-change'),

    path('course/<int:course>/members/', EnrollListView.as_view(), name='enroll-list')

]
