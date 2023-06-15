from rest_framework import viewsets

from .models import Tags
from .serializers import TagsSerializer
from .permissions import OnlyAdminOrRead


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (OnlyAdminOrRead,)
