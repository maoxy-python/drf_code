from django.conf.urls import url
from django.urls import path
from django.views.static import serve

from drf_code import settings
from seria import views

urlpatterns = [
    path("emp/", views.EmployeeAPIVIew.as_view()),
    path("emp/<str:pk>/", views.EmployeeAPIVIew.as_view()),
]
