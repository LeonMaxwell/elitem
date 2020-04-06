from django import forms

from elservicecollection.models import Service


class AddServiceForm(forms.ModelForm):
    name_service = forms.CharField(max_length=255, label="Имя сервиса")
    about_service = forms.CharField(widget=forms.Textarea, label='Описание сервиса')
    file_service = forms.FileField(label='Файл сервиса')

    class Meta:
        model = Service
        fields = '__all__'
