from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.creator == request.user


class IsAdminOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True

        return obj.creator == request.user


class IsNotDraftOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if obj.status != "DRAFT":
            return True

        return obj.creator == request.user
