from django.urls import path

from elitemservice import views


urlpatterns = [
    path('', views.homepage),
    path('login/', views.Logid.as_view(), name='login'),
    path('api/', views.GetServiceList.as_view(), name='apiServices'),
]