from django.db import models


# Create your models here.

class Forks(models.Model):
    name_forks = models.CharField(max_length=255, verbose_name="Имя разветления")
    about_forks = models.TextField(max_length=255, verbose_name="Описания развлетвения")
    path_forks = models.SlugField(max_length=255, verbose_name="Адрес развлетвения")

    class Meta:
        verbose_name_plural = "Развлетвения"
        verbose_name = "Развлетение"

    def __str__(self):
        return self.name_forks
