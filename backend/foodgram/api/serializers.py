from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Subscribe

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(
            user=self.context.get('request').user,
            author=obj.id
        ).exists()
