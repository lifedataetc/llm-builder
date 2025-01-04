from django.db import models
from picklefield.fields import PickledObjectField

# Create your models here.
class ErrorLog(models.Model):
    created_ts = models.DateTimeField(auto_now_add=True, null=True)
    error = models.TextField()
    error_function = models.TextField(db_index=True)
    request_payload = PickledObjectField()

    class Meta:
        db_table = "error_log"


# TODO: Create a scheduled task to delete old session data after 24 hours
class SessionData(models.Model):
    created_ts = models.DateTimeField(auto_now_add=True, null=True)
    session_key = models.TextField(db_index=True)
    session_type = models.TextField(db_index=True)
    session_data = PickledObjectField()

    class Meta:
        db_table = "session_data"