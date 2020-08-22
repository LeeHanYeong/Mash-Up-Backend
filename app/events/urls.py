from django.urls import path, include

app_name = "events"

urlpatterns = [
    path("lol/", include("events.lol.urls")),
]
