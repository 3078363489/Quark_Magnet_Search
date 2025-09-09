# installer/models.py
from django.db import models


class InstallationStatus(models.Model):
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'installation_status'