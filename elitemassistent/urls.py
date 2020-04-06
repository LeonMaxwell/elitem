from django.urls import path

from elitemassistent import views

urlpatterns = [
    path('/', views.HomePage.as_view(), name='homepage'),
]