from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, TemplateView

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


class Login(CreateView):
    template_name = 'elitemservice/forms/login.html'
    model = Service

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'forms': LoginUser()})


class HomePage(TemplateView):
    template_name = 'elitemservice/main.html'
