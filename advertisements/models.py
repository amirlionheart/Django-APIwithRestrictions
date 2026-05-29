from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(default="")

    status = models.CharField(
        max_length=10,
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN,
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ads"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "advertisement")
