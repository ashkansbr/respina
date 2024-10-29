from rest_framework import serializers
from ad_management.models import Ad, Comment

class AdSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Ad
        fields = ('id', 'title', 'description', 'owner', 'created_at', 'updated_at')

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    ad = serializers.ReadOnlyField(source='ad.id')

    class Meta:
        model = Comment
        fields = ('id', 'ad', 'user', 'text', 'created_at', 'updated_at')
