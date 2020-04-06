from django.contrib import admin

# Register your models here.
from elhub.models import Forks


@admin.register(Forks)
class ForksAdmin(admin.ModelAdmin):
    list_display = ('name_forks', 'pk', 'path_forks')
    list_filter = ('name_forks',)
    prepopulated_fields = {'path_forks': ('name_forks',)}
    ordering = ('name_forks',)
