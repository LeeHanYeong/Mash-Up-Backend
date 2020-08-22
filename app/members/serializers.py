from rest_auth.serializers import TokenSerializer

from utils.drf.serializers import ModelSerializer, ModelSerializerMixin
from .models import User, Team, Period, UserPeriodTeam

__all__ = (
    "TeamSerializer",
    "PeriodSerializer",
    "UserPeriodTeamSerializer",
    "UserSerializer",
    "AuthTokenSerializer",
)


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = (
            "id",
            "name",
        )


class PeriodSerializer(ModelSerializer):
    class Meta:
        model = Period
        fields = (
            "id",
            "is_current",
            "number",
        )


class UserPeriodTeamSerializer(ModelSerializer):
    period = PeriodSerializer()
    team = TeamSerializer()

    class Meta:
        model = UserPeriodTeam
        fields = (
            "period",
            "team",
        )


class UserSerializer(ModelSerializer):
    user_period_team_set = UserPeriodTeamSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "phone_number",
            "email",
            "github",
            "user_period_team_set",
        )


class AuthTokenSerializer(ModelSerializerMixin, TokenSerializer):
    user = UserSerializer()

    class Meta(TokenSerializer.Meta):
        fields = TokenSerializer.Meta.fields + ("user",)
