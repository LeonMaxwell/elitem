from django.contrib.postgres.fields import ArrayField
from django.db import models


class Service(models.Model):
    name_service = models.CharField(max_length=255, verbose_name='Назание сервиса')
    about_service = models.TextField(verbose_name='Описание микросервиса')
    tags_service = ArrayField(models.CharField(max_length=255), blank=True, verbose_name='Тэги микросервиса')
    possibility = models.FileField(upload_to='upload_microservice', default=None, verbose_name='Файл микросервиса')
    design = models.FileField(upload_to='upload_microservice', verbose_name='Дизайн микросервиса', default='standard')

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return self.name_service