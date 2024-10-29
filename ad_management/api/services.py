from django.core.exceptions import PermissionDenied
from ad_management.models import Ad, Comment

def create_ad(owner, data):
    return Ad.objects.create(owner=owner, **data)

def update_ad(ad, data, user):
    if ad.owner != user:
        raise PermissionDenied("You do not have permission to edit this ad.")
    for field, value in data.items():
        setattr(ad, field, value)
    ad.save()
    return ad

def delete_ad(ad, user):
    if ad.owner != user:
        raise PermissionDenied("You do not have permission to delete this ad.")
    ad.delete()

def create_comment(ad, user, text):
    if Comment.objects.filter(ad=ad, user=user).exists():
        raise PermissionDenied("You have already commented on this ad.")
    return Comment.objects.create(ad=ad, user=user, text=text)
