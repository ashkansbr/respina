from django.shortcuts import get_object_or_404
from ad_management.models import Ad, Comment

def get_all_ads():
    return Ad.objects.all()

def get_ad_by_id(pk):
    return get_object_or_404(Ad, pk=pk)

def get_comments_for_ad(pk):
    ad = get_ad_by_id(pk)
    return ad.comments.all()