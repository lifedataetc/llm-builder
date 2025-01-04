from auth_system.models import Role, Organization

org = Organization.objects.create(name='Telperion')
org.save()

role = Role.objects.create(username='mandeep',password='180389',user_type=1,organization=org)
role.save()