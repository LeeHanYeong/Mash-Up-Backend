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
            'username',
            'name',
            'email',
            'phone_number',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.username:
            user.username = self.cleaned_data['email']
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
                    Q(pk__in=self.cleaned_data['groups'].values_list('pk', flat=True)) |
                    Q(pk=group.pk),
                )
        else:
            if group in self.cleaned_data['groups']:
                self.cleaned_data['groups'] = self.cleaned_data['groups'].exclude(pk=group.pk)
        return super().save(*args, **kwargs)
