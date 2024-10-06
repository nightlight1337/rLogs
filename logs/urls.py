from django.urls import path
from .views import AddLogView, log_entry_list

urlpatterns = [
    path("add-log/", AddLogView.as_view(), name="add_log"),
    path("", log_entry_list, name="log_entry_list"),
]
