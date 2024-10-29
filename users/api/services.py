from ..models import BaseUser
from django.db import transaction

@transaction.atomic()
def create_user(email, password):
    return BaseUser.objects.create_user(email=email, password=password)


