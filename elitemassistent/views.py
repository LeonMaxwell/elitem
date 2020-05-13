# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from elitemassistent.core import elnlu
from elitemservice.forms import LoginUser, RegisterUser
from elitemservice.serializers import ServiceSerializer
from elusermaneger.models import ElBaseUser


@api_view(['GET'])
def service(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            serialized = ServiceSerializer(user.loads_services, many=True)
        else:
            standard_services = ElBaseUser.objects.get(login='el').loads_services.all()
            serialized = ServiceSerializer(standard_services, many=True)
        return Response({'Services': serialized.data})


class BindWithAssistant(CreateView):
    load_service = list()

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serialized = ServiceSerializer(user.loads_services, many=True)
        else:
            standart_services = ElBaseUser.objects.get(login='el').loads_services.all()
            serialized = ServiceSerializer(standart_services, many=True)
        data = serialized.data
        BindWithAssistant.load_service = data
        return render(request, 'elassistent/main.html')

    def post(self, request, *args, **kwargs):
        textToBots = request.POST.get('appeal', None)
        toUser = elnlu.main(textToBots, self.load_service)
        contaxt = {'text': textToBots, 'toUser': toUser}
        return render(request, 'elassistent/extinsions/log.html', contaxt)


class HomePage(TemplateView):
    template_name = 'elassistent/main.html'


class Login(FormView):
    template_name = 'elassistent/intermediate/authorization.html'
    form_class = LoginUser


class Register(CreateView):
    isEmail = False
    isLogin = False
    template_name = 'elassistent/intermediate/authorization.html'
    form_class = RegisterUser
    model = ElBaseUser
    success_url = reverse_lazy('homepage')