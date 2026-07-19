from rest_framework import filters, viewsets
from rest_framework.permissions import IsAdminUser

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by(
        "username"
    )

    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]

    ordering_fields = [
        "username",
        "first_name",
        "date_joined",
        "is_active",
    ]

    ordering = [
        "username",
    ]