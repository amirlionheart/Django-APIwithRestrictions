from rest_framework import serializers
from advertisements.models import Advertisement, Favorite


class AdvertisementSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):

        request = self.context["request"]
        status = data.get("status")

        if status == "OPEN":

            qs = Advertisement.objects.filter(creator=request.user, status="OPEN")

            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.count() >= 10:
                raise serializers.ValidationError(
                    "Нельзя иметь больше 10 открытых объявлений."
                )

        return data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"
