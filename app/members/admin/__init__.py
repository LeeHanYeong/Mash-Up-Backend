from .team_period import *
from .user import *
from ..models import *

admin.site.register(Team, TeamAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserPeriodTeam, UserPeriodTeamAdmin)
