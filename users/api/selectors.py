from ..models import BaseUser

def get_users():
    return BaseUser.objects.all()



