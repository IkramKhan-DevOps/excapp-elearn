from django.urls import path

from src.portals.admins.views import (
    DashboardView,
    CourseListView, CourseCreateView, CourseUpdateView, CourseDetailView
)

app_name = "admins"
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('course/', CourseListView.as_view(), name='course'),
    path('course/add/', CourseCreateView.as_view(), name='course-add'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
]
