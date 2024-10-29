from django.db import models
from django.contrib.auth import get_user_model
from common.basemodel import BaseModel

User = get_user_model()


class Ad(BaseModel):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    description = models.TextField()

    def __str__(self):
        return self.title


class Comment(BaseModel):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        unique_together = ('ad', 'user')

    def __str__(self):
        return f"Comment by {self.user} on {self.ad}"
