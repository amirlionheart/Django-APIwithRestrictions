from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorite
from advertisements.permissions import (
    IsAdminOrOwner,
    IsNotDraftOrOwner,
)
from advertisements.serializers import (
    AdvertisementSerializer,
    FavoriteSerializer,
)


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        """Фильтрует объявления в зависимости от статуса и авторизации."""
        user = self.request.user

        if user.is_authenticated:
            # Авторизованный пользователь видит OPEN объявления и свои (любого статуса)
            return Advertisement.objects.filter(Q(status="OPEN") | Q(creator=user))

        # Неавторизованный пользователь видит только OPEN объявления
        return Advertisement.objects.filter(status="OPEN")

    def get_permissions(self):
        """Устанавливает разные permissions для разных actions."""
        if self.action == "create":
            # Создавать могут только авторизованные пользователи
            return [IsAuthenticated()]

        if self.action == "retrieve":
            # Черновики может видеть только автор, остальные видят все остальные статусы
            return [IsNotDraftOrOwner()]

        if self.action in ["update", "partial_update", "destroy"]:
            # Обновлять и удалять может только автор или админ
            return [IsAuthenticated(), IsAdminOrOwner()]

        # Для остальных действий (list, favorite, favorites) доступ открыт
        return []

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """Добавляет объявление в избранное."""
        adv = self.get_object()

        # Автор не может добавить своё объявление в избранное
        if adv.creator == request.user:
            return Response(
                {"error": "Нельзя добавить своё объявление в избранное"}, status=400
            )

        obj, created = Favorite.objects.get_or_create(
            user=request.user, advertisement=adv
        )

        serializer = FavoriteSerializer(obj)

        return Response(
            {
                "status": "added" if created else "already_exists",
                "favorite": serializer.data,
            }
        )

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def favorites(self, request):
        """Возвращает все избранные объявления пользователя."""
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
