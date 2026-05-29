from django.contrib import admin
from advertisements.models import Advertisement, Favorite


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "creator", "created_at")
    list_filter = ("status", "created_at")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "advertisement")
