from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from ..forms import UserCreationForm


class UserAdmin(BaseUserAdmin):
    list_display = ('name', 'username', 'email', 'phone_number', 'is_staff')
    search_fields = ('full_name', 'email', 'phone_number',)

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
            )
        }),
        ('개인정보', {
            'fields': (
                'last_name',
                'first_name',
                'email',
                'phone_number',
            )
        }),
        ('권한', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
        ('주요 기록', {
            'fields': (
                'last_login',
                'date_joined',
            )
        })
    )
    readonly_fields = (
        'last_login',
        'date_joined',
    )
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'last_name',
                'first_name',
                'phone_number',
                'email',
                'password1',
                'password2',
            )
        }),
    )
