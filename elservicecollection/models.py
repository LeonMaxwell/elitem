from django.db import models


# Create your models here.

class Service(models.Model):
    name_service = models.CharField(max_length=255, verbose_name='Назание сервиса')
    about_service = models.TextField(verbose_name='Описание микросервиса')
    file_service = models.FileField(upload_to='upload_microservice', verbose_name='Файл микросервиса')

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return self.name_service