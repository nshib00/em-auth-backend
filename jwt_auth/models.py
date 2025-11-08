from django.db import models
from django.contrib.auth import get_user_model


class RefreshToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
