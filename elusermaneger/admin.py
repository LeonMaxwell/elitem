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
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(ElBaseUser, ElUserAdmin)
