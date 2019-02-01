from django.contrib import admin

from .study import *
from .study_meeting import *
from ..models import *

admin.site.register(Study, StudyAdmin)
admin.site.register(StudyMembership, StudyMembershipAdmin)
admin.site.register(StudyMeeting, StudyMeetingAdmin)
admin.site.register(StudyMeetingUserActivity, StudyMeetingUserActivityAdmin)
admin.site.register(StudyMeetingFineCategory, StudyMeetingFineCategoryAdmin)
admin.site.register(StudyMeetingFine, StudyMeetingFineAdmin)
