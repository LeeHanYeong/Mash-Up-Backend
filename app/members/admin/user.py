from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from ..forms import UserCreationForm, UserChangeForm
from ..models import User, Period


class UserAdminProxy(User):
    class Meta:
        proxy = True
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    @property
    def outcount(self):
        try:
            current_period = Period.objects.get(is_current=True)
        except Period.DoesNotExist:
            return '현재 기수정보 없음'
        period_outcount = self.user_period_outcount_set.filter(period=current_period)
        if period_outcount.exists():
            period_outcount = period_outcount.get()
            return f'{period_outcount.count} ({period_outcount.period.number}기)'
        return '해당없음'

    outcount.fget.short_description = '아웃카운트'


@admin.register(User)
@admin.register(UserAdminProxy)
class UserAdminProxyAdmin(BaseUserAdmin):
    list_display = ('name', 'username', 'email', 'phone_number', 'birth_date', 'is_staff')
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

    def get_list_display(self, request):
        if hasattr(self.model, 'outcount'):
            return self.list_display + ('outcount',)
        return self.list_display

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
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
                    'birth_date',
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
