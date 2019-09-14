from rest_framework import serializers

from .models import User, Team, Period, UserPeriodTeam


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            'pk',
            'name',
        )


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = (
            'pk',
            'is_current',
            'number',
        )


class UserPeriodTeamSerializer(serializers.ModelSerializer):
    period = PeriodSerializer()
    team = TeamSerializer()

    class Meta:
        model = UserPeriodTeam
        fields = (
            'period',
            'team',
        )


class UserSerializer(serializers.ModelSerializer):
    user_period_team_set = UserPeriodTeamSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'name',
            'phone_number',
            'email',
            'github',

            'user_period_team_set',
        )
