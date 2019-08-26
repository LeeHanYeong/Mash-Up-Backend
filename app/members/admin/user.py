from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from ..forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    list_display = ('name', 'username', 'email', 'phone_number', 'is_staff')
    search_fields = ('name', 'email', 'phone_number',)

    readonly_fields = (
        'last_login',
        'date_joined',
    )
    form = UserChangeForm
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name',
                'phone_number',
                'email',
            )
        }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'username',
                    'password',
                )
            }),
            ('개인정보', {
                'fields': (
                    'name',
                    'email',
                    'phone_number',
                    'github',
                )
            }),
            ('권한', {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ) if request.user.is_superuser else (
                    'is_active',
                    'is_staff',
                    'groups',
                )
            }),
            ('주요 기록', {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            })
        )
        return fieldsets
