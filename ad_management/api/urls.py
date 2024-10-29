from django.urls import path
from ad_management.api import views as ad_views

urlpatterns = [
    path('ads/', ad_views.AdListCreateView.as_view(), name='ad-list-create'),
    path('ads/<uuid:pk>/', ad_views.AdRetrieveUpdateDeleteView.as_view(), name='ad-detail'),
    path('ads/<uuid:pk>/comments/', ad_views.CommentListCreateView.as_view(), name='comment-list-create'),
]
