from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from elusermaneger.forms import ElUserCreateForm, ElUserChangeForm
from elusermaneger.models import ElBaseUser

admin.site.unregister(Group)


# Register your models here.

class ElUserAdmin(UserAdmin):
    add_form = ElUserCreateForm
    form = ElUserChangeForm
    model = ElBaseUser
    list_display = ('email', 'is_staff', 'is_active', 'login')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('login', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Settings Service', {'fields': ('loads_services',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('loads_services',)


admin.site.register(ElBaseUser, ElUserAdmin)
