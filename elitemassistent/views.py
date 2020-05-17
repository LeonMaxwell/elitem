# Create your views here.
from importlib import import_module

from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from elitemassistent.core import elnlu
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
    service_starter = False
    specific_service = ''
    assistant_massage = ''
    loc = ''
    result_service = ''

    def get(self, request, *args, **kwargs):

        BindWithAssistant.load_service = list()
        BindWithAssistant.service_starter = False
        BindWithAssistant.specific_service = ''
        BindWithAssistant.assistant_massage = ''
        BindWithAssistant.loc = ''
        BindWithAssistant.result_service = ''

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
        if self.service_starter:
            if textToBots == '/exit ' + self.specific_service:
                BindWithAssistant.service_starter = False
                BindWithAssistant.result_service = ''
                return render(request, 'elassistent/extinsions/close.html',
                              {
                                'close_serive': self.specific_service,
                                'request_user': textToBots
                              })
            else:
                BindWithAssistant.result_service = self.loc.main(textToBots)
                contaxt = {
                    'request_user': textToBots,
                    'name_service': self.specific_service,
                    'service_start': self.service_starter,
                    'response_service': self.result_service,
                }
                return render(request, 'elassistent/extinsions/act.html', contaxt)

        else:
            BindWithAssistant.specific_service = elnlu.main(textToBots, self.load_service)
            if self.specific_service == 'Такого сервиса не существует':
                return render(request, 'elassistent/extinsions/notfound.html', {
                    'request_user': textToBots,
                    'response_service': self.specific_service
                })
            else:
                BindWithAssistant.service_starter = True
                for service in self.load_service:
                    if service['name_service'] == self.specific_service:
                        BindWithAssistant.loc = import_module(service['possibility'][1:].
                                                              replace(".py", "").replace("/", "."))
                        return render(request, 'elassistent/extinsions/found.html',
                                      {
                                          'found_service': self.specific_service,
                                          'request_user': textToBots
                                      })


class HomePage(TemplateView):
    template_name = 'elassistent/main.html'