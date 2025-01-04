from django.db import models
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):
    created_ts = models.DateTimeField(auto_now_add=True, null=False)
    name = models.TextField(max_length=100, db_index=True, null=False)

    class Meta:
        db_table = "organization"

    def __unicode__(self):
        return u'%s' % self.name

# WARNING: 1 email can only be attached to 1 role
class Role(AbstractUser):
    ROLE_TYPE_CHOICES = (
        # system admin
        (1, 'Admin'),
    )

    user_type = models.PositiveSmallIntegerField(choices=ROLE_TYPE_CHOICES)
    created_ts = models.DateTimeField(auto_now_add=True, null=True)
    organization = models.ForeignKey(Organization, null=False, db_index=True, on_delete = models.CASCADE)

    class Meta:
        db_table = "role"

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)