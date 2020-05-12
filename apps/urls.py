from django.urls import path

from apps import views

urlpatterns = [
    path("student/", views.StudentView.as_view()),
    path("student/<str:pk>/", views.StudentView.as_view()),
    path("users/", views.UserView.as_view()),
]
