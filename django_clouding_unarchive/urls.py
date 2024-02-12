from django.urls import path
from .views import UnarchiveView, StatusView, IsActiveView

app_name = "django_clouding_unarchive"

urlpatterns = [
    path("server-status/", StatusView.as_view(), name="server-status"),
    path("unarchive-server/", UnarchiveView.as_view(), name="unarchive-server"),
    path("server-is-active/", IsActiveView.as_view(), name="server-is-active")
]

