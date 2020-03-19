from django.urls import path

from elitemservice import views


urlpatterns = [
    path('', views.homepage),
    path('api/', views.GetServiceList.as_view(), name='apiServices'),
]