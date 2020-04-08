# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView

from elitemassistent.core import elnlu


class BindWithAssistant(CreateView):
    def post(self, request, *args, **kwargs):
        toUser = ''
        textToBots = request.POST.get('appeal', None)
        toUser = elnlu.main(textToBots)
        contaxt = {'text': textToBots, 'toUser': toUser}
        return render(request, 'elassistent/extinsions/log.html', contaxt)


class HomePage(TemplateView):
    template_name = 'elassistent/main.html'