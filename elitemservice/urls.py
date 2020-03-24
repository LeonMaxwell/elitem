from django.urls import path

from elitemservice import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('api/', views.GetServiceList.as_view(), name='apiServices'),
]