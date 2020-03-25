from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView

from rest_framework.response import Response
from rest_framework.views import APIView

from elitemservice.forms import LoginUser, RegisterUser
from elitemservice.serializers import ServiceSerializer
from elservicecollection.models import Service
from elusermaneger.models import ElBaseUser


class GetServiceList(APIView):

    def get(self, request):
        service = Service.objects.all()
        serialized = ServiceSerializer(service, many=True)
        return Response({'Services': serialized.data})


class Login(FormView):
    template_name = 'elitemservice/forms/login.html'
    form_class = LoginUser

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class, 'act' : 'login'})

    def post(self, request, *args, **kwargs):
        form = LoginUser(request.POST)
        email = form['email'].data
        password = form['password'].data
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'elitemservice/forms/login.html')
            else:
                return render(request, 'elitemservice/forms/login.html')
        else:
            return render(request, 'elitemservice/forms/login.html')


class LogOut(LogoutView):
    template_name = 'elitemservice/main.html'


class Register(CreateView):
    model = ElBaseUser
    template_name = 'elitemservice/forms/login.html'
    form_class = RegisterUser
    success_url = reverse_lazy('homepage')

    def post(self, request, *args, **kwargs):
        user_form = RegisterUser(request.POST)
        logb = user_form['login'].data
        email = user_form['email'].data
        password = user_form['password1'].data
        password_confirm = user_form['password2'].data
        if password == password_confirm:
            ElBaseUser.objects.create_user(email, password, logb)
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'elitemservice/forms/login.html')
                else:
                    return render(request, 'elitemservice/forms/login.html')
            else:
                return render(request, 'elitemservice/forms/login.html')


class HomePage(TemplateView):
    template_name = 'elitemservice/main.html'