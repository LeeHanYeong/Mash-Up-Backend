import os
from datetime import datetime

import openpyxl
from django.conf import settings
from django.core.management import BaseCommand

from members.forms import UserCreationForm
from members.models import Period, Team


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = os.path.join(settings.ROOT_DIR, ".temp", "members.xlsx")
        book = openpyxl.load_workbook(path)
        sheet = book.worksheets[0]

        members = {}
        current_team = None
        for row in sheet.iter_rows(min_row=2, max_col=6):
            data_list = [col.value for col in row]
            team = data_list[0]
            if team is not None:
                current_team = team
                members[current_team] = []

            if data_list[1] is None:
                continue
            cur_member = {
                "name": data_list[1].strip(),
                "birth": data_list[2],
                "email": data_list[3].strip(),
                "period": data_list[4],
                "phone": str(data_list[5]).strip(),
            }
            members[current_team].append(cur_member)

            period, _ = Period.objects.get_or_create(number=8)
            for team_name, member_info_list in members.items():
                team, _ = Team.objects.get_or_create(name=team_name)

                for member_info in member_info_list:
                    data = {
                        "name": member_info["name"],
                        "email": member_info["email"],
                    }
                    form = UserCreationForm(data=data)
                    if form.is_valid():
                        try:
                            user = form.save()
                        except:
                            continue

                        try:
                            user.birth_date = member_info["birth"]
                            user.save()
                        except Exception as eb1:
                            try:
                                user.birth_date = datetime.strptime(
                                    member_info["birth"].replace(" ", ""), "%Y.%m.%d"
                                ).date()
                                user.save()
                            except Exception as eb2:
                                user.birth_date = None
                                print("error birth!", member_info["birth"])
                                print(eb1)
                                print(eb2)
                                print()

                        try:
                            user.phone_number = member_info["phone"]
                            user.save()
                        except Exception as e1:
                            try:
                                phone = "0" + member_info["phone"]
                                user.phone_number = phone
                                user.save()
                            except Exception as e2:
                                user.phone_number = None
                                print(f"error phone! @{member_info['phone']}@")
                                print(e1)
                                print(e2)
                                print()

                        user.user_period_team_set.get_or_create(
                            period=period, team=team,
                        )
                        user.save()
                    else:
                        print(form.errors)
