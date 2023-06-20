from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from .models import Subscribe
from .paginators import UserPaginator
from .serializers import SubscribeSerializer

User = get_user_model()


class UserViewSet(UserViewSet):
    pagination_class = UserPaginator

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)

        if request.user == author:
            return Response({'errors': 'Пописываться на себя запрещено!'},
                            status=status.HTTP_400_BAD_REQUEST)

        subscribe = Subscribe.objects.filter(user=request.user, author=author)

        if request.method == 'POST':
            if subscribe.exists():
                return Response({'errors': 'Подписка уже существует!'},
                                status=status.HTTP_400_BAD_REQUEST)

            subsctibe = Subscribe.objects.create(
                user=request.user,
                author=author
            )
            serializer = SubscribeSerializer(subsctibe)
            return Response(serializer.data)

        if subscribe.exists():
            subscribe.delete()
            return Response({'Подписка успешно удалена!'},
                            status=status.HTTP_204_NO_CONTENT)

        return Response({'error': 'Вы не подписаны на данного автора!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = Subscribe.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(pages, many=True)

        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = User.objects.get(username=request.user)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
