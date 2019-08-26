from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

__all__ = (
    'Team',
    'Period',
    'User',
    'UserPeriodTeam',
    'UserPeriodOutcount',
)


class Team(models.Model):
    name = models.CharField('팀명', max_length=20)

    class Meta:
        verbose_name = '팀'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.name}팀'


class Period(models.Model):
    is_current = models.BooleanField('현재 기수여부', default=False)
    number = models.PositiveSmallIntegerField('기수')

    class Meta:
        verbose_name = '기수정보'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-number', '-pk', 'is_current',)

    def __str__(self):
        return f'{self.number}기'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_current:
            Period.objects.exclude(pk=self.pk).update(is_current=False)


class UserManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs


class User(AbstractUser):
    first_name = None
    last_name = None
    period_set = models.ManyToManyField(
        Period, verbose_name='활동기수', blank=True,
        through='UserPeriodTeam', related_name='users', related_query_name='user',
    )
    phone_number = PhoneNumberField('전화번호', unique=True, blank=True, null=True)
    name = models.CharField('이름', max_length=50, blank=True)
    email = models.EmailField('이메일', unique=True)
    github = models.CharField('GitHub 사용자명', max_length=50, blank=True)

    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name


class UserPeriodTeam(models.Model):
    user = models.ForeignKey(
        User, verbose_name='사용자', on_delete=models.CASCADE,
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
        unique_together = (
            ('user', 'period'),
        )

    def __str__(self):
        return f'{self.period.number}기 | {self.team.name} | {self.user.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # UserPeriodOutcount가 없을경우 만들어준다
        self.user.user_period_outcount_set.get_or_create(period=self.period)


class UserPeriodOutcount(models.Model):
    user = models.ForeignKey(
        User, verbose_name='사용자', on_delete=models.CASCADE,
        related_name='user_period_outcount_set', related_query_name='user_period_outcount',
    )
    period = models.ForeignKey(
        Period, verbose_name='기수', on_delete=models.CASCADE,
        related_name='user_period_outcount_set', related_query_name='user_period_outcount',
    )
    count = models.DecimalField('아웃카운트', max_digits=3, decimal_places=2, default=0)

    class Meta:
        verbose_name = '사용자 활동기수별 아웃카운트 정보'
        verbose_name_plural = f'{verbose_name} 목록'
        unique_together = (
            ('user', 'period'),
        )

    def __str__(self):
        return f'{self.user.name} | {self.period.number}기 | 아웃카운트: {self.count}'
