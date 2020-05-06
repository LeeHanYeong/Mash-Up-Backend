from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.models import Group
from django.db.models import Q

User = get_user_model()

__all__ = (
    'UserCreationForm',
    'UserChangeForm',
    'LoginForm',
    'PasswordSetForm',
)


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


class LoginForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '이름을 입력해주세요',
        },
    ))
    email = forms.CharField(required=False, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'example@lhy.kr',
        },
    ))
    password = forms.CharField(required=False, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '처음 로그인한다면 비워주세요',
        },
    ))

    def clean(self):
        cleaned_data = super().clean()
        fields = ('name', 'email')
        not_none_fields = {field: cleaned_data[field] for field in fields if bool(cleaned_data[field])}
        try:
            User.objects.get(**not_none_fields)
        except User.DoesNotExist:
            raise forms.ValidationError('해당하는 사용자 정보가 없습니다')
        except User.MultipleObjectsReturned:
            raise forms.ValidationError('해당 정보로 여러 사용자가 검색됩니다. 다른 필드들을 입력해주세요')


class PasswordSetForm(forms.Form):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
        },
    ))
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '위와 같은 비밀번호를 입력해주세요',
        },
    ))

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('비밀번호와 비밀번호 확인의 값이 다릅니다')