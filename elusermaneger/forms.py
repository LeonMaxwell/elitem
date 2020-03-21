from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ElBaseUser


class ElUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = ElBaseUser
        fields = ('email', 'password',)


class ElUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = ElBaseUser
        fields = ('email', 'password',)
