from django.urls import path

from elitemassistent import views

urlpatterns = [
    path('/', views.HomePage.as_view(), name='homepage'),
    path('/send/', views.BindWithAssistant.as_view(), name='sendtext'),
    path('/api', views.service, name='apiServicesUser')
]