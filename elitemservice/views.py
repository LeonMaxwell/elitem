from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView


from elitemservice.serializers import ServiceSerializer
from elservicecollection.models import Service


class GetServiceList(APIView):
    def get(self, request):
        service = Service.objects.all()
        serialized = ServiceSerializer(service, many=True)
        return Response({'Services': serialized.data})


def homepage(request):
    return render(request, 'elitemservice/main.html')
