from django.urls import path

from elhub import views

urlpatterns = [
    path('', views.el_hub, name='Hub')
]