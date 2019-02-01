from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from django.db.models.functions import Concat
from phonenumber_field.modelfields import PhoneNumberField

__all__ = (
    'Team',
    'Period',
    'User',
    'UserPeriodTeam',
)


class Team(models.Model):
    name = models.CharField('팀명', max_length=20)

    class Meta:
        verbose_name = '팀'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.name}팀'


class Period(models.Model):
    number = models.PositiveSmallIntegerField('기수')

    class Meta:
        verbose_name = '기수정보'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.number}기'


class UserManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.annotate(
            full_name=Concat(
                'last_name', 'first_name', output_field=models.CharField()
            )
        )


class User(AbstractUser):
    period_set = models.ManyToManyField(
        Period, verbose_name='활동기수', blank=True,
        through='UserPeriodTeam', related_name='users', related_query_name='user',
    )
    phone_number = PhoneNumberField('전화번호', unique=True, blank=True, null=True)

    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name

    @property
    def name(self):
        return getattr(self, 'full_name', f'{self.last_name}{self.first_name}')
    name.fget.short_description = '이름'


class UserPeriodTeam(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='사용자', on_delete=models.CASCADE,
        related_name='user_period_team_set', related_query_name='user_period_team',
    )
    period = models.ForeignKey(
        Period, verbose_name='기수', on_delete=models.CASCADE,
        related_name='user_period_team_set', related_query_name='user_period_team',
    )
    team = models.ForeignKey(
        Team, verbose_name='팀', on_delete=models.CASCADE,
        related_name='user_period_team_set', related_query_name='user_period_team',
    )

    class Meta:
        verbose_name = '사용자 활동기수 정보'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.period.number}기 | {self.team.name} | {self.user.name}'
