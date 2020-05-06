from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

from utils.django.models import Model

_TIER_NAMES = (
    ('unranked', '언랭'),
    ('iron', '아이언'),
    ('bronze', '브론즈'),
    ('silver', '실버'),
    ('gold', '골드'),
    ('platinum', '플래티넘'),
    ('diamond', '다이아몬드'),
)
TIERS = []
for k, v in _TIER_NAMES:
    for i in range(1, 6):
        TIERS.append((f'{k}{i}', f'{v}{i}'))


class LOLTeam(Model):
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '{leader}팀{members}'.format(
            leader=self.leader.name,
            members=f' ({", ".join(self.player_set.values_list("name", flat=True))})' if self.player_set.exists() else '',
        )


class Player(TimeStampedModel, Model):
    team = models.ForeignKey(LOLTeam, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    tier = models.CharField(choices=TIERS, max_length=20)
    position_set = models.ManyToManyField('Position', blank=True)

    def __str__(self):
        positions = ', '.join([position.get_name_display() for position in self.position_set.all()])
        return f'{self.name} (' \
               f'{self.get_tier_display()} | ' \
               f'{positions})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        players = Player.objects.all()
        for owner in players:
            for player in players:
                if owner != player:
                    owner.owner_point_set.get_or_create(player=player)

    @property
    def name(self):
        return self.user.name


class Position(Model):
    CHOICES_NAME = (
        ('top', '탑'),
        ('jungle', '정글'),
        ('mid', '미드'),
        ('adc', '원딜'),
        ('sup', '서폿'),
    )
    name = models.CharField(choices=CHOICES_NAME, max_length=6)

    def __str__(self):
        return self.get_name_display()


class PlayerPoint(Model):
    CHOICES_POINT = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    owner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='owner_point_set')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='point_set')
    point = models.PositiveSmallIntegerField(choices=CHOICES_POINT, blank=True, null=True)
    drip = models.CharField(verbose_name='드립을 쳐주세요', max_length=100)

    def __str__(self):
        return f'{self.player.name} ({self.point}점)'
