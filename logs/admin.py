from django.contrib import admin
from .models import LogEntry


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "category", "user", "message")
    list_filter = ("category", "user", "timestamp")
    search_fields = ("message",)
    ordering = ("-timestamp",)


admin.site.register(LogEntry, LogEntryAdmin)
