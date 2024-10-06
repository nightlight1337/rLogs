from django.db import models


class LogEntry(models.Model):
    category = models.CharField(max_length=64)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=384)

    def __str__(self):
        return f"{self.timestamp} - {self.category} - {self.user} - {self.message[:50]}"
