from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.models import Group
from django.db.models import Q

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'name',
            'email',
            'phone_number',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True

    def _get_validation_exclusions(self):
        exclude = super()._get_validation_exclusions()
        exclude.append('email')
        return exclude

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        name = self.cleaned_data.get('name')
        if not user.username:
            user.username = email
            if not email:
                user.email = None
                index = 2
                current_name = name
                while User.objects.filter(
                        Q(username=current_name) |
                        Q(name=current_name)).exists():
                    current_name = f'{name}{index}'
                    print(current_name)
                    index += 1
                user.username = current_name
        if commit:
            user.save()
        return user


class UserChangeForm(DjangoUserChangeForm):
    def save(self, *args, **kwargs):
        """
        저장시 is_staff여부에 따라, groups에 운영진 Group포함 여부를 변경
        """
        group = Group.objects.get_or_create(name='운영진')[0]
        if self.cleaned_data['is_staff']:
            if group not in self.cleaned_data['groups']:
                self.cleaned_data['groups'] = Group.objects.filter(
                    Q(id__in=self.cleaned_data['groups'].values_list('id', flat=True)) |
                    Q(id=group.id),
                )
        else:
            if group in self.cleaned_data['groups']:
                self.cleaned_data['groups'] = self.cleaned_data['groups'].exclude(id=group.id)
        return super().save(*args, **kwargs)
