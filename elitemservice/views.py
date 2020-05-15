import pandas as pd
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, FormView, CreateView
from rest_framework.response import Response
from rest_framework.views import APIView

from elitemservice.forms import LoginUser, RegisterUser
from elitemservice.serializers import ServiceSerializer
from elservicecollection.forms import AddServiceForm
from elservicecollection.models import Service
from elusermaneger.models import ElBaseUser


class GetServiceList(APIView):
    def get(self, request):
        service = Service.objects.all()
        serialized = ServiceSerializer(service, many=True)
        data = serialized.data
        print(pd.DataFrame(pd.json_normalize(data)))
        return Response({'Services': serialized.data})

    def post(self, request):
        id_service = request.POST.get('current_id', None)
        service = Service.objects.all()
        serialized = ServiceSerializer(service, many=True)
        user = request.user
        if user.is_authenticated:
            user.loads_services.add(service.get(pk=id_service))
            user.save()
        context = {'user': user, 'Services': serialized.data}
        return render(request, 'elitemservice/main.html', context)


class AddService(CreateView):
    template_name = 'elitemservice/forms/addservice.html'
    form_class = AddServiceForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})


class DoneAdd(CreateView):
    model = Service
    template_name = 'elitemservice/main.html'
    fields = '__all__'
    success_url = reverse_lazy('homepage')

    method_decorator(csrf_protect)

    def form_valid(self, form):
        resp = super(DoneAdd, self).form_valid(form)
        # после вызова суперметода в self.object находится созданный по форме объект
        user = self.request.user
        model = Service.objects.all()
        if user.is_authenticated:
            user.loads_services.add(model.get(pk=self.object.pk))
            user.save()
        return resp


class DeleteService(CreateView):
    def post(self, request, *args, **kwargs):
        id_service = request.POST.get('current_id', None)
        service = Service.objects.all()
        serialized = ServiceSerializer(service, many=True)
        user = request.user
        if user.is_authenticated:
            user.loads_services.remove(service.get(pk=id_service))
            user.save()
        return render(request, 'elitemservice/main.html')


class Login(FormView):
    template_name = 'elitemservice/forms/login.html'
    form_class = LoginUser

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class, 'act': 'login'})

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
    isEmail = False
    isLogin = False
    model = ElBaseUser
    template_name = 'elitemservice/forms/login.html'
    form_class = RegisterUser
    success_url = reverse_lazy('homepage')

    def check_match(self, email, login):
        model = self.model.objects.all()
        try:
            email_is_find = model.get(email=email)
            self.isEmail = True
        except ObjectDoesNotExist:
            pass
        try:
            login_is_find = model.get(login=login)
            self.isLogin = True
        except ObjectDoesNotExist:
            pass

    def post(self, request, *args, **kwargs):
        self.isEmail = False
        self.isLogin = False
        model = ElBaseUser.objects.all()
        user_form = RegisterUser(request.POST)
        logb = user_form['login'].data
        email = user_form['email'].data
        password = user_form['password1'].data
        password_confirm = user_form['password2'].data
        standart_microservice = ElBaseUser.objects.get(login='el').loads_services.all()
        if password == password_confirm:
            self.check_match(email, logb)
            if self.isEmail:
                return render(request, 'elitemservice/forms/login.html', {'error': 'Данная почта используется',
                                                                          'form': self.form_class})
            elif self.isLogin:
                return render(request, 'elitemservice/forms/login.html', {'error': 'Данный логин используется',
                                                                          'form': self.form_class})
            else:
                ElBaseUser.objects.create_user(email, password, logb)
                user = authenticate(email=email, password=password)
                if user is not None:
                    if user.is_active:
                        for count in range(standart_microservice.count()):
                            user.loads_services.add(standart_microservice[count])
                        login(request, user)
                        return render(request, 'elitemservice/forms/register_done.html')
                    else:
                        return render(request, 'elitemservice/forms/login.html')
                else:
                    return render(request, 'elitemservice/forms/login.html')
        else:
            return render(request, 'elitemservice/forms/login.html', {'error': 'Пароль не совпадает',
                                                                      'form': self.form_class})


class Profile(TemplateView):
    template_name = 'elitemservice/extension/profile.html'
    model = ElBaseUser


class HomePage(TemplateView):
    template_name = 'elitemservice/main.html'
