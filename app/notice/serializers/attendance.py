from rest_framework import serializers
from ..models import Attendance


class AttendanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = (
            'vote',
        )
