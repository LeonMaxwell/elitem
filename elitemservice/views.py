from django.contrib.auth import authenticate, login
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, FormView

from rest_framework.response import Response
from rest_framework.views import APIView

from elitemservice.forms import LoginUser
from elitemservice.serializers import ServiceSerializer
from elservicecollection.models import Service


class GetServiceList(APIView):

    def get(self, request):
        service = Service.objects.all()
        serialized = ServiceSerializer(service, many=True)
        return Response({'Services': serialized.data})


class Login(FormView):
    template_name = 'elitemservice/forms/login.html'
    model = Service
    form_class = LoginUser

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

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


class HomePage(TemplateView):
    template_name = 'elitemservice/main.html'