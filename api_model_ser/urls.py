from django.urls import path

from api_model_ser import views

urlpatterns = [
    path("books/", views.BookAPIView.as_view()),
    path("books/<str:id>/", views.BookAPIView.as_view()),

    path("press/", views.PressAPIView.as_view()),
    path("press/<str:id>/", views.PressAPIView.as_view()),

    path("v2/books/", views.BookAPIView2.as_view()),
    path("v2/books/<str:id>/", views.BookAPIView2.as_view()),

    path("gen/books/", views.GenericAPIView.as_view()),
    path("gen/books/<str:id>/", views.GenericAPIView.as_view()),
]
