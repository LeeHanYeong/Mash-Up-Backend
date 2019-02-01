from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

User = get_user_model()


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'last_name',
            'first_name',
            'phone_number',
        )
